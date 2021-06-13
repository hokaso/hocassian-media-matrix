<template>
  <div
    :style="{
      width: width + 'px',
      height: height + 'px',
      background: background,
      color: arrowColor
    }"
    class="play-icon__wrap">
    <svg-icon
      v-show="isPlay"
      icon-class="playing"
      :style="{ 'font-size': iconSize + 'px' }" />
    <svg-icon
      v-show="!isPlay"
      icon-class="play"
      :style="{ 'font-size': iconSize + 'px' }" />
  </div>
</template>

<script>
export default {
  props: {
    width: {
      type: Number,
      required: true
    },
    height: {
      type: Number,
      required: true
    },
    background: String,
    arrowColor: String,
    iconSize: Number,
    isPlay: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      imgUrl: '@/assets/images/bgc_play.png',
    }
  }
}
</script>

<style lang="scss">
.play-icon__wrap {
  background: #d33a31;
  width: 55px;
  height: 55px;
  border-radius: 50%;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  & > i {
    font-size: 30px;
  }
}
</style>