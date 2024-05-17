<template>
  <div id="app">
    <nav>
      <button @click="view = 'camera'" :class="{ active: view === 'camera' }">Register User</button>
      <button @click="view = 'getById'" :class="{ active: view === 'getById' }">Get User by ID</button>
      <button @click="view = 'getByName'" :class="{ active: view === 'getByName' }">Get User by Name</button>
      <button @click="view = 'deleteUser'" :class="{ active: view === 'deleteUser' }">Delete User by ID</button>
      <button @click="view = 'updateUser'" :class="{ active: view === 'updateUser' }">Update User</button>
      <button @click="view = 'requestAccess'" :class="{ active: view === 'requestAccess' }">Request Access</button>
      <button @click="view = 'accessLogs'" :class="{ active: view === 'accessLogs' }">Get Access Logs</button>
      <button @click="view = 'userRequests'" :class="{ active: view === 'userRequests' }">Get Access Requests</button>
      <button @click="view = 'userPermissions'" :class="{ active: view === 'userPermissions' }">Get User Permissions</button>
      <button @click="view = 'accessLog'" :class="{ active: view === 'accessLog' }">Get Access Log</button>
      <button @click="view = 'accessRequestLogs'" :class="{ active: view === 'accessRequestLogs' }">Get Access Request Logs</button>
      <button @click="view = 'termsOfService'" :class="{ active: view === 'termsOfService' }">Terms of Service</button>
      <button @click="view = 'linkRelations'" :class="{ active: view === 'linkRelations' }">Link Relations</button>
      <button @click="view = 'facePass'" :class="{ active: view === 'facePass' }">FacePass</button>
    </nav>
    <div class="content">
      <div v-if="view === 'camera'">
        <RegisterUser />
      </div>
      <div v-if="view === 'getById'">
        <UserSearch mode="getById" />
      </div>
      <div v-if="view === 'getByName'">
        <UserSearch mode="getByName" />
      </div>
      <div v-if="view === 'deleteUser'">
        <DeleteUser />
      </div>
      <div v-if="view === 'updateUser'">
        <UpdateUser />
      </div>
      <div v-if="view === 'requestAccess'">
        <AccessRequest />
      </div>
      <div v-if="view === 'accessLogs'">
        <AccessLogs />
      </div>
      <div v-if="view === 'userRequests'">
        <UserRequests />
      </div>
      <div v-if="view === 'userPermissions'">
        <UserPermissions />
      </div>
      <div v-if="view === 'accessLog'">
        <AccessLog />
      </div>
      <div v-if="view === 'accessRequestLogs'">
        <AccessRequestLogs />
      </div>
      <div v-if="view === 'termsOfService'">
        <TermsOfService />
      </div>
      <div v-if="view === 'linkRelations'">
        <LinkRelations />
      </div>
      <div v-if="view === 'facePass'">
        <FacePass />
      </div>
    </div>
  </div>
</template>

<script>
import RegisterUser from './components/RegisterUser.vue';
import UserSearch from './components/UserSearch.vue';
import DeleteUser from './components/DeleteUser.vue';
import UpdateUser from './components/UpdateUser.vue';
import AccessRequest from './components/AccessRequest.vue';
import AccessLogs from './components/AccessLogs.vue';
import UserRequests from './components/UserRequests.vue';
import UserPermissions from './components/UserPermissions.vue';
import AccessLog from './components/AccessLog.vue';
import AccessRequestLogs from './components/AccessRequestLogs.vue';
import TermsOfService from './components/TermsOfService.vue';
import LinkRelations from './components/LinkRelations.vue';
import FacePass from './components/FacePass.vue';

export default {
  name: 'App',
  components: {
    RegisterUser,
    UserSearch,
    DeleteUser,
    UpdateUser,
    AccessRequest,
    AccessLogs,
    UserRequests,
    UserPermissions,
    AccessLog,
    AccessRequestLogs,
    TermsOfService,
    LinkRelations,
    FacePass
  },
  data() {
    return {
      view: 'camera' // Default view
    };
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 20px;
}

nav button {
  background-color: #3498db;
  border: none;
  color: white;
  padding: 10px 20px;
  margin: 5px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

nav button:hover {
  background-color: #2980b9;
}

nav button.active {
  background-color: #2980b9;
}

.content {
  padding: 20px;
  background-color: #ecf0f1;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
