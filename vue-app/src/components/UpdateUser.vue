<template>
  <div>
    <h1>Update User Details</h1>
    <form @submit.prevent="updateUser">
      <input v-model="userId" placeholder="Enter User ID" />
      <input v-model="userName" placeholder="Enter New Name" />
      <input type="file" ref="image" @change="onImageChange" />
      <select v-model="userPermission">
        <option disabled value="">Select New Permission</option>
        <option>employee</option>
        <option>admin</option>
        <!-- Add other permissions as needed -->
      </select>
      <button type="submit">Update User</button>
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
      userPermission: '',
      image: null
    };
  },
  methods: {
    onImageChange(event) {
      this.image = event.target.files[0];
    },
    async updateUser() {
      const formData = new FormData();
      formData.append('name', this.userName);
      formData.append('permission', this.userPermission);
      if (this.image) {
        formData.append('image', this.image);
      }

      try {
        const response = await axios.put(`http://localhost:8080/identities/${this.userId}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        console.log(response.data);
        alert(`User ${this.userId} updated successfully.`);
      } catch (error) {
        console.error(error);
        alert('Failed to update user');
      }
    }
  }
};
</script>
