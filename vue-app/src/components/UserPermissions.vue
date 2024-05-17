<template>
  <div class="container">
    <h1>Permissions for User ID</h1>
    <form @submit.prevent="getUserPermissions" class="form-container">
      <input v-model="userId" placeholder="Enter User ID" class="input-field">
      <button type="submit" class="btn">Get User Permissions</button>
    </form>
    <div v-if="userPermissions.length" class="details-container">
      <h3>User Permissions</h3>
      <ul>
        <li v-for="permission in userPermissions" :key="permission.id">
          <p><strong>Permission ID:</strong> {{ permission.id }}</p>
          <p><strong>Permission Level:</strong> {{ permission.permission_level }}</p>
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
