<template>
  <div id="app">
    <nav>
      <button @click="view = 'camera'">Camera Input</button>
      <button @click="view = 'getById'">Get User by ID</button>
      <button @click="view = 'getByName'">Get User by Name</button>
      <button @click="view = 'deleteUser'">Delete User by ID</button>
      <button @click="view = 'updateUser'">Update User</button>
      <button @click="view = 'requestAccess'">Request Access</button>
      <button @click="view = 'accessLogs'">Get Access Logs</button>
      <button @click="view = 'userRequests'">Get Access Requests</button>
      <button @click="view = 'userPermissions'">Get User Permissions</button>
      <button @click="view = 'accessLog'">Get Access Log</button>
      <button @click="view = 'accessRequestLogs'">Get Access Request Logs</button>
      <button @click="view = 'termsOfService'">Terms of Service</button>
      <button @click="view = 'linkRelations'">Link Relations</button>
      <button @click="view = 'userProfile'">User Profile</button>
    </nav>
    <div v-if="view === 'camera'">
      <CameraInput />
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
    <div v-if="view === 'userProfile'">
      <UserProfile />
    </div>
  </div>
</template>

<script>
import CameraInput from './components/CameraInput.vue';
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
import UserProfile from './components/UserProfile.vue';

export default {
  name: 'App',
  components: {
    CameraInput,
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
    UserProfile
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
  margin-top: 60px;
}

nav button {
  margin: 10px;
}
</style>
