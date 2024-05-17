<template>
  <div class="container">
    <div class="video-container">
      <video id="video" width="640" height="480" autoplay></video>
      <button class="btn capture-btn" @click="capture">Capture</button>
      <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
    </div>
    <div class="form-container">
      <input v-model="userName" placeholder="Enter Name" class="input-field">
      <select v-model="userPermission" class="input-field">
        <option disabled value="">Select Permission</option>
        <option>employee</option>
        <option>admin</option>
        <!-- Add other permissions as needed -->
      </select>
      <button class="btn register-btn" @click="registerPerson">Register</button>
    </div>
    <div v-if="capturedImages.length" class="captured-images">
      <h3>Captured Images:</h3>
      <div v-for="(image, index) in capturedImages" :key="index" class="image-preview">
        <img :src="image" :alt="'Captured Image ' + (index + 1)">
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userName: '',
      userPermission: '',
      capturedImages: [] // Array to store captured images
    };
  },
  methods: {
    capture() {
      const video = document.querySelector('#video');
      const canvas = document.querySelector('#canvas');
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // Convert canvas image to data URL and store in array
      const dataUrl = canvas.toDataURL('image/png');
      this.capturedImages.push(dataUrl);
      alert('Image captured and added to list');
    },
    async registerPerson() {
      console.log('Register button clicked');
      console.log('Username:', this.userName);
      console.log('UserPermission:', this.userPermission);

      const formData = new FormData();
      formData.append('name', this.userName);
      formData.append('permission', this.userPermission);

      // Append each captured image as a file to the FormData
      for (let i = 0; i < this.capturedImages.length; i++) {
        const response = await fetch(this.capturedImages[i]);
        const blob = await response.blob();
        const file = new File([blob], `capture_${i + 1}.png`, { type: 'image/png' });
        formData.append('image', file);
      }

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

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f7f9fc;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
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

.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-field {
  width: 100%;
  max-width: 300px;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.register-btn {
  padding: 10px 20px;
  background-color: #2ecc71;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.register-btn:hover {
  background-color: #27ae60;
}

.captured-images {
  margin-top: 20px;
  text-align: center;
}

.image-preview {
  display: inline-block;
  margin: 5px;
}

.image-preview img {
  max-width: 100px;
  max-height: 100px;
  border-radius: 5px;
}
</style>
