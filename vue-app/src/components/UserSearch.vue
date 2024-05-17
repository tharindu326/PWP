<template>
  <div>
    <h1 v-if="mode === 'getById'">Get User by ID</h1>
    <h1 v-if="mode === 'getByName'">Get User by Name</h1>

    <div v-if="mode === 'getById'">
      <form @submit.prevent="fetchUserById">
        <input v-model="userId" placeholder="Enter User ID" />
        <button type="submit">Fetch User</button>
      </form>
      <div v-if="user">
        <h3>User Details</h3>
        <p>ID: {{ user.id }}</p>
        <p>Name: {{ user.name }}</p>
        <p v-if="user.access_permissions && user.access_permissions.length">
          Permission Level: {{ user.access_permissions[0].permission_level }}
        </p>
      </div>
    </div>

    <div v-if="mode === 'getByName'">
      <form @submit.prevent="fetchUserByName">
        <input v-model="userName" placeholder="Enter User Name" />
        <button type="submit">Fetch User</button>
      </form>
      <div v-if="users.length">
        <h3>User Details</h3>
        <div v-for="user in users" :key="user.id">
          <p>ID: {{ user.id }}</p>
          <p>Name: {{ user.name }}</p>
          <p v-if="user.access_permissions && user.access_permissions.length">
            Permission Level: {{ user.access_permissions[0].permission_level }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['mode'],
  data() {
    return {
      userId: '',
      userName: '',
      user: null,
      users: []
    };
  },
  methods: {
    async fetchUserById() {
      try {
        const response = await axios.get(`http://localhost:8080/identities/${this.userId}`, {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        const parsedMessages = JSON.parse(response.data.message);
        this.user = parsedMessages;
      } catch (error) {
        console.error(error);
        alert('Failed to fetch user');
      }
    },
    async fetchUserByName() {
      try {
        const response = await axios.get(`http://localhost:8080/identities/name/${this.userName}`, {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        this.users = response.data.message; // Assuming message is an array
        console.log(response.data);
      } catch (error) {
        console.error(error);
        alert('Failed to fetch user');
      }
    }
  }
};
</script>
