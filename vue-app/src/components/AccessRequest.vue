<template>
  <div class="container">
    <h1>Request Access by User ID</h1>
    <form @submit.prevent="requestAccess" class="form-container">
      <div class="video-container">
        <video id="video" width="640" height="480" autoplay></video>
        <button type="button" class="btn capture-btn" @click="capture">Capture</button>
        <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
      </div>
      <select v-model="selectedPermission" class="input-field">
        <option disabled value="">Select Permission</option>
        <option>employee</option>
        <option>admin</option>
        <!-- Add other permissions as needed -->
      </select>
      <button type="submit" class="btn">Request Access</button>
    </form>
    <div v-if="accessData" class="details-container">
      <h3>Access Data</h3>
      <p><strong>Permission Levels:</strong></p>
      <ul>
        <li v-for="permission in accessData.permissions" :key="permission.id">{{ permission.permission_level }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
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
      alert('Image captured and drawn on canvas');
    },
    async requestAccess() {
      const canvas = document.querySelector('#canvas');

      console.log('Request Access button clicked');
      console.log('SelectedPermission:', this.selectedPermission);

      canvas.toBlob(async (blob) => {
        const file = new File([blob], 'capture.png', { type: 'image/png' }); // Create a File object from the Blob
        const formData = new FormData();
        formData.append('image', file); // Append the File object to FormData
        formData.append('associated_permission', this.selectedPermission);

        formData.forEach((value, key) => {
          console.log(`${key}:`, value);
        });

        try {
          const response = await axios.post('http://localhost:8080/identities/access-request', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Authorization': '4fd3efa18991cf343d2dfc1b7b698ac4' // Replace with your actual API key
            }
          });
          this.accessData = response.data;
          console.log(response.data);
        } catch (error) {
          console.error(error);
          const errorMessage = error.response && error.response.data && error.response.data.error
            ? error.response.data.error
            : 'Access Request Failed';
          alert(errorMessage);
        }
      }, 'image/png'); // Specify the image format here
    }
  },
  mounted() {
    const video = document.getElementById('video');
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
        video.srcObject = stream;
        video.play();
      });
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

.video-container {
  position: relative;
  margin-bottom: 20px;
}

.capture-btn {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  background-color: #3498db;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.capture-btn:hover {
  background-color: #2980b9;
}

.btn {
  padding: 10px 20px;
  background-color: #2ecc71;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #27ae60;
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
