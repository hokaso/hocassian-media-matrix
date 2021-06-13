<template>
  <el-row style="margin: 24px 24px;">
    <el-col :sm="24" :md="{ span: '16', offset: '4' }">
      <el-card>
        <el-row :gutter="16">
          <el-col :sm="24" :md="8" style="margin-bottom: 16px;">
            <h2 class="title" style="line-height: 1.5;">
              {{ video.videoTitle }}
            </h2>
            <div class="info">
              <span style="margin-right: 16px;">{{ video.createAt }}</span>
              <span>{{ video.videoAuthor }}</span>
            </div>
            <div class="introduction">
              {{ video.videoProfile }}
            </div>
          </el-col>
          <el-col :sm="24" :md="16">
            <div style="position: relative; padding: 28.25% 45%;">
              <iframe
                :src="videoUrl"
                scrolling="no"
                border="0"
                frameborder="no"
                framespacing="0"
                allowfullscreen="true"
                sandbox="allow-top-navigation allow-same-origin allow-forms allow-scripts"
                style="position: absolute; width: 100%; height: 100%; left: 0; top: 0;"
              >
              </iframe>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import WebApi from "@/api/WebApi";
import { mapState } from "vuex";
export default {
  data() {
    return {
      video: {},
      videoUrl: ""
    };
  },
  mounted() {
    this.fetch();
  },
  methods: {
    async fetch() {
      let data = await WebApi.findOneVideo("515610152276340736");
      console.log(data);
      this.video = data;
      this.videoUrl =
        "https://player.bilibili.com/player.html?aid=" +
        data.videoUrl +
        "&page=1&high_quality=1&danmaku=0&as_wide=1";
      // console.log(this.videoUrl)
      // this.videoUrl = 'https://player.bilibili.com/player.html?cid=145147963&aid=84267566&page=1&as_wide=1&high_quality=1&danmaku=0'
    }
  },
  computed: {
    ...mapState("app", ["isMobile"])
  }
};
</script>

<style lang="scss" scoped>
.info {
  // text-align: center;
  font-size: 18px;
  color: #656565;
}
.introduction {
  font-size: 14px;
  color: #aaa;
  line-height: 1.5;
  margin-top: 24px;
}
</style>
