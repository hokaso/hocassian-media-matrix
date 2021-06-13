<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
  import { findAboutInfo } from '@/api/WebApi'
  import store from '@/store'

  export default {
    name: 'App',
    updated() {
      window.scroll(0, 0)
    },
    created() {
      findAboutInfo().then(data => {
        store.dispatch('about/toggleInfo', data.data)
      })
    }
  }
</script>

