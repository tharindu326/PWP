<template>
  <div>
    <h1>Request Access by User ID</h1>
    <form @submit.prevent="requestAccess">
      <input v-model="userId" placeholder="Enter User ID" />
      <div>
        <h2>Capture Image</h2>
        <video id="video" width="640" height="480" autoplay></video>
        <button type="button" @click="capture">Capture</button>
        <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
      </div>
      <div>
        <h2>Select Permission Level</h2>
        <select v-model="selectedPermission">
          <option disabled value="">Select Permission</option>
          <option>employee</option>
          <option>admin</option>
          <!-- Add other permissions as needed -->
        </select>
      </div>
      <button type="submit">Request Access</button>
    </form>
    <div v-if="accessData">
      <h3>Access Data</h3>
      <p>User ID: {{ accessData.user_id }}</p>
      <p>Permission Levels: </p>
      <ul>
        <li v-for="permission in accessData.permissions" :key="permission.id">
          {{ permission.permission_level }}
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
      selectedPermission: '',
      accessData: null
    };
  },
  methods: {
    capture() {
      const video = document.querySelector('#video');
      const canvas = document.querySelector('#canvas');
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
    },
    async requestAccess() {
      const canvas = document.querySelector('#canvas');
      const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));

      const formData = new FormData();
      formData.append('user_id', this.userId);
      formData.append('associated_permission', this.selectedPermission);
      formData.append('image', blob, 'capture.png');

      formData.forEach((value, key) => {
        console.log(`${key}:`, value);
      });

      try {
        const response = await axios.post(`http://localhost:8080/access_request`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
          }
        });
        this.accessData = response.data;
        console.log(response.data);
      } catch (error) {
        console.error(error);
        alert('Failed to request access');
      }
    }
  },
  mounted() {
    const video = document.getElementById('video');
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
        video.srcObject = stream;
        video.play();
      });
    }
  }
};
</script>
