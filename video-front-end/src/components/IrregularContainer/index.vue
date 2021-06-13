<template>
  <div>
    <el-row
      v-if="!isMobile"
      type="flex"
      justify="center"
      style="margin-bottom: 80px;"
    >
      <el-col v-if="listTemp" :span="7" class="articleL">
        <el-row class="articleL1">
          <router-link :to="'/video/' + listTemp[0][0].videoId">
            <img alt="" :src="listTemp[0][0].pic" class="article1_img" />
            <div class="article1">
              <h5 class="article_title">
                {{ listTemp[0][0].videoTitle }}
              </h5>
              <span class="article_contain_i" v-html="listTemp[0][0].videoInfo">
              </span>
            </div>
          </router-link>
        </el-row>
        <el-row class="articleL2">
          <router-link :to="'/video/' + listTemp[0][1].videoId">
            <div class="article2">
              <h5 class="article_title">
                {{ listTemp[0][1].videoTitle }}
              </h5>
              <span class="article_contain_i" v-html="listTemp[0][1].videoInfo">
              </span>
            </div>
            <img alt="" :src="listTemp[0][1].pic" class="article2_img" />
          </router-link>
        </el-row>
        <el-row class="articleL3">
          <router-link :to="'/video/' + listTemp[0][2].videoId">
            <img alt="" :src="listTemp[0][2].pic" class="article3_img" />
            <div class="article3">
              <h5 class="article_title">
                {{ listTemp[0][2].videoTitle }}
              </h5>
              <span class="article_contain_i" v-html="listTemp[0][2].videoInfo">
              </span>
            </div>
          </router-link>
        </el-row>
      </el-col>
      <el-col v-if="listTemp" :span="7" class="articleC">
        <el-row class="articleC1">
          <router-link :to="'/video/' + listTemp[1][0].videoId">
            <img alt="" :src="listTemp[1][0].pic" class="article4_img" />
            <div class="article4">
              <h5 class="article_title">
                {{ listTemp[1][0].videoTitle }}
              </h5>
              <span class="article_contain_j" v-html="listTemp[1][0].videoInfo">
              </span>
            </div>
          </router-link>
        </el-row>
        <el-row class="articleC2">
          <router-link :to="'/video/' + listTemp[1][1].videoId">
            <div class="article5">
              <h5 class="article_title">
                {{ listTemp[1][1].videoTitle }}
              </h5>
              <span class="article_contain_j" v-html="listTemp[1][1].videoInfo">
              </span>
            </div>
            <img alt="" :src="listTemp[1][1].pic" class="article5_img" />
          </router-link>
        </el-row>
      </el-col>
      <el-col v-if="listTemp" :span="7" class="articleR">
        <el-row class="articleR1">
          <router-link :to="'/video/' + listTemp[2][0].videoId">
            <img alt="" :src="listTemp[2][0].pic" class="article6_img" />
            <div class="article6">
              <h5 class="article_title">
                {{ listTemp[2][0].videoTitle }}
              </h5>
              <span class="article_contain" v-html="listTemp[2][0].videoInfo">
              </span>
            </div>
          </router-link>
        </el-row>
        <el-row class="articleR2">
          <router-link :to="'/video/' + listTemp[1][2].videoId">
            <img alt="" :src="listTemp[1][2].pic" class="article7_img" />
            <div class="article7">
              <h5 class="article_title">
                {{ listTemp[1][2].videoTitle }}
              </h5>
              <span class="article_contain" v-html="listTemp[1][2].videoInfo">
              </span>
            </div>
          </router-link>
        </el-row>
      </el-col>
    </el-row>
    <div v-else class="card">
      <el-card
        shadow="never"
        v-for="(item, idx) in list"
        :key="idx"
        :body-style="{ padding: '0px' }"
        class="card_body"
        @click.native="$router.push(`/video/${item.videoId}`)"
      >
        <img :src="item.pic" class="full" alt="" />
        <div class="article">
          <h5 class="article_title">
            {{ item.videoTitle }}
          </h5>
        </div>
        <span class="article_contain" v-html="item.videoInfo"></span>
      </el-card>
    </div>
  </div>
</template>

<script>
import WebApi from "@/api/WebApi";
import { mapState } from "vuex";

export default {
  name: "IrregularContainer",
  data() {
    return {
      total: "",
      listTemp: null,
      list: [],
      listQuery: {
        pageNum: 1,
        pageSize: 7,
        videoIsHuge: "1"
      }
    };
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
          this.list[key].pic =
            "/prod-api/profile/video_matrix/" + this.list[key].videoPic;
        });
        Object.keys(this.list).forEach(key => {
          this.list[key].videoInfo = this.list[key].videoProfile + "……";
        });
        // console.log(this.list)
        const _list = this.list,
          listTemp = [];
        for (const i in _list) {
          const index = parseInt((i / 3).toString());
          if (listTemp.length <= index) {
            listTemp.push([]);
          }
          if (Object.prototype.hasOwnProperty.call(_list, i)) {
            listTemp[index].push(_list[i]);
          }
        }
        this.listTemp = listTemp;
        // console.log(Boolean(this.listTemp))
        // console.log(this.listTemp)
      });
    }
  },
  computed: {
    ...mapState("app", ["isMobile"])
  }
};
</script>

