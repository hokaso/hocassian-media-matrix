<template>
  <div class="article_detail">
    <div v-if="!isMobile">
      <div class="banner">
        <img src="../../assets/article_fill.jpg" alt="" />
      </div>
      <el-row :gutter="20">
        <el-col :span="9" :offset="5" class="main_container">
          <h1 class="main_title_c">{{ temp.title }}</h1>
          <div class="article_info">
            <span>{{ temp.createAt }}</span>
            <span style="padding-left: 8px"
              >&emsp; 作者：{{ temp.author }}</span
            >
          </div>
          <div class="article_detail" v-html="temp.article"></div>
        </el-col>
        <el-col :span="4" style="margin-left: 30px">
          <div class="block-title">
            推荐文章
          </div>
          <el-row
            v-for="item in list"
            class="abbr_article_single"
            :key="item.id"
          >
            <router-link :to="'/article/' + item.id">
              <div class="abbr_article_word">
                <div class="abbr_article_title">
                  {{ item.title }}
                </div>
                <div class="abbr_article_info">
                  <span>{{ item.createAt }}</span>
                  <span style="padding-left: 8px"
                    >&emsp; 作者：{{ item.author }}</span
                  >
                </div>
              </div>
              <img alt="" :src="item.pic" class="abbr_article_img" />
            </router-link>
          </el-row>
        </el-col>
      </el-row>
    </div>
    <div v-else>
      <div>
        <img src="../../assets/article_fill.jpg" alt="" class="full" />
      </div>
      <div class="card">
        <el-card shadow="never" style="margin-bottom: 16px;padding: 10px;">
          <h1 class="main_title_c">{{ temp.title }}</h1>
          <div class="article_info">
            <span>{{ temp.createAt }}</span>
            <span style="padding-left: 8px"
              >&emsp; 作者：{{ temp.author }}</span
            >
          </div>
          <div class="article_detail " v-html="temp.article"></div>
        </el-card>
        <el-card shadow="never" style="margin-bottom: 16px;" class="t">
          <div class="t_title">
            推荐文章
          </div>
          <el-row
            v-for="item in list"
            class="abbr_article_single"
            style="width: 100%"
            :key="item.id"
            :gutter="24"
          >
            <router-link :to="'/article/' + item.id">
              <el-col :span="18">
                <div class="abbr_article_word">
                  <div class="abbr_article_title">
                    {{ item.title }}
                  </div>
                  <div class="abbr_article_info">
                    <span>{{ item.createAt }}</span>
                    <span style="padding-left: 8px"
                      >&emsp; 作者：{{ item.author }}</span
                    >
                  </div>
                </div>
              </el-col>
              <el-col :span="6">
                <img alt="" :src="item.pic" class="abbr_article_img" />
              </el-col>
            </router-link>
          </el-row>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import WebApi from "@/api/WebApi";
import { mapState } from "vuex";
export default {
  name: "detail",

  data() {
    return {
      total: 0,
      temp: {
        readings: "",
        author: "",
        article: ``,
        title: "",
        status: "",
        createAt: "",
        isDel: ""
      },
      listTemp: [],
      list: null,
      listQuery: {
        page: 1,
        size: 5,
        keywords: "",
        direction: "DESC"
      }
    };
  },
  created() {
    const id = this.$route.params && this.$route.params.id;
    this.fetchData(id);
    this.getRefresh();
  },
  methods: {
    fetchData(id) {
      WebApi.findOneArticle(id)
        .then(data => {
          this.temp = data;
        })
        .catch(err => {
          console.log(err);
        });
    },
    getRefresh() {
      WebApi.findSomeArticle(this.listQuery).then(data => {
        this.list = data.data;
        this.total = this.list.length;
        Object.keys(this.list).forEach(
          key =>
            (this.list[key].pic =
              "/file/" + this.list[key].pic)
        );
        Object.keys(this.list).forEach(
          key => (this.list[key].article = this.list[key].article + "……")
        );
      });
    }
  },
  computed: {
    ...mapState("app", ["isMobile"])
  }
};
</script>

<style lang="scss">
.article_detail {
  @media screen and (max-width: 768px) {
    .card {
      padding: 10px;
      .article,
      .article_contain {
        padding: 0 10px 1px;
      }
      .card_body {
        margin-bottom: 16px;
      }
    }
    .abbr_article_word{
      width: 5.5rem !important;
    }
    .article_detail {
      padding-bottom: 0 !important;
      section {
        img {
          width: auto;
          height: auto;
          max-width: 100%;
          max-height: 100%;
        }
      }
      p {
        img {
          width: auto;
          height: auto;
          max-width: 100%;
          max-height: 100%;
        }
      }
    }
    .t {
      padding: 10px;
      .t_title {
        font-size: 18px;
        color: #222;
        border-bottom: 1px solid #e5e9ef;
        padding-bottom: 10px;
      }
    }

    .full {
      width: 100%;
      padding: 0.5rem 0.5rem 0 0.5rem;
    }
    .abbr_article_img{
      /*margin-left: 16px;*/
    }
  }

  .main_container {
    margin-top: 60px;
  }
  .main_title_c {
    width: 100%;
    font-size: 22px;
    font-weight: bold;
    line-height: 30px;
    color: #323232;
    text-align: center;
  }
  .banner {
    display: block;
    margin: 60px auto 0;
    border-radius: 0.6rem;
    width: 1200px;
    height: 150px;
    overflow: hidden;
  }
  .article_info {
    float: left;
    /*margin-bottom: 20px;*/
    width: 100%;
    height: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 14px;
    line-height: 14px;
    color: #a2a2a2;
    text-align: center;
  }
  .article_detail {
    display: block;
    float: left;
    /*margin: 15px 10px 0 10px;*/
    width: 100%;
    font-size: 16px;
    line-height: 28px;
    color: #656565;
    padding-bottom: 50px;
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
    width: 230px;
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
    display: -webkit-box;
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
    // margin-left: 16px;
    overflow: hidden;
    vertical-align: middle;
    background-size: cover;
    background-position: 50%;
    background-repeat: no-repeat;
  }
}
</style>
