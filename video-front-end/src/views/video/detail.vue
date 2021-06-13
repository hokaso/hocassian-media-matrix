<template>
  <div>
    <!--    <VueXgplayer :config="configMp4" :rootStyle="rootStyleMp4" @player="Player = $event"/>-->
    <div v-if="!isMobile" style="padding: 70px 0;">
      <el-row type="flex" justify="center">
        <el-col :span="24" class="banner">
          <img src="../../assets/article_fill.jpg" style="margin:0 auto" alt/>
        </el-col>
      </el-row>
      <el-row :gutter="20" class="container_wrap" type="flex" justify="center" style="margin-bottom: 10px;">
        <div style="min-width:1400px">
          <el-col :offset="2" :span="20" style="display:inline-block;" class="main_container">
            <h1 class="main_title">{{ videoDetail.videoTitle }}</h1>
            <div class="video-info">
              <div class="article_info">
                <span style="padding-left: 8px">&emsp; 作者：{{ videoDetail.busChannel.channelOwner }}</span>
              </div>
              <div class="article_info">
                <span>发布时间：{{videoDetail.videoPublish}}</span>

              </div>
              <div class="ipv6_info">
                <span>IPv6加速通道（请确认所在网域已开启ipv6）：</span>
              </div>
              <el-switch
                v-model="ipv6"
                active-value="0"
                inactive-value="1"
                @change="useIPV6()"
              ></el-switch>
            </div>
            <div class="video_detail">
              <div id="mse"></div>
            </div>
            <div class="video_info">视频简介：{{ videoDetail.videoProfile }}</div>
          </el-col>
          <el-col :span="4" :offset="1" style="display:inline-block;">
            <div class="block-title">推荐视频</div>
            <el-row v-for="item in list" class="abbr_article_single" :key="item.videoId">
              <router-link :to="'/video/' + item.videoId">
                <div class="abbr_article_word">
                  <div class="abbr_article_title">{{ item.videoTitle }}</div>
                  <div class="abbr_article_info">
                    <span>{{ item.videoPublish }}</span>
                    <span style="padding-left: 8px">{{ item.busChannel.channelOwner }}</span>
                  </div>
                </div>
                <img alt :src="item.videoPic" class="abbr_article_img"/>
              </router-link>
            </el-row>
          </el-col>
        </div>
      </el-row>
    </div>
    <div v-else>
      <div>
        <img src="../../assets/article_fill.jpg" alt class="full_a"/>
      </div>
      <div class="card">
        <el-card
          shadow="never"
          style="margin-bottom: 16px;padding: 0px;"
          :body-style="{ padding: '10px' }"
        >
          <h1 class="main_title">{{ videoDetail.videoTitle }}</h1>
          <div class="article_info">
            <span>{{ videoDetail.videoPublish }}</span>
            <span style="padding-left: 8px">&emsp; 作者：{{ videoDetail.busChannel.channelOwner }}</span>
          </div>
          <div class="video-info-mobile">
            <div class="ipv6_info_mob">
              <span>IPv6加速通道：</span>
            </div>
            <el-switch
              v-model="ipv6"
              active-value="0"
              inactive-value="1"
              @change="useIPV6()"
            ></el-switch>
          </div>
          <div style="text-align: center; margin: 20px 0 16px; ">
            <div style="position: relative;">
              <div id="msem"></div>
            </div>
          </div>
          <div class="video_info">视频简介：{{ videoDetail.videoProfile }}</div>
        </el-card>
        <el-card
          shadow="never"
          style="margin-bottom: 16px;"
          class="t"
          :body-style="{ padding: '10px' }"
        >
          <div class="t_title">推荐视频</div>
          <el-row
            v-for="item in list"
            style="width: 100%;margin-top: 16px;"
            :key="item.id"
            :gutter="24"
          >
            <router-link :to="'/video/' + item.videoId">
              <el-col :span="17" style="padding-left: 18px;">
                <div style="display: inline-block;">
                  <div class="video_title_c">{{ item.videoTitle }}</div>
                  <div class="abbr_article_info">
                    <span>{{ item.videoPublish }}</span>
                    <br/>
                    <span>作者：{{ item.busChannel.channelOwner }}</span>
                  </div>
                </div>
              </el-col>
              <el-col :span="7" style="padding-left: 0px;">
                <img alt :src="item.videoPic" class="t_img"/>
              </el-col>
            </router-link>
          </el-row>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
  // import XgPlayer from 'xgplayer-vue';
  // import xgplayer from "xgplayer";
  import Player from 'xgplayer';
  import WebApi from "@/api/WebApi";
  import {mapState} from "vuex";
  import Cookies from "js-cookie";

  export default {
    // components:{ XgPlayer },
    name: "detail",

    data() {
      return {
        ipv6: "1",
        xgplayer: null,
        total: 0,
        videoProfileTemp: "",
        videoDetail: {
          videoId: "",
          videoTitle: "",
          videoProfile: ``,
          videoUrl: "",
          videoClass: "",
          busChannel: {
            channelOwner: ""
          },
          videoPath: "",
          videoPublish: ""
        },
        listTemp: [],
        list: null,
        listQuery: {
          pageNum: 1,
          pageSize: 5,
          videoTitle: ""
        },
        UrlConfig: "",
        rootStyleMp4: {
          backgroundColor: 'rgba(0,0,0,0.87)'
        },
        Player: null
      };
    },
    created() {

      const id = this.$route.params && this.$route.params.id;
      // console.log(id);
      this.fetchData(id);
      this.getRefresh();
    },
    methods: {
      useMp4Play(url, pic_url) {
        console.log("使用mp4播放器");
        this.xgplayer = new Player({
          id: "mse",
          url: url,
          playsinline: true,
          whitelist: [""],
          volume: 0.5,
          lang: "zh-cn",
          playbackRate: [0.5, 1, 1.25, 1.5, 2],
          keyShortcut: "on",
          controls: true,
          fluid: true,
          poster: pic_url
        });
      },
      useIPV6() {
        console.log(this.ipv6)
        if (this.ipv6 === "0") {
          Cookies.set("ipv6", "0")
        } else {
          Cookies.set("ipv6", "1")
        }
        location.reload()

        // if (this.ipv6 === "0"){
        //   this.ipv6 = "1"
        // }
        // else {
        //   this.ipv6 = "0"
        // }
      },

      useMp4PlayMobile(url, pic_url) {
        console.log("使用mp4播放器");
        this.xgplayer = new Player({
          id: "msem",
          url: url,
          playsinline: true,
          whitelist: [""],
          volume: 0.5,
          lang: "zh-cn",
          playbackRate: [0.5, 1, 1.25, 1.5, 2],
          keyShortcut: "on",
          controls: true,
          fluid: true,
          poster: pic_url
        });
      },

      fetchData(id) {
        const ipv6 = Cookies.get("ipv6");
        this.ipv6 = ipv6;
        WebApi.findOneVideo(id)
          .then(data => {
            this.videoDetail = data;
            this.videoDetail.videoPublish = data.videoPublish.split(" ")[0];
            // this.config.id = this.videoDetail.videoId;
            if (ipv6 && ipv6 === "0") {
              this.UrlConfig = "http://ops.hocassian.com:8080/profile/video_matrix/" + this.videoDetail.videoPath;
            } else {
              this.UrlConfig = "/prod-api/profile/video_matrix/" + this.videoDetail.videoPath;
            }
            this.UrlPic = "/prod-api/profile/video_matrix/" + this.videoDetail.videoPic;
            if (this.isMobile) {
              this.useMp4PlayMobile(this.UrlConfig, this.UrlPic)
            } else {
              this.useMp4Play(this.UrlConfig, this.UrlPic)
            }
            // this.config.url = ""

            // console.log(this.videoDetail);
          })
          .catch(err => {
            console.log(err);
          });
      },
      getRefresh() {
        WebApi.findAllVideo(this.listQuery).then(data => {
          this.list = data.rows;
          this.total = data.total;
          Object.keys(this.list).forEach(key => {
            this.list[key].videoPic = "/prod-api/profile/video_matrix/" + this.list[key].videoPic
            this.list[key].videoPublish = this.list[key].videoPublish.substring(0, 10)
          })
        });
      }
    },
    computed: {
      ...mapState("app", ["isMobile"])
    }
  };
