<template>
  <section
    class="scroll__wrap"
    @mouseenter="stopNext()"
    @mouseleave="keepNext()">
    <div class="scroll__container">
      <div
        v-for="item in imgList"
        :key="item.activeIndex"
        :style="{ 'background-image': `url(${item.url})`}"
        class="scroll__card"
        :class="setClass(item.activeIndex)"
        @click="handleActive(item.activeIndex)" />
      <!-- <i
        class="iconfont icon-fanhui scroll__icon left"
        @click="prev()" />
      <i
        class="iconfont icon-gengduo scroll__icon right"
        @click="next()" /> -->
    </div>
    <ul class="scroll__circle">
      <li
        v-for="item in imgList"
        :key="item.activeIndex"
        :class="{ 'active': activeIndex === item.activeIndex }"
        @mouseover="handleActive(item.activeIndex)" />
    </ul>
  </section>
</template>

<script lang="ts">
export default {
  props: {
    imgList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      activeIndex: 1,
      time: null
    }
  },
  mounted() {
    this.autoSwtich();
  },
  methods: {
    /**
     * 根据activeIndex设置对应的class
     */
    setClass(i) {
      const prev = this.activeIndex === 1 ? this.imgList.length : this.activeIndex - 1;
      const next = this.activeIndex === this.imgList.length ? 1 : this.activeIndex + 1;
      switch(i) {
        case prev:
          return 'prev';
        case next:
          return 'next';
        case this.activeIndex:
          return 'active';
        default:
          return '';
      }
    },
    /**
     * 切换图片
     */
    handleActive(activeIndex) {
      this.activeIndex = activeIndex;
    },
    prev() {
      this.activeIndex = this.activeIndex === 1 ? this.imgList.length : this.activeIndex - 1;
    },
    next() {
      this.activeIndex = this.activeIndex === this.imgList.length ? 1 : this.activeIndex + 1;
    },

    /**
     * 自动切换图片
     */
    autoSwtich() {
      this.time = setInterval(() => {
        this.next();
      }, 3000);
    },

    /**
     * 鼠标进入，停止计时器
     */
    stopNext() {
      clearInterval(this.time);
    },

    /**
     * 鼠标出来，继续轮播
     */
    keepNext() {
      this.autoSwtich();
    },
    changeImage() {

    }
  },
}
</script>

<style lang="scss">
.scroll__wrap {
  width: 1300px;
  height: 100%;
  margin: 50px auto 50px auto;
  .scroll__container {
    width: 100%;
    height: 300px;
    position: relative;
    margin: 0 auto;
    perspective: 300px;
    .scroll__card {
      width: 1000px;
      height: 300px;
      border-radius: 12px;
      position: absolute;
      left: 50%;
      top: 50%;
      transition: 500ms all ease-in-out;
      transform: translate3d(-50%, -50%, -60px);
      cursor: pointer;
      background-size: cover;
      background-color: transparent;
      background-position: center;
      &:before {
        position: absolute;
        content: '';
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 12px;
        transition: 500ms all;
      }
      &.active {
        transform: translate3d(-50%, -50%, 0);
        z-index: 20;
        &:before {
          background-color: transparent;
        }
      }
      &.prev {
        transform: translate3d(-75%, -50%, -60px);
        z-index: 19;
      }
      &.next {
        transform: translate3d(-25%, -50%, -60px);
        z-index: 18;
      }
    }
    &:hover {
      .scroll__icon {
        display: block;
      }
    }
    .scroll__icon {
      display: none;
      font-size: 36px;
      color: #f5f5f7;
      position: absolute;
      top: 50%;
      z-index: 19;
      transform: translateY(-50%);
      cursor: pointer;
      &.left {
        left: 3%;
      }
      &.right {
        right: 3%;
      }
    }
  }
  .scroll__circle {
    width: 800px;
    list-style: none;
    display: flex;
    justify-content: center;
    margin: 20px auto 0 auto;
    & > li {
      margin: 0 10px;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #f5f5f5;
      cursor: pointer;
      &.active {
        background: #d33a31;
      }
    }
  }
}
</style>