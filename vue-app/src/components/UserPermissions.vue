<template>
  <div>
    <h1>Permissions for User ID</h1>
    <form @submit.prevent="getUserPermissions">
      <input v-model="userId" placeholder="Enter User ID" />
      <button type="submit">Get User Permissions</button>
    </form>
    <div v-if="userPermissions.length">
      <h3>User Permissions</h3>
      <ul>
        <li v-for="permission in userPermissions" :key="permission.id">
          <p>Permission ID: {{ permission.id }}</p>
          <p>Permission Level: {{ permission.permission_level }}</p>
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
      userPermissions: []
    };
  },
  methods: {
    async getUserPermissions() {
      try {
        const response = await axios.get(`http://localhost:8080/identities/${this.userId}/permissions`, {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        this.userPermissions = response.data.message;
      } catch (error) {
        console.error(error);
        alert('Failed to retrieve user permissions');
      }
    }
  }
};
</script>