</script>

<style lang="scss">
  @media screen and (max-width: 768px) {
    .video_info {
      font-size: 16px;
      color: #656565;
      margin-bottom: 0 !important;
    }
    .card {
      padding: 16px;
    }
    .t {
      padding: 10px;

      .t_title {
        font-size: 18px;
        color: #222;
        border-bottom: 1px solid #e5e9ef;
        padding-bottom: 10px;
      }

      .t_img {
        display: inline-block;
        width: 150%;
        height: 100%;
        border-radius: 4px;
        overflow: hidden;
        vertical-align: middle;
        background-size: cover;
        background-position: 50%;
        background-repeat: no-repeat;
      }
    }
    .abbr_article_word {
      width: 100%;
    }
    .abbr_article_single {
      width: 100%;
    }
    .video_title_c {
      font-size: 12px;
      color: #222;
      line-height: 1.5;
      max-height: 32px;
      overflow: hidden;
    }
    .abbr_article_info {
      margin-top: 8px !important;
      margin-left: 2px;
      line-height: 1.5;
    }
    .full_a {
      width: 100%;
      padding: 0.5rem 0.5rem 0 0.5rem;
    }
  }

  .container_wrap {
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    overflow-x: scroll; /* 1 */
    -webkit-backface-visibility: hidden;
    -webkit-perspective: 1000;
    -webkit-overflow-scrolling: touch; /* 2 */
    text-align: justify; /* 3 */
    &::-webkit-scrollbar {
      display: none;
    }
  }

  .main_container {
    width: 800px;
    min-width: 820px;
    margin-top: 40px;
  }

  .main_title {
    width: 100%;
    /*height: 30px;*/
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 22px;
    font-weight: bold;
    line-height: 30px;
    color: #323232;
    /*text-align: center;*/
  }

  .banner {
    display: block;
    border-radius: 0.6rem;
    width: 1200px;
    height: 150px;
    overflow: hidden;
  }

  .article_info {
    align-self: center;

    margin-right: 20px;
    /*width: 100%;*/
    height: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 14px;
    line-height: 14px;
    color: #a2a2a2;
    /*text-align: center;*/
  }

  .ipv6_info {
    flex: 1;
    text-align: right;
    align-self: center;
    /*margin-left: 300px;*/
    /*width: 100%;*/
    height: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 14px;
    line-height: 14px;
    color: #a2a2a2;
  }

  .ipv6_info_mob {

    align-self: center;
    /*margin-left: 300px;*/
    /*width: 100%;*/
    height: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 14px;
    line-height: 14px;
    color: #a2a2a2;
  }

  .video_detail {
    display: block;
    /*margin: 15px 10px 0 10px;*/
    padding-top: 30px;
    margin-bottom: 30px;
  }

  .block-title {
    display: block;
    margin-top: 70px;
    font-size: 18px;
    color: #222;
    border-bottom: 1px solid #e5e9ef;
    padding-bottom: 10px;
  }

  .abbr_article_single {
    margin-top: 16px;
    width: 310px;
    display: block;
    font-size: 0;
  }

  .abbr_article_word {
    width: 190px;
    line-height: 16px;
    display: inline-block;
    font-size: 12px;
    color: #222;
    margin-right: 12px;
    vertical-align: middle;
  }

  .abbr_article_title {
    max-height: 32px;
    transition: 0.3s;
    text-overflow: ellipsis;
    overflow: hidden;
    /*display: -webkit-box;*/
    -webkit-box-orient: vertical;
  }

  .abbr_article_info {
    font-size: 12px;
    color: #99a2aa;
    letter-spacing: 0;
    margin-top: 4px;
  }

  .abbr_article_img {
    display: inline-block;
    /*width: 68px;*/
    height: 50px;
    border-radius: 4px;
    overflow: hidden;
    vertical-align: middle;
    background-size: cover;
    background-position: 50%;
    background-repeat: no-repeat;
  }

  .video_info {
    white-space: normal;
    font-size: 16px;
    /*color: #99a2aa;*/
    letter-spacing: 0;
    /*margin-bottom: 80px;*/
    margin-left: 5px;
    line-height: 25px;
  }

  .video-info {
    display: flex;
  }

  .video-info-mobile {
    display: flex;
    margin-top: 20px;
  }
</style>
