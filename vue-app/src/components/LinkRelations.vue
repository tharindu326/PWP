<template>
  <div>
    <h1>Link Relations</h1>
    <div v-html="linkRelationsContent"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      linkRelationsContent: ''
    };
  },
  methods: {
    async fetchLinkRelations() {
      try {
        const response = await axios.get('http://localhost:8080/face_pass/link-relations', {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key if needed
          }
        });
        this.linkRelationsContent = response.data;
      } catch (error) {
        console.error(error);
        alert('Failed to load link relations');
      }
    }
  },
  mounted() {
    this.fetchLinkRelations();
  }
};
</script>

<style>
/* Add any styles you need for the link relations page here */
</style>
