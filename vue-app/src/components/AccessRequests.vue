<template>
  <div>
    <h1>Access Requests for User ID</h1>
    <form @submit.prevent="getAccessRequests">
      <input v-model="userId" placeholder="Enter User ID" />
      <button type="submit">Get Access Requests</button>
    </form>
    <div v-if="accessRequests.length">
      <h3>Access Requests</h3>
      <ul>
        <li v-for="request in accessRequests" :key="request.id">
          <p>Request ID: {{ request.id }}</p>
          <p>Timestamp: {{ request.timestamp }}</p>
          <p>Associated Permission: {{ request.associated_permission }}</p>
          <p>Outcome: {{ request.outcome ? 'Granted' : 'Denied' }}</p>
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
