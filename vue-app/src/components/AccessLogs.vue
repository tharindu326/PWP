<template>
  <div>
    <h1>Access Logs for User ID</h1>
    <form @submit.prevent="getAccessLogs">
      <input v-model="userId" placeholder="Enter User ID" />
      <button type="submit">Get Access Logs</button>
    </form>
    <div v-if="accessLogs.length">
      <h3>Access Logs</h3>
      <ul>
        <li v-for="log in accessLogs" :key="log.access_request_id">
          <p>Access Request ID: {{ log.access_request_id }}</p>
          <p>Timestamp: {{ log.timestamp }}</p>
          <p>Outcome: {{ log.outcome ? 'Granted' : 'Denied' }}</p>
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
      accessLogs: []
    };
  },
  methods: {
    async getAccessLogs() {
      try {
        const response = await axios.get(`http://localhost:8080/identities/${this.userId}/access-logs`, {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        this.accessLogs = response.data.message;
      } catch (error) {
        console.error(error);
        alert('Failed to retrieve access logs');
      }
    }
  }
};
</script>
