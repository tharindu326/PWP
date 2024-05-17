<template>
  <div class="container">
    <h1 v-if="mode === 'getById'">Get User by ID</h1>
    <h1 v-if="mode === 'getByName'">Get User by Name</h1>

    <div v-if="mode === 'getById'">
      <form @submit.prevent="fetchUserById" class="form-container">
        <input v-model="userId" placeholder="Enter User ID" class="input-field">
        <button type="submit" class="btn">Fetch User</button>
      </form>
      <div v-if="user" class="details-container">
        <h3>User Details</h3>
        <p><strong>ID:</strong> {{ user.id }}</p>
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p v-if="user.access_permissions && user.access_permissions.length">
          <strong>Permission Level:</strong> {{ user.access_permissions[0].permission_level }}
        </p>
      </div>
    </div>

    <div v-if="mode === 'getByName'">
      <form @submit.prevent="fetchUserByName" class="form-container">
        <input v-model="userName" placeholder="Enter User Name" class="input-field">
        <button type="submit" class="btn">Fetch User</button>
      </form>
      <div v-if="users.length" class="details-container">
        <h3>User Details</h3>
        <div v-for="user in users" :key="user.id">
          <p><strong>ID:</strong> {{ user.id }}</p>
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p v-if="user.access_permissions && user.access_permissions.length">
            <strong>Permission Level:</strong> {{ user.access_permissions[0].permission_level }}
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
        alert('User not found');
      }
    },
    async fetchUserByName() {
      try {
        const response = await axios.get(`http://localhost:8080/identities/name/${this.userName}`, {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' 
          }
        });
        this.users = response.data.message;
        console.log(response.data);
      } catch (error) {
        console.error(error);
        alert('User not found');
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
