<template>
  <div>
    <svg-icon icon-class="github" @click="goto"/>
  </div>
</template>

<script>
export default {
  name: 'HocassianGit',
  data() {
    return {
      url: 'https://github.com/hokaso/'
    }
  },
  methods: {
    goto() {
      window.open(this.url)
    }
  }
}
</script>
