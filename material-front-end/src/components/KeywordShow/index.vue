<template>
  <div class="tag__wrap">
    <div
      v-for="(tag, index) in list"
      :key="tag + index"
      v-show="tag !== ''"
      :style="{
        background: `${colorList[Math.floor(Math.random()*colorList.length)]}`
      }"
      class="tag__block"
      @click="$emit('search', tag)">
      {{ tag }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    list: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      colorList: [ '#f3edfd', '#fee9f7', '#ffe8f2', '#ffedf3', '#ffebf0', '#e9f6ff', '#e0f8fa', '#e7fcf3', '#e6fdec', '#ebfce6' ],
    }
  }
}
</script>

<style lang="scss">
.tag__wrap {
  text-align: center;
  font-size: 14px;
  color: #484848;
  .tag__block {
    display: inline-block;
    min-width: min-content;
    padding: 5px;
    border-radius: 12px;
    margin: 5px;
    cursor: pointer;
    &:hover {
      box-shadow: #bbb 0 2px 8px;
    }
  }
}
</style>
