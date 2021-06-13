<template>
  <div>
    <svg-icon icon-class="question" @click="goto"/>
  </div>
</template>

<script>
export default {
  name: 'HocassianBlog',
  data() {
    return {
      url: 'https://hocassian.cn/'
    }
  },
  methods: {
    goto() {
      window.open(this.url)
    }
  }
}
</script>
