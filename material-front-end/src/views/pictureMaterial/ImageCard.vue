<template>
  <div class="image-card__wrap">
    <div
      v-for="(img, index) in list"
      :key="img.imageId"
      class="img-block"
      :style="{width: (img.width*300/img.height)/1.5 + 'px', height: '66.6%', 'flex-grow': (img.width*300/img.height)}">
      <el-image
        :src="img.url"
        fit="fill"
        :preview-src-list="getUrlList(index)"
        :z-index="999"
        class="img">
      </el-image>
      <img
        v-show="showCopyRight"
        class="icon"
        :src="img.isCopyright === '0' ? require('@/assets/images/copyright.png') : require('@/assets/images/no-copyright.png')"  alt=""/>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    list: {
      type: Array,
      default: () => []
    },
    showCopyRight: {
      type: Boolean,
      default: false,
    },
    urlList: {
      type: Array,
      default: () => []
    },
  },
  data() {
    return {
      currentIndex: 0,
    }
  },
  methods: {
    getUrlList(index) {
      return this.urlList.slice(index).concat(this.urlList.slice(0,index))
    }
  },
}
</script>

<style lang="scss">
.image-card__wrap {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  &:after { // 处理最后一行
    content: '';
    flex-grow: 999999999;
  }
  .img-block {
    margin: 10px 0 0 10px;
    display: inline-block;
    height: 300px;
    position: relative;
    .img {
      width: 100%;
      height: 100%;
    }
    .icon {
      position: absolute;
      bottom: 10px;
      right: 10px;
      display: block;
      width: 28px;
      height: 28px;
      z-index: 1;
    }
  }
}
</style>