<style lang="scss" scoped>
.articleL {
  float: left;
  margin-right: 20px;
  width: 570px;
}

.articleL1,
.articleL3,
.articleL2 {
  /*height: 240px;*/
  box-shadow: 0 0 14px #e4e2e2;
  -webkit-box-shadow: 0 0 14px #e4e2e2;
}

.article1_img,
.article3_img {
  display: block;
  float: left;
  margin-right: 20px;
  max-height: 179px;
}

.article1,
.article3 {
  display: block;
  float: left;
  width: 230px;
  padding-right: 20px;
  overflow: hidden;
}

.article_title {
  margin-top: 12px;
  margin-bottom: 2px;
  width: 100%;
  height: 75px;
  line-height: 24px;
  font-size: 17px;
  color: #313131;
  overflow: hidden;
}

.article_contain {
  margin-top: 5px;
  display: block;
  float: left;
  width: 100%;
  height: 64px;
  font-size: 12px;
  line-height: 20px;
  color: #656565;
  overflow: hidden;
}

.article2_img {
  display: block;
  float: right;
  /*margin-left: 20px;*/
  /*max-height: 240px;*/
  max-height: 179px;
}

.article2 {
  display: block;
  float: left;
  width: 230px;
  padding-left: 20px;
  overflow: hidden;
}

.articleL1,
.articleC1,
.articleC2,
.articleR1 {
  margin-top: 20px;
  display: block;
  float: left;
  width: 100%;
  background: #fff;
  overflow: hidden;
}

.articleR2 {
  margin-top: 30px;
  display: block;
  float: left;
  width: 100%;
  background: #fff;
  overflow: hidden;
}

.articleL2,
.articleL3 {
  margin-top: 58px;
  display: block;
  float: left;
  width: 100%;
  background: #fff;
  overflow: hidden;
}

.articleC {
  float: left;
  margin-right: 20px;
  width: 240px;
}

.articleC1 {
  width: 100%;
  /*height: 370px;*/
  box-shadow: 0 0 14px #e4e2e2;
  -webkit-box-shadow: 0 0 14px #e4e2e2;
}

.articleC2 {
  width: 100%;
  height: 322px;
  box-shadow: 0 0 14px #e4e2e2;
  -webkit-box-shadow: 0 0 14px #e4e2e2;
}

.articleR2 {
  width: 100%;
  /*height: 360px;*/
  box-shadow: 0 0 14px #e4e2e2;
  -webkit-box-shadow: 0 0 14px #e4e2e2;
}

.article4_img {
  display: block;
  float: left;
  margin-right: 20px;
  max-width: 240px;
}

.article5_img {
  /*margin: 10px 0 0;*/
  max-width: 240px;
  /*position: absolute;*/
  left: 0;
  bottom: 0;
}

.article6_img {
  display: block;
  float: left;
  width: 320px;
}

.article7_img {
  display: block;
  float: left;
  width: 320px;
  margin-top: -30px;
}

.article4,
.article5 {
  display: block;
  float: left;
  /*width: 220px;*/
  padding: 5px 20px 10px 20px;
  overflow: hidden;
}

.article6,
.article7 {
  display: block;
  float: left;
  /*width: 300px;*/
  padding: 0 20px;
  overflow: hidden;
}

.articleR {
  float: left;
  margin-right: 20px;
  width: 320px;
}

.articleR1 {
  width: 100%;
  /*height: 380px;*/
  box-shadow: 0 0 14px #e4e2e2;
  -webkit-box-shadow: 0 0 14px #e4e2e2;
}

.article_contain_i {
  display: block;
  float: left;
  width: 100%;
  font-size: 13px;
  height: 90px;
  line-height: 22px;
  color: #656565;
  overflow: hidden;
}

.article_contain_j {
  display: block;
  float: left;
  width: 100%;
  height: 83px;
  font-size: 14px;
  line-height: 20px;
  color: #656565;
  overflow: hidden;
}

@media screen and (max-width: 768px) {
  .card {
    padding: 16px;

    .article,
    .article_contain {
      padding: 0 10px 0;
      margin-top: 0 !important;
    }

    .article_contain {
      font-size: 15px;
    }

    .card_body {
      margin-bottom: 16px;
    }
  }
  .full {
    width: 100%;
  }
}
</style>
