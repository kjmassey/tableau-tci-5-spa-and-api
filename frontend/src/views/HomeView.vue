<template>
  <div class="gray-bg">
    <div class="outer">
      <div class="main-card-div pt-16">
        <v-card class="main-card py-4 px-4">
          <v-card-title class="text-h4">
            Let's look at some practical examples!
          </v-card-title>
          <v-card-text>
            <Nav @tabChange="changeActiveTab($event)"></Nav>
          </v-card-text>
          <v-card-item>
            <OnboardToServer v-if="activeTab == 'Onboard to Tableau'" />
            <DeployContent v-if="activeTab == 'Publish Content'" />
            <AutomatedCleanup v-if="activeTab == 'Automated Cleanup'" />
          </v-card-item>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

// Components
import Nav from "@/components/TypeNav.vue";
import OnboardToServer from "@/components/OnboardToServer";
import DeployContent from "@/components/PublishContent.vue";
import AutomatedCleanup from "@/components/AutomatedCleanUp.vue";

export default defineComponent({
  name: "HomeView",

  data: () => ({
    activeTab: "Onboard to Tableau",
  }),

  components: { Nav, OnboardToServer, DeployContent, AutomatedCleanup },
  methods: {
    changeActiveTab: function (typeName) {
      this.activeTab = typeName;
    },
  },
});
</script>

<style scoped>
.outer {
  display: flex;
  width: 100%;
  justify-content: center;
}
.main-card-div {
  width: 725px;
  align-self: baseline;
}

.main-card {
  width: 100%;
}
.gray-bg {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  background-color: lightgray;
  height: 100%;
  width: 100%;
}

.gray-bg > div {
  width: 100%;
  align-items: center;
}
</style>
