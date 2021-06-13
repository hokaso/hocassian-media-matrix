<template>
  <div
    :style="{ width: width + 'px' }"
    class="popver__wrapper">
    <i class="el-icon-caret-top icon-arrow" /> 
    <slot name="container"></slot>
  </div>
</template>

<script>
export default {
  props: {
    width: {
      type: Number,
      default: 120
    },
  },
}
</script>

<style lang="scss">
.popver__wrapper {
  position: absolute;
  min-width: 120px;
  padding: 10px;
  height: 100%;
  width: 100%;
  background: #fff;
  border-radius: 4px;
  text-align: center;
  .icon-arrow {
    position: absolute;
    z-index: 999;
    top: -9px;
    color: #fff;
    right: 32px;
  }
}

.el-button--text {
  letter-spacing: 1px;
  color: #409EFF;
  background: 0 0;
  padding-left: 0;
  padding-right: 0;
}
</style>