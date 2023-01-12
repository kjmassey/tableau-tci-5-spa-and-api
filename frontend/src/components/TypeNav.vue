<template>
  <div class="nav-outer pt-4">
    <div
      v-for="(actionType, index) in actionTypes"
      :key="index"
      class="type-div"
      :class="[
        activeTab == actionType ? 'active-type' : '',
        activeTab == actionType ? 'text-primary' : '',
      ]"
      @click="changeTab(actionType)"
    >
      {{ actionType }}
    </div>
  </div>
</template>

<script>
export default {
  name: "TypeNav",
  data: () => ({
    actionTypes: ["Onboard to Tableau", "Publish Content", "Automated Cleanup"],
    activeTab: "Onboard to Tableau",
  }),
  methods: {
    changeTab: function (tabName) {
      this.activeTab = tabName;
      this.$emit("tabChange", tabName);
    },
  },
};
</script>

<style scoped>
.nav-outer {
  display: flex;
}

.type-div {
  padding-right: 24px;
  cursor: pointer;
  user-select: none;
  font-size: 16px;
}

.active-type {
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 10px;
  text-decoration-thickness: 2px;
}
</style>
