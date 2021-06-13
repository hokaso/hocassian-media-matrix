<template>
  <div class="container">
    <el-menu
      :default-active="activeIndex"
      :background-color="variables.menuBg"
      :text-color="variables.menuText"
      :active-text-color="variables.menuActiveText"
      mode="horizontal"
    >
      <img
        class="logo"
        :src="'/prod-api/profile/video_matrix/' + about.aboutIcon"
        alt=""
      />
      <head-nav
        v-for="route in permission_routes"
        :key="route.path"
        :item="route"
        :base-path="route.path"
      />
    </el-menu>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import HeadNav from "./HeadNav";
import variables from "@/styles/variables.scss";

export default {
  components: { HeadNav },
  data() {
    return {};
  },
  computed: {
    ...mapGetters(["permission_routes", "about"]),
    activeIndex() {
      const route = this.$route;
      const { meta, path } = route;
      // if set path, the sidebar will highlight the path you set
      if (meta.activeMenu) {
        return meta.activeMenu;
      }
      return path;
    },
    variables() {
      return variables;
    }
  }
};
</script>
<style lang="scss" scoped>
.el-menu {
  display: flex;
  justify-content: center;
  align-items: center;
}</style
>>
