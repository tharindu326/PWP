<template>
  <div>
    <h1>Terms of Service</h1>
    <div v-html="tosContent"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tosContent: ''
    };
  },
  methods: {
    async fetchTermsOfService() {
      try {
        const response = await axios.get('http://localhost:8080/face_pass/tos', {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key if needed
          }
        });
        this.tosContent = response.data;
      } catch (error) {
        console.error(error);
        alert('Failed to load terms of service');
      }
    }
  },
  mounted() {
    this.fetchTermsOfService();
  }
};
</script>

<style>
/* Add any styles you need for the terms of service page here */
</style>
