<template>
  <div class="pic-material__wrap">
    <div class="banner__wrap">
      <video
        style="width: 100%"
        :src="bannerUrl" autoplay muted loop />
      <div class="banner-content">
        <h1>{{about.aboutKeyword}} + 素材矩阵</h1>
        <p>高品质小众原创媒体推广平台</p>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapGetters } from "vuex";
export default {
  props: {
    bannerUrl: {
      type: String,
      default: '/prod-api/profile/video_clip/preview/banner.mp4'
    }
  },
  computed: {
    ...mapGetters(["about"])
  }
}
</script>

<style lang="scss">
.pic-material__wrap {
  .banner__wrap {
    min-width: 1280px;
    position: relative;
    width: 100%;
    .banner-content {
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      z-index: 1;
      text-align: center;
      & > h1 {
        font-size: 40px;
        font-weight: 500;
        color: #ffffff;
        text-shadow: 1px 3px 4px rgba(0, 0, 0, 0.64);
        letter-spacing: 16px;
      }
      & > p {
        text-shadow: 1px 3px 4px rgba(0, 0, 0, 0.64);
        font-size: 20px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.75);
        margin: 4px 0 28px;
        letter-spacing: 8px;
      }
    }
  }
}
</style>
