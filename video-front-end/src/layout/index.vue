<template>
  <div class="app-wrapper">
    <sidebar class="sidebar-container" />
    <app-main />
    <end-part />

  </div>
</template>

<script>
import { AppMain,Sidebar,EndPart } from './components'
export default {
  name: "Layout",
  components: {
    Sidebar,
    AppMain,
    EndPart
  },
}
</script>

<style lang="scss" scoped>
  @import "~@/styles/mixin.scss";
  @import "~@/styles/variables.scss";

  .drawer-bg {
    background: #000;
    opacity: 0.3;
    width: 100%;
    top: 0;
    height: 100%;
    position: absolute;
    z-index: 999;
  }

  .fixed-header {
    position: fixed;
    top: 0;
    right: 0;
    z-index: 9;
    width: calc(100% - #{$sideBarWidth});
    transition: width 0.28s;
  }

  .hideSidebar .fixed-header {
    width: calc(100% - 54px)
  }

  .mobile .fixed-header {
    width: 100%;
  }

</style>
