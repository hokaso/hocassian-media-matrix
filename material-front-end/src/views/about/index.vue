<template>
  <div>
    <el-row type="flex" justify="center">
      <el-col :md="9" :sm="24">
        <div class="intro">
          <h3>关于我们</h3>
          <div class="sub-area">
            <h4>组织简介</h4>
            <div class="text-area" v-html="about.aboutInfo">
<!--                {{ about.aboutInfo }}-->
            </div>
          </div>
          <div class="sub-area">
            <h4>组织宣言</h4>
            <div class="text-area-center">
              {{ about.aboutDeclaration }}
            </div>
          </div>
          <div class="sub-area">
            <h4>大众平台</h4>
            <el-row class="img-com" type="flex" justify="center">
              <div
                style="padding: 5px"
                v-for="pic in JSON.parse(about.aboutQrcode)"
                :key="pic.name"
              >
                <img
                  :src="'/prod-api/profile/video_matrix/' + pic.url"
                  alt=""
                />
              </div>
            </el-row>
          </div>
          <h3>联系方式</h3>
          <div class="sub-area">
            <h4>{{ about.aboutName }}</h4>
            <div class="text-area-center">
              {{ about.aboutContact }}
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "index",
  computed: {
    ...mapGetters(["about"])
  }
};
</script>

<style scoped lang="scss">
.intro {
  margin-top: 50px;
  margin-bottom: 50px;
  .sub-area {
    .text-area {
      padding-left: 50px;
      padding-right: 50px;
      font-size: 14px;
      color: #656565;
      line-height: 25px;
      white-space: pre-line;
    }
    .text-area-center {
      text-align: center;
      font-size: 14px;
      color: #656565;
      line-height: 25px;
      white-space: pre-line;
    }
    .img-com {
      margin-top: 30px;
      flex-wrap: wrap;
      img {
        width: 150px;
        text-align: center;
      }
    }
  }
  h3 {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
    background: url(../../assets/t-line.png) center 7px no-repeat;
    margin-bottom: 30px;
  }
  h4 {
    font-size: 22px;
    color: #323232;
    text-align: center;
    margin: 25px 0 20px;
  }
}
</style>
