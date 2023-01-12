<template>
  <v-overlay :model-value="showOverlay" class="align-center justify-center">
    <v-progress-circular indeterminate size="64" color="primary" />
  </v-overlay>
  <div class="text-h6">Publish a Workbook/Datasource to Tableau Server</div>
  <div class="text-body pt-4">
    We'll use the following methods to publish a workbook or datasource to
    Tableau Server:

    <div>
      <ul class="ul-items pl-4">
        <li>Sign In</li>
        <li>Get a List of Projects</li>
        <li>Select a File to Publish</li>
        <li>Publish Item to Server</li>
        <li>Sign-Out</li>
      </ul>
    </div>
  </div>
  <v-form ref="Form" class="publish-form pt-7">
    <v-btn color="primary" flat v-if="!projectsFetched" @click="getProjects()"
      >Get Started</v-btn
    >
    <template v-if="projectsFetched">
      <v-autocomplete
        :items="allSiteProjects"
        variant="outlined"
        dense
        return-object
        item-title="_name"
        density="compact"
        color="primary"
        label="Select a Project"
        clearable
        v-model="selectedProject"
      >
      </v-autocomplete>
      <v-radio-group
        v-model="objectType"
        direction="horizontal"
        density="compact"
        inline
        color="primary"
      >
        <v-radio value="workbook" label="Workbook" class="pr-6" />
        <v-radio value="datasource" label="Datasource" />
      </v-radio-group>

      <v-text-field
        variant="outlined"
        density="compact"
        label="Paste the path to your workbook/datasource..."
        prepend-inner-icon="mdi-paperclip"
        hint="In a real environment, you could use a file input component to automatically upload the file."
        persistent-hint
        clearable
        v-model="filePath"
        color="primary"
      ></v-text-field>
      <div class="w-100 d-flex justify-end pt-4" v-if="readyToPublish">
        <v-btn color="primary" flat @click="submitPublish()">Publish</v-btn>
      </div>
    </template>
  </v-form>
  <v-dialog :model-value="showResultDialog" class="result-dialog" persistent>
    <v-card class="px-4 py-4">
      <v-card-text>
        <div class="text-h6">
          Your {{ this.objectType }} has been published!
        </div>
        <div class="text-body pt-4">
          <a :href="this.responseObj._webpage_url" target="_blank"
            >Click here</a
          >
          to view on Tableau Server
        </div>
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
  name: "PublishContent",
  data: () => ({
    projectsFetched: false,
    projSelected: false,
    selectedFile: null,
    allSiteProjects: [],
    selectedProject: null,
    objectType: "workbook",
    filePath: null,
    showOverlay: false,
    showResultDialog: false,
    responseObj: {},
  }),
  computed: {
    readyToPublish() {
      return this.selectedProject && this.filePath;
    },
  },
  methods: {
    getProjects: async function () {
      this.showOverlay = true;

      await axios
        .get("http://localhost:5000/getProjects")
        .then((response) => {
          this.allSiteProjects = response.data;
          this.projectsFetched = true;
        })
        .catch((error) => {
          console.log("+++++++ ", error);
        });

      this.showOverlay = false;
    },

    submitPublish: async function () {
      this.showOverlay = true;

      let reqBody = {
        projectLuid: this.selectedProject._id,
        objectType: this.objectType,
        filePath: this.filePath.toString().replace(/"/g, '\\"'),
      };

      await axios
        .post("http://localhost:5000/publish", reqBody)
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

.publish-form {
  min-width: 200px;
}
.result-dialog {
  width: 600px;
}
</style>
