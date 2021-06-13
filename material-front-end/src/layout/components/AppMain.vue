<template>
  <section class="app-main">
    <transition name="fade-transform" mode="out-in">
      <router-view :key="key" />
    </transition>
  </section>
</template>

<script>
export default {
  name: "AppMain",
  computed: {
    key() {
      return this.$route.path;
    }
  }
};
</script>

<style scoped lang="scss">
.app-main {
  min-height: calc(100vh - 50px);
    width: 100%;
    position: relative;
    overflow: hidden;
    background-color: rgba(255, 244, 243, 0.22);
}

.fixed-header + .app-main {
  padding-top: 50px;
}
.el-popup-parent--hidden {
  .fixed-header {
    padding-right: 15px;
  }
}
</style>
