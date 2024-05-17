<template>
  <div class="container">
    <h1>Access Requests for User ID</h1>
    <form @submit.prevent="getAccessRequests" class="form-container">
      <input v-model="userId" placeholder="Enter User ID" class="input-field">
      <button type="submit" class="btn">Get Access Requests</button>
    </form>
    <div v-if="accessRequests.length" class="details-container">
      <h3>Access Requests</h3>
      <ul>
        <li v-for="request in accessRequests" :key="request.id">
          <p><strong>Request ID:</strong> {{ request.id }}</p>
          <p><strong>Timestamp:</strong> {{ request.timestamp }}</p>
          <p><strong>Associated Permission:</strong> {{ request.associated_permission }}</p>
          <p><strong>Outcome:</strong> {{ request.outcome ? 'Granted' : 'Denied' }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userId: '',
      accessRequests: []
    };
  },
  methods: {
    async getAccessRequests() {
      try {
        const response = await axios.get(`http://localhost:8080/identities/${this.userId}/requests`, {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        this.accessRequests = response.data.message;
      } catch (error) {
        console.error(error);
        alert('Failed to retrieve access requests');
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

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background-color: #ecf0f1;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}
</style>
