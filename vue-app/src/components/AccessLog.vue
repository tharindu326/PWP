<template>
  <div class="container">
    <h1>Access Log Details</h1>
    <form @submit.prevent="getAccessLog" class="form-container">
      <input v-model="logId" placeholder="Enter Log ID" class="input-field">
      <button type="submit" class="btn">Get Access Log</button>
    </form>
    <div v-if="accessLog" class="details-container">
      <h3>Access Log</h3>
      <p><strong>Access Request ID:</strong> {{ accessLog.access_request_id }}</p>
      <p><strong>Timestamp:</strong> {{ accessLog.timestamp }}</p>
      <p><strong>Outcome:</strong> {{ accessLog.outcome ? 'Granted' : 'Denied' }}</p>
      <p><strong>Associated Permission:</strong> {{ accessLog.associated_permission }}</p>
      <p><strong>User Profile ID:</strong> {{ accessLog.user_profile_id }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      logId: '',
      accessLog: null
    };
  },
  methods: {
    async getAccessLog() {
      try {
        const response = await axios.get(`http://localhost:8080/access-log/${this.logId}`, {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        this.accessLog = response.data.message;
      } catch (error) {
        console.error(error);
        alert('Failed to retrieve access log');
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
