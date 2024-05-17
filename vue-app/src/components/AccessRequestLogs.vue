<template>
  <div>
    <h1>Access Logs for Access Request ID</h1>
    <form @submit.prevent="getAccessRequestLogs">
      <input v-model="accessRequestId" placeholder="Enter Access Request ID" />
      <button type="submit">Get Access Request Logs</button>
    </form>
    <div v-if="accessRequest">
      <h3>Access Request Details</h3>
      <p>Request ID: {{ accessRequest.id }}</p>
      <p>Timestamp: {{ accessRequest.timestamp }}</p>
      <p>Associated Permission: {{ accessRequest.associated_permission }}</p>
      <p>Outcome: {{ accessRequest.outcome ? 'Granted' : 'Denied' }}</p>
      <p>User Profile ID: {{ accessRequest.user_profile_id }}</p>
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
