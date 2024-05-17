<template>
  <div class="container">
    <h1>Delete User by ID</h1>
    <form @submit.prevent="deleteUser" class="form-container">
      <input v-model="userId" placeholder="Enter User ID" class="input-field">
      <button type="submit" class="btn">Delete User</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userId: ''
    };
  },
  methods: {
    async deleteUser() {
      try {
        const response = await axios.delete(`http://localhost:8080/identities/${this.userId}`, {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        alert(`User ${this.userId} deleted successfully`);
        console.log(response.data);
      } catch (error) {
        console.error(error);
        alert('No such user found');
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
  background-color: #e74c3c;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #c0392b;
}
</style>
