<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import WebApi from "@/api/WebApi";
import store from "@/store";
export default {
  name: "App",
  // updated() {
  //     window.scroll(0, 0);
  // },
  created() {
    WebApi.findAboutInfo().then(data => {
      store.dispatch("about/toggleInfo", data);
    });
  }
};
</script>
