<template>
  <div>
    <video id="video" width="640" height="480" autoplay></video>
    <button @click="capture">Capture</button>
    <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
    <!-- Input for user details -->
    <input v-model="userName" placeholder="Enter Name">
    <select v-model="userPermission">
      <option disabled value="">Select Permission</option>
      <option>employee</option>
      <option>admin</option>
      <!-- Add other permissions as needed -->
    </select>
    <!-- Button triggers registration -->
    <button @click="registerPerson">Register</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userName: '',
      userPermission: ''
    };
  },
  methods: {
    capture() {
      const video = document.querySelector('#video');
      const canvas = document.querySelector('#canvas');
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      alert('Image captured and drawn on canvas');
    },
    async registerPerson() {
      const canvas = document.querySelector('#canvas');

      console.log('Register button clicked');
      console.log('Username:', this.userName);
      console.log('UserPermission:', this.userPermission);

      canvas.toBlob(async (blob) => {
        const file = new File([blob], 'capture.png', { type: 'image/png' }); // Create a File object from the Blob
        const formData = new FormData();
        formData.append('image', file); // Append the File object to FormData
        formData.append('name', this.userName);
        formData.append('permission', this.userPermission);

        formData.forEach((value, key) => {
          console.log(`${key}:`, value);
        });
        try {
          const response = await axios.post('http://localhost:8080/identities', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
            }
          });
          if (response.status == 201) {
            alert(`Registration Successful: ${response.status}`);
          } else {
            alert('Registration Successful');
          }
        } catch (error) {
          console.error(error);
          const errorMessage = error.response && error.response.data && error.response.data.error
            ? error.response.data.error
            : 'Registration Failed';
          alert(errorMessage);
        }
      }, 'image/png'); // Specify the image format here
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