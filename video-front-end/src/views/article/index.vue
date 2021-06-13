<template>
  <div class="article_list">
    <div v-if="!isMobile">
      <swiper-vertical />
      <div class="filter-container">
        <el-input
          class="filter-item"
          placeholder="请输入内容"
          prefix-icon="el-icon-search"
          v-model="listQuery.keywords"
        >
        </el-input>
        <el-button
          class="filter-item-button"
          type="primary"
          icon="el-icon-search"
          @click="getRefresh"
        >
          搜索
        </el-button>
      </div>
      <el-row type="flex" justify="center">
        <el-col v-if="list" :span="12" class="article_container">
          <el-row v-for="item in list" class="article_single" :key="item.id">
            <router-link :to="'/article/' + item.id">
              <div class="article_word">
                <div class="article_title">
                  {{ item.title }}
                </div>
                <div class="article_info">
                  <span>{{ item.createAt }}</span>
                  <span style="padding-left: 8px"
                    >&emsp; 作者：{{ item.author }}</span
                  >
                </div>
                <div class="article_profile" v-html="item.article"></div>
              </div>
              <img alt="" :src="item.pic" class="article_img" />
            </router-link>
          </el-row>
        </el-col>
      </el-row>
      <pagination
        v-show="total || total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :size.sync="listQuery.size"
        @pagination="getRefresh"
      />
    </div>
    <div v-else>
      <my-swiper />
      <div class="search">
        <el-input
          class="search_input"
          placeholder="请输入内容"
          prefix-icon="el-icon-search"
          v-model="listQuery.keywords"
        >
        </el-input>
        <el-button
          class="search_btn"
          type="primary"
          icon="el-icon-search"
          @click="getRefresh"
        >
          搜索
        </el-button>
      </div>
      <div class="card">
        <el-card
          shadow="never"
          v-for="(item, idx) in list"
          :key="idx"
          :body-style="{ padding: '0px' }"
          class="card_body"
          @click.native="$router.push(`/article/${item.id}`)"
        >
          <img :src="item.pic" class="full" />
          <div class="article">
            <h5 class="article_title">
              {{ item.title }}
            </h5>
          </div>
          <div class="article_info">
            <span> {{ item.createAt }}</span>
            <span style="padding-left: 8px"
              >&emsp; 作者：{{ item.author }}</span
            >
          </div>
          <div class="article_contain" v-html="item.article"></div>
        </el-card>
      </div>
      <pagination
        v-show="total || total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :size.sync="listQuery.size"
        @pagination="getRefresh"
        class="pagination"
        layout="total,prev, pager, next,jumper"
      />
    </div>
  </div>
</template>

<script>
import SwiperVertical from "@/components/SwiperVertical";
import MySwiper from "@/components/Swiper";
import WebApi from "@/api/WebApi";
import Pagination from "@/components/Pagination"; // secondary package based on el-pagination
import { mapState } from "vuex";
export default {
  name: "Article",
  components: { SwiperVertical, Pagination, MySwiper },
  data() {
    return {
      total: 0,
      index: "",
      createAt: "",
      listTemp: [],
      list: null,
      listQuery: {
        page: 1,
        size: 8,
        keywords: "",
        direction: "DESC"
      }
    };
  },
  created() {
    this.getRefresh();
  },
  methods: {
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
    },
    handleClick() {
      console.log("成立");
    }
  },
  computed: {
    ...mapState("app", ["isMobile"])
  }
};
</script>

<style lang="scss">
.article_list {
  @media screen and (min-width: 768px) {
    .article_single {
      background: rgba(241, 255, 248, 0.6);
      /*float: left;*/
      display: block;
      margin-bottom: 30px;
      border-radius: 0.6rem;
      /*z-index: 3;*/
      box-shadow: 0 0.06rem 0.12rem rgba(0, 0, 0, 0.1),
        0 0.2rem 0.6rem rgba(0, 0, 0, 0.1);
      /*transition-duration: 0.3s;*/
      overflow: hidden;
    }
    .article_title {
      padding-top: 25px;
      padding-left: 30px;
      width: 658px;
      overflow: hidden;
      font-size: 16px;
      color: #323232;
    }
    .article_word {
      float: left;
      width: 658px;
      /*height: 120px;*/
      overflow: hidden;
      margin-right: 30px;
    }
    .article_info {
      clear: both;
      display: block;
      margin-top: 15px;
      margin-left: 30px;
      line-height: 12px;
      font-size: 12px;
      color: #a2a2a2;
    }
    .article_profile {
      float: left;
      /*margin-top: 5px;*/
      padding-left: 30px;
      width: 658px;
      overflow: hidden;
      font-size: 14px;
      color: #656565;
      line-height: 24px;
    }
    .article_img {
      float: left;
      width: 212px;
      overflow: hidden;
    }
    .article_container {
      width: 900px;
    }


  }

  @media screen and (max-width: 768px) {
    .el-pagination {
      white-space: inherit !important;
    }
    .card {
      padding: 16px;
      .article,
      .article_contain {
        padding: 0 10px 0;
      }
      .article_contain {
        font-size: 12px;
        line-height: 20px;
        color: #656565;
      }
      .card_body {
        margin-bottom: 16px;
      }
      .article_title {
        margin-top: 0.6rem;
        margin-bottom: 0.3rem;
        width: 100%;
        line-height: 24px;
        font-size: 18px;
        color: #313131;
        overflow: hidden;
      }
      .article_info {
        font-size: 12px;
        color: #a2a2a2;
        /*text-align: center;*/
        margin-left: 0.3rem;
      }
    }
    .search {
      display: flex;
      justify-content: space-around;
      margin-top: 16px;
      box-sizing: border-box;
      padding: 0 12px;
      .search_input {
        width: 60%;
      }
      .search_btn {
        width: 30%;
      }
    }
    .full {
      width: 100%;
    }
  }
}
</style>
