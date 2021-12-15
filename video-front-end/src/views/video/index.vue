<template>
  <div class="video_list">
    <div v-if="!isMobile">
      <swiper-vertical />
      <div class="filter-container">
        <el-input
          class="filter-item"
          placeholder="请输入内容"
          prefix-icon="el-icon-search"
          v-model="listQuery.videoTitle"
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
      <el-row
        :gutter="20"
        v-for="(row, i) in listTemp"
        :key="i"
        type="flex"
        class="row-bg"
        justify="center"
        style="padding-bottom:50px;"
      >
        <el-col
          :span="3"
          :id="'T_' + (i * 3 + j)"
          v-for="(cell, j) in row"
          :key="cell.id"
          :offset="j > 0 ? 1 : 0"
        >
          <router-link :to="'/video/' + cell.videoId">
            <el-card :body-style="{ padding: '0px' }">
              <img :src="cell.videoPic" class="image" alt="" />
              <div class="video_title_a">
                <span>{{ cell.videoTitle }}</span>
                <div class="bottom clearfix">
                  <!--                <span class="info">{{ cell.videoProfile }}</span>-->
                </div>
              </div>
            </el-card>
          </router-link>
        </el-col>
      </el-row>
      <pagination
        v-show="total || total > 0"
        :total="total"
        :page.sync="listQuery.pageNum"
        :limit.sync="listQuery.pageSize"
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
          v-model="listQuery.videoTitle"
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
      <el-row :gutter="24" style="margin-top: 16px;padding: 16px; margin-bottom: -50px;">
        <el-col
          v-for="(item, idx) in list"
          :key="idx"
          :span="12"
          style="min-height: 5rem;"
        >
          <el-card :body-style="{ padding: '0px' }" @click.native="$router.push(`/video/${item.videoId}`)">
            <img :src="item.videoPic" style="width: 100%;" alt="" />
            <div class="video_title_a">
              <span>{{ item.videoTitle }}</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
      <pagination
        v-show="total || total > 0"
        :total="total"
        :page.sync="listQuery.pageNum"
        :limit.sync="listQuery.pageSize"
        @pagination="getRefresh"
        layout="total,prev, next,jumper"
      />
    </div>
  </div>
</template>

<script>
import SwiperVertical from "@/components/SwiperVertical";
import WebApi from "@/api/WebApi";
import MySwiper from "@/components/Swiper";
import Pagination from "@/components/Pagination"; // secondary package based on el-pagination
import { mapState } from "vuex";
export default {
  name: "Video",
  components: { MySwiper, SwiperVertical, Pagination },
  data() {
    return {
      total: 0,
      index: "",
      createAt: "",
      listTemp: [],
      list: null,
      listQuery: {
        pageNum: 1,
        pageSize: 32,
        videoTitle: ""
      }
    };
  },
  created() {
    this.getRefresh();
  },
  methods: {
    getRefresh() {
      WebApi.findAllVideo(this.listQuery).then(data => {
        console.log(data);
        this.list = data.rows;
        this.total = data.total;
        Object.keys(this.list).forEach(key =>{
            this.list[key].videoPic = "/prod-api/profile/video_matrix/" + this.list[key].videoPic
        });
        // console.log(this.list)
        const _list = this.list,
          listTemp = [],
          sectionCount = 4;
        for (const i in _list) {
          const index = parseInt((i / sectionCount).toString());
          if (listTemp.length <= index) {
            listTemp.push([]);
          }
          listTemp[index].push(_list[i]);
        }
        this.listTemp = listTemp;
      });
    }
  },
  computed: {
    ...mapState("app", ["isMobile"])
  }
};
</script>

<style lang="scss">
.video_list {
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
        margin-top: 20px;
        margin-bottom: 10px;
        width: 100%;
        line-height: 24px;
        font-size: 18px;
        color: #313131;
        overflow: hidden;
      }
      .article_info {
        font-size: 12px;
        color: #a2a2a2;
        text-align: center;
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
    .video_title_a {
      padding: 11px;
      font-size: 14px;
      height: 77px;
      line-height: 1.5;
      overflow: hidden;
    }
  }

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
    .video_title_a {
      padding: 16px;
      font-size: 16px;
      line-height: 23px;
    }
  }
}
</style>
