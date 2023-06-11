<template>
  <div>
    <el-carousel
      v-if="!isMobile && listTemp"
      :interval="5000"
      type="card"
      height="22vw"
      style="padding: 40px 0 10px 0;"
    >
      <el-carousel-item v-for="(row, i) in listTemp" :key="i">
        <el-row type="flex" class="row-bg" justify="center">
          <el-col
            :span="7"
            :id="'T_' + (i * 3 + j)"
            v-for="(cell, j) in row"
            :key="cell.id"
            :offset="j > 0 ? 1 : 0"
          >
            <router-link :to="'/video/' + cell.videoId">
              <el-card :body-style="{ padding: '0px' }">
                <img :src="cell.videoPic" class="image" alt=""/>
                <div class="video_title">
                  <span>{{ cell.videoTitle }}</span>
                </div>
              </el-card>
            </router-link>
          </el-col>
        </el-row>
      </el-carousel-item>
    </el-carousel>
    <swiper
      class="swiper"
      :options="swiperOption"
      ref="swiper"
      @click-slide="handleClick"
      v-if="isMobile"
    >
      <swiper-slide v-for="(row, i) in list" :key="i">
        <router-link :to="'/video/' + row.videoId">
          <el-card :body-style="{ padding: '0px' }">
            <img :src="row.videoPic" class="full" alt=""/>
            <div class="video_title">
              <span>{{ row.videoTitle }}</span>
            </div>
          </el-card>
        </router-link>
      </swiper-slide>
      <div class="swiper-pagination " slot="pagination"></div>
      <div class="swiper-button-prev" slot="button-prev"></div>
      <div class="swiper-button-next" slot="button-next"></div>
    </swiper>
  </div>
</template>

<script>
  import WebApi from "@/api/WebApi";
  import {mapState} from "vuex";

  export default {
    name: "GridSwitch",
    data() {
      return {
        total: "",
        index: "",
        videoPic: "",
        videoHugePic: "",
        videoTitle: "",
        videoProfile: "",
        listTemp: null,
        list: [],
        listQuery: {
          pageNum: 1,
          pageSize: 10,
          videoIsHuge: "2"
        },
        swiperOption: {
          effect: "coverflow",
          grabCursor: true,
          centeredSlides: true,
          slidesPerView: "2",
          coverflowEffect: {
            rotate: 50,
            stretch: 0,
            depth: 100,
            modifier: 1,
            slideShadows: false
          },
          pagination: {
            el: ".swiper-pagination"
          },
          autoplay: {
            delay: 2500,
            disableOnInteraction: false
          },
          navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev"
          }
        }
      };
    },
    computed: {
      // listTemp() {
      //   const _list = this.list, listTemp = [], sectionCount = 3;
      //   for (const i in _list) {
      //     const index = parseInt((i / sectionCount).toString());
      //     if (listTemp.length <= index) {
      //       listTemp.push([]);
      //     }
      //     listTemp[index].push(_list[i]);
      //   }
      //   return listTemp;
      // }
      ...mapState("app", ["isMobile"])
    },
    created() {
      this.getRefresh();
    },
    methods: {
      getRefresh() {
        WebApi.findAllVideo(this.listQuery).then(data => {
          this.list = data.rows;
          this.total = data.total;
          Object.keys(this.list).forEach(key => {
            this.list[key].videoPic = "/prod-api/profile/video_matrix/" + this.list[key].videoHugePic
          });
          // console.log(this.list)
          const _list = this.list,
            listTemp = [],
            sectionCount = 2;
          for (const i in _list) {

            const index = parseInt((i / sectionCount).toString());
            if (listTemp.length <= index) {
              listTemp.push([]);
            }
            if (Object.prototype.hasOwnProperty.call(_list, i)) {
              listTemp[index].push(_list[i]);
            }

          }
          this.listTemp = listTemp;
        });
      },
      handleClick(data) {
        this.$router.push(`/video/${this.list[data].id}`);
      }
    }
  };
</script>

<style lang="scss">
  @media screen and (min-width: 768px) {
    .image {
      width: 100%;
      display: block;
    }
    .info {
      font-size: 13px;
      color: #999;
    }
    .bottom {
      margin-top: 13px;
      line-height: 12px;
    }
    .el-carousel__mask {
      opacity: 0;
    }
    .video_title {
      padding: 10px 10px 5px;
      font-size: 14px;
    }
  }

  @media screen and (max-width: 768px) {
    .swiper {
      padding-bottom: 24px;
      padding-top: 22px;

      .swiper-item {
        height: 100%;
        text-align: center;
        font-size: 16px;
        background: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
      }
    }
    .full {
      display: block;
      width: 100%;
    }
    .swiper-pagination {
      bottom: 0 !important;
    }
    .video_title {
      padding: 10px 10px 5px;
      font-size: 14px;
    }
  }
</style>
