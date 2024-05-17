<template>
  <div>
    <h1>Access Log Details</h1>
    <form @submit.prevent="getAccessLog">
      <input v-model="logId" placeholder="Enter Log ID" />
      <button type="submit">Get Access Log</button>
    </form>
    <div v-if="accessLog">
      <h3>Access Log</h3>
      <p>Access Request ID: {{ accessLog.access_request_id }}</p>
      <p>Timestamp: {{ accessLog.timestamp }}</p>
      <p>Outcome: {{ accessLog.outcome ? 'Granted' : 'Denied' }}</p>
      <p>Associated Permission: {{ accessLog.associated_permission }}</p>
      <p>User Profile ID: {{ accessLog.user_profile_id }}</p>
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
