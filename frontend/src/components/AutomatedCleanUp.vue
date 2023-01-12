<template>
  <v-overlay :model-value="showOverlay" class="align-center justify-center">
    <v-progress-circular indeterminate size="64" color="primary" />
  </v-overlay>
  <div class="text-h6">Automatically Identify Items for Cleanup</div>
  <div class="text-body pt-4">
    We'll use the following methods to create a new project, a new server group,
    add a user and add permissions:

    <div>
      <ul class="ul-items pl-4">
        <li>Sign In</li>
        <li>Filter a list of items (workbooks) based on their modified date</li>
        <li>Return this list here</li>
        <li>Sign-Out</li>
      </ul>
    </div>
  </div>
  <div class="cal-picker pt-8">
    <div class="text-body-2 pl-1 pb-2">Find items last modified before:</div>
    <Datepicker
      v-model="selectedDate"
      placeholder="Pick A Date"
      :enable-time-picker="false"
    />
  </div>
  <div class="d-flex justify-start pt-6" v-if="this.selectedDate">
    <v-btn color="primary" @click="submitItemSearch()">Find Items</v-btn>
  </div>
  <v-dialog :model-value="showFoundDialog" class="result-dialog" persistent>
    <v-card class="px-4 py-4">
      <v-card-text>
        <div class="text-h6 pb-4">
          The following workbooks match your search:
        </div>
        <div
          class="text-body"
          v-for="(wb, index) in responseObj"
          :key="wb - { index }"
        >
          <a :href="wb._webpage_url" target="_blank">{{ wb.name }}</a>
        </div>
      </v-card-text>
      <v-card-actions>
        <div class="w-100 d-flex justify-end">
          <v-btn variant="outlined" @click="showFoundDialog = false"
            >Close</v-btn
          >
        </div></v-card-actions
      >
    </v-card>
  </v-dialog>
</template>

<script>
import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import axios from "axios";

export default {
  name: "AutomatedCleanup",
  components: { Datepicker },
  data: () => ({
    selectedDate: null,
    showOverlay: false,
    showFoundDialog: false,
    responseObj: {},
  }),
  methods: {
    submitItemSearch: async function () {
      this.showOverlay = true;

      let reqBody = {
        cleanUpType: this.cleanUpType,
        selectedDate: this.selectedDate,
      };

      await axios
        .post("http://localhost:5000/findItems", reqBody)
        .then((response) => {
          this.responseObj = response.data.map((e) => JSON.parse(e));
          this.showFoundDialog = true;
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
.result-dialog {
  width: 600px;
}

.cal-picker {
  width: 33%;
}
</style>
