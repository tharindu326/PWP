<template>
  <div class="container">
    <h1>Access Logs for Access Request ID</h1>
    <form @submit.prevent="getAccessRequestLogs" class="form-container">
      <input v-model="accessRequestId" placeholder="Enter Access Request ID" class="input-field">
      <button type="submit" class="btn">Get Access Request Logs</button>
    </form>
    <div v-if="accessRequest" class="details-container">
      <h3>Access Request Details</h3>
      <p><strong>Request ID:</strong> {{ accessRequest.id }}</p>
      <p><strong>Timestamp:</strong> {{ accessRequest.timestamp }}</p>
      <p><strong>Associated Permission:</strong> {{ accessRequest.associated_permission }}</p>
      <p><strong>Outcome:</strong> {{ accessRequest.outcome ? 'Granted' : 'Denied' }}</p>
      <p><strong>User Profile ID:</strong> {{ accessRequest.user_profile_id }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      accessRequestId: '',
      accessRequest: null
    };
  },
  methods: {
    async getAccessRequestLogs() {
      try {
        const response = await axios.get(`http://localhost:8080/access-request/${this.accessRequestId}`, {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        this.accessRequest = response.data.message;
      } catch (error) {
        console.error(error);
        alert('Failed to retrieve access request logs');
      }
    }
  }
};
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f7f9fc;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 0 auto;
}

.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.input-field {
  width: 100%;
  max-width: 300px;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn {
  padding: 10px 20px;
  background-color: #3498db;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #2980b9;
}

.details-container {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
}
</style>
