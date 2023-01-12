<template>
  <v-overlay :model-value="showOverlay" class="align-center justify-center">
    <v-progress-circular indeterminate size="64" color="primary" />
  </v-overlay>
  <div class="text-h6">Create a brand new project on Tableau Server!</div>
  <div class="text-body pt-4">
    We'll use the following methods to create a new project, a new server group,
    add a user and add permissions:

    <div>
      <ul class="ul-items pl-4">
        <li>Sign In</li>
        <li>Create Project</li>
        <li>Create Group</li>
        <li>Add User to Site</li>
        <li>Add User to Group</li>
        <li>Add Project Permissions</li>
        <li>Sign-Out</li>
      </ul>
    </div>
  </div>
  <v-form ref="onboardForm" class="onboard-form pt-7">
    <v-text-field
      variant="outlined"
      density="compact"
      label="Project Name"
      light
      v-model="projName"
      color="primary"
    ></v-text-field>
    <v-text-field
      variant="outlined"
      density="compact"
      label="Group Name"
      v-model="groupName"
      color="primary"
    ></v-text-field>
    <v-text-field
      variant="outlined"
      density="compact"
      label="New User Email"
      color="primary"
      v-model="userEmail"
    ></v-text-field>
    <div class="w-100 d-flex justify-end">
      <v-btn color="primary" flat @click="submitOnboard()">Create</v-btn>
    </div>
  </v-form>
  <v-dialog :model-value="showResultDialog" class="result-dialog" persistent>
    <v-card class="px-4 py-4">
      <v-card-text>
        <div class="text-h6">All actions have completed!</div>
        <div class="text-body pt-4">
          <strong>New Project Details:</strong>
        </div>
        <div class="text-body pt-2">
          Name: {{ this.responseObj.project._name }}
        </div>
        <div class="text-body">LUID: {{ this.responseObj.project._id }}</div>
        <div class="text-body pt-4">
          <strong>New Group Details:</strong>
        </div>
        <div class="text-body pt-2">
          Name: {{ this.responseObj.group._name }}
        </div>
        <div class="text-body">LUID: {{ this.responseObj.group._id }}</div>
        <div class="text-body pt-4">
          <strong>New User Details:</strong>
        </div>
        <div class="text-body pt-2">
          Name: {{ this.responseObj.user._name }}
        </div>
        <div class="text-body">LUID: {{ this.responseObj.user._id }}</div>
      </v-card-text>
      <v-card-actions>
        <div class="w-100 d-flex justify-end">
          <v-btn variant="outlined" @click="showResultDialog = false"
            >Close</v-btn
          >
        </div></v-card-actions
      >
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";

export default {
  name: "OnboardToServer",
  data: () => ({
    projName: "",
    groupName: "",
    userEmail: "",
    showOverlay: false,
    showResultDialog: false,
    responseObj: {},
  }),
  methods: {
    submitOnboard: async function () {
      this.showOverlay = true;

      let reqBody = {
        projectName: this.projName,
        groupName: this.groupName,
        userEmail: this.userEmail,
      };

      await axios
        .post("http://localhost:5000/onboard", reqBody)
        .then((response) => {
          this.responseObj = response.data;
          this.showResultDialog = true;
        })
        .catch((error) => {
          console.log("----- error: ", error);
        });

      this.showOverlay = false;
    },
  },
};
</script>

<style scoped>
.ul-items > li {
  margin-left: 20px;
  list-style-type: disc;
}

.onboard-form {
  min-width: 200px;
}
.result-dialog {
  width: 50%;
}
</style>
