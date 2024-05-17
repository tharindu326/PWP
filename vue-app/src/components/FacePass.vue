<template>
  <div>
    <div v-html="profileContent"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FacePass',
  data() {
    return {
      profileContent: ''
    };
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await axios.get('http://localhost:8080/face_pass/profile', {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key if needed
          }
        });
        this.profileContent = response.data;
      } catch (error) {
        console.error(error);
        alert('Failed to load profile');
      }
    }
  },
  mounted() {
    this.fetchProfile();
  }
};
</script>

<style>
/* Add any styles you need for the profile page here */
</style>
