<template>
  <div class="container">
    <h1>Update User</h1>
    <form @submit.prevent="updateUser" class="form-container">
      <input v-model="userId" placeholder="Enter User ID" class="input-field">
      <input v-model="userName" placeholder="Enter New Name" class="input-field">
      <select v-model="userPermission" class="input-field">
        <option disabled value="">Select New Permission</option>
        <option>employee</option>
        <option>admin</option>
        <!-- Add other permissions as needed -->
      </select>
      <button type="submit" class="btn">Update User</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userId: '',
      userName: '',
      userPermission: ''
    };
  },
  methods: {
    async updateUser() {
      const formData = new FormData();
      formData.append('name', this.userName);
      formData.append('permission', this.userPermission);

      try {
        const response = await axios.put(`http://localhost:8080/identities/${this.userId}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        alert(`User ${this.userId} updated successfully`);
        console.log(response.data);
      } catch (error) {
        console.error(error);
        alert('Failed to update user');
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
  background-color: #f39c12;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #e67e22;
}
</style>
