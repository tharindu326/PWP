<template>
  <div>
    <h1>Delete User by ID</h1>
    <form @submit.prevent="deleteUserById">
      <input v-model="deleteUserId" placeholder="Enter User ID" />
      <button type="submit">Delete User</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      deleteUserId: '' // Input for deleting user
    };
  },
  methods: {
    async deleteUserById() {
      try {
        const response = await axios.delete(`http://localhost:8080/identities/${this.deleteUserId}`, {
          headers: {
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        console.log(response.data);
        alert(`User with ID ${this.deleteUserId} has been deleted.`);
        this.deleteUserId = ''; // Clear the input field after deletion
      } catch (error) {
        console.error(error);
        alert('Failed to delete user');
      }
    }
  }
};
</script>
