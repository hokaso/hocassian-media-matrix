<template>
  <div>
    <Banner />
    <div class="main-classify">
      <div class="sort">
        <div class="border-title">
          <i>
            <span>热门影视素材</span>
          </i>
        </div>
        <PicVideo
          :list="videoList"
          :width="360"
          class="pic-video__container" />
      </div>
      <div class="sort">
        <div class="border-title">
          <i>
            <span>热门音频素材</span>
          </i>
        </div>
        <SongCard
          :list="musicList"
          @getPlayListIndex="getPlayListIndex" />
      </div>
      <div class="sort">
        <div class="border-title">
          <i>
            <span>热门图片素材</span>
          </i>
        </div>
        <ImageCard
          :list="imageList"
          :urlList="urlList"
          class="image__container" />
      </div>
    </div>
    <AudioPlay
      v-if="canPlay"
      :playList="musicList"
      :currentIndex.sync="currentIndex"
      :isAccompany="isAccompany" />
  </div>
</template>

<script>
  import MySwiper from '@/components/Swiper';
  import { findAllClip, musicList, musicPic } from '@/api/WebApi';
  import { imageList } from '@/api/pic';
  import PicVideo from '@/components/PicVideo';
  import Banner from '@/components/Banner/index.vue';
  import SongCard from '../musicMaterial/SongCard.vue';
  import AudioPlay from '../musicMaterial/AudioPlay.vue';
  import ImageCard from '../pictureMaterial/ImageCard.vue';

  export default {
    components: { MySwiper, PicVideo, Banner, SongCard, AudioPlay, ImageCard },
    data() {
      return {
        name: 'newest',
        bannerUrl: '/prod-api/profile/video_clip/preview/banner.mp4',
        videoList: [],
        musicList: [],
        isAccompany: false, // 是否为伴奏
        currentIndex: 0,
        canPlay: false,
        imageList: [],
        urlList: [],
      }
    },
    created() {
      this.getVideoList();
      this.getMusicList();
      this.getImageList();
    },
    methods: {
      getVideoList() {
        findAllClip({
          pageNum: 1,
          pageSize: 9,
          materialTag: ''
        }).then(data => {
          this.videoList = data.rows;
          Object.keys(this.videoList).forEach(
            key =>{
              this.videoList[key].materialPicPath =
                "/prod-api/profile/video_clip/clip_slot/" + this.videoList[key].materialPath + "_cover.jpg";
              this.videoList[key].videoPath = "/prod-api/profile/video_clip/preview/" + this.videoList[key].materialPath + ".mp4";
              this.videoList[key].isShow = false;
            }
          );
        });
      },
      /**
       * 获取热门音频
       */
      async getMusicList() {
        const picArr = await this.getMusicPic();
        const len = picArr.length;
        let i = 0;
        const { rows } = await musicList({
          audioName: '',
          pageNum: 1,
          pageSize: 36,
        });
        this.musicList = rows.map(item => ({
          ...item,
          picUrl: process.env.VUE_APP_BASE_API + `/profile/image/${picArr[`${i > len ? i = 0 : i++ }`]}_color_mini.jpg`,
          canShow: false
        }));
      },
      async getMusicPic() {
        const { data } = await musicPic();
        return data;
      },
      /**
       * @param index 当前索引值
       * @param isAccompany 是否为伴奏
       */
      getPlayListIndex(index, isAccompany) {
        this.canPlay = false;
        this.isAccompany = isAccompany;
        this.currentIndex = index;
        this.$nextTick(() => {
          this.canPlay = true;
        });
      },
      /**
       * 获取热门图片
       */
      async getImageList() {
        this.urlList = [];
        const { rows, total } = await imageList({
          imageTag: '',
          pageNum: 1,
          pageSize: 10,
        });
        this.imageList = rows.map((item) => {
          item.url = process.env.VUE_APP_BASE_API + `/profile/image/${item.imagePath}_mini.jpg`;
          item.width = item.imageSize.split('*')[0]/10;
          item.height = item.imageSize.split('*')[1]/10;
          this.urlList.push(process.env.VUE_APP_BASE_API + `/profile/image/${item.imagePath}.jpg`)
          return {...item};
        });
      },
    }
  }
</script>

<style lang="scss">
  .main-classify {
    margin-bottom: 50px;
    .sort {
      display: block;
      padding: 50px 0 20px;
      .pic-video__container {
        margin: 0 auto;
      }
      .image__container {
        width: 1320px;
        margin: 20px auto;
      }
    }
  }

  body {
    color: #000;
    margin: 0 auto;
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", STHeiti, sans-serif;
    font-size: 12px;
    height: auto !important;
    min-height: 100%;
    position: relative;
    -webkit-text-size-adjust: none;
    -webkit-tap-highlight-color: rgba(240, 240, 240, 0);
    /*-moz-tap-highlight-color: rgba(240,240,240,0);*/
    min-width: 1280px;
    overflow-x: auto;
  }

  .border-title {
    font-size: 32px;
    font-weight: 500;
    text-align: center;
    color: #333333;
    position: relative;
    padding-bottom: 30px;

    i {
      display: inline-block;
      position: relative;
      font-style: normal;
    }

    i::before {
      top: 0;
      left: 0;
    }

    i::after {
      bottom: 0;
      right: 0;
    }

    i::before, i::after {
      content: "";
      position: absolute;
      width: 3px;
      height: 10px;
      background-color: #e74b3b;
    }

    span {
      display: inline-block;
      position: relative;
      padding: 0 12px;
    }

    span::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 10px;
      height: 3px;
      background-color: #e74b3b;
    }

    span::after {
      content: "";
      display: block;
      position: absolute;
      bottom: 0;
      right: 0;
      width: 10px;
      height: 3px;
      background-color: #e74b3b;
    }
  }
</style>
