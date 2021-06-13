<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
  import {findAboutInfo} from "@/api/business/about";
  import store from '@/store'

  export default {
    name: 'App',
    // updated() {
    //   window.scroll(0, 0);
    // },
    created() {
      findAboutInfo().then(data => {
        console.log(data.data)
        store.dispatch("about/toggleInfo", data.data)
      })
    },
  }
</script>
