<template>
  <div class="clip__wrap">
    <my-swiper />
    <div class="clip-search__wrap">
      <search
        class="search"
        :value.sync="inputValue"
        @search="judgeSearch(true)" />
    </div>
    <keyword-show
      :list="keyWordList"
      class="keyword__container"
      @search="getInputValue" />
    <params-filter
      v-show="getToken() !== '' && getToken() !== undefined"
      :params="paramsList"
      :query-params="queryParams"
      :translation="translation"
      class="params-filter__container"
      @search="getParams" />
    <pic-video
      :list="list"
      :width="300"
      :total="total"
      :pageSize="page.size"
      :rowIndex="4"
      :needPage="true"
      :showVideoInfo="true"
      :showCopyRight="getToken() !== '' && getToken() !== undefined"
      class="clip-video__container"
      @handleCurrentChange="handleCurrentChange" />
  </div>
</template>

<script>
  import MySwiper from "@/components/Swiper";
  import Search from '@/components/Search';
  import PicVideo from '@/components/PicVideo';
  import { findAllClip, keyword, queryMemberVideoList } from '@/api/WebApi';
  import KeywordShow from './KeywordShow.vue';
  import ParamsFilter from '@/components/ParamsFilter/index.vue';
  import { getToken } from '@/utils/auth'

  export default {
    components: { MySwiper, Search, PicVideo, KeywordShow, ParamsFilter },
    name: 'index',
    data() {
      return {
        inputValue: '',
        total: 0,
        page: {
          num: 1,
          size: 12
        },
        list: [],
        keyWordList: [],
        paramsList: {
          materialType: [
            { label: '全部', value: '' },
            { label: '高质素材', value: 0 },
            { label: '普通素材', value: 1 }
          ],
          isCopyright: [
            { label: '全部', value: '' },
            { label: '有版权', value: 0 },
            { label: '无版权', value: 1 }
          ],
          orderbyMark: [
            { label: '时间排序', value: 1 },
            { label: '分数排序', value: 0 }
          ],
        },
        translation: {
          materialType: '素材类型',
          isCopyright: '素材版权',
          orderbyMark: '时间排序'
        },
        queryParams: {
          materialType: '',
          isCopyright: '',
          orderbyMark: '1',
          isShow: '0',
          materialStatus: '0',
        }
      };
    },
    created() {
      this.judgeSearch();
      this.getKeyword();
    },
     methods: {
      getToken,
      judgeSearch(isResetPage = false) {
        const token = this.getToken();
        if (token !== '' && token !== undefined) {
          this.getMemberList(isResetPage);
        } else {
          this.getList(isResetPage);
        }
      },
      /**
       * 不需要登录获取的视频列表
       */
      getList(isResetPage = false) {
        if (isResetPage) {
          this.page.num = 1;
        }
        findAllClip({
          materialTag: this.inputValue,
          pageNum: this.page.num,
          pageSize: this.page.size
        }).then(data => {
          this.list = data.rows;
          this.total = data.total;
          Object.keys(this.list).forEach(
            key =>{
              this.list[key].materialPicPath =
                "/prod-api/profile/video_clip/clip_slot/" + this.list[key].materialPath + "_cover.jpg";
              this.list[key].videoPath = "/prod-api/profile/video_clip/preview/" + this.list[key].materialPath + ".mp4";
              this.list[key].isShow = false;
            }
          );
        });
      },
      /**
       * 需要登录才可获取
       */
      async getMemberList(isResetPage = false) {
        if (isResetPage) {
          this.page.num = 1;
        }
        queryMemberVideoList({
          materialTag: this.inputValue,
          ...this.queryParams,
          pageNum: this.page.num,
          pageSize: this.page.size
        }).then(data => {
          this.list = data.rows;
          this.total = data.total;
          Object.keys(this.list).forEach(
            key =>{
              this.list[key].materialPicPath =
                "/prod-api/profile/video_clip/clip_slot/" + this.list[key].materialPath + "_cover.jpg";
              this.list[key].videoPath = "/prod-api/profile/video_clip/preview/" + this.list[key].materialPath + ".mp4";
              this.list[key].isShow = false;
            }
          );
        });
      },
      /**
       * 获取搜索条件
       */
      getParams(key, value) {
        this.queryParams[key] = value.toString();
        this.getMemberList(true);
      },
      handleCurrentChange(current) {
        this.page.num = current;
        this.judgeSearch();
      },
      /**
       * 获取视频素材关键字
       */
      async getKeyword() {
        const { data } = await keyword();
        this.keyWordList = data;
      },
      getInputValue(value) {
        this.inputValue = value;
        this.judgeSearch(true);
      }
    },
  }
</script>

<style lang="scss">
.clip__wrap {
  width: 100%;
  height: 100%;
  .clip-search__wrap {
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 50px auto 20px auto;
    .search {
      font-size: 16px;
      width: 1000px;
    }
  }
  .params-filter__container {
    width: 1340px;
    margin: 50px auto 30px auto;
    padding: 0 20px;
  }
  .keyword__container {
    width: 1200px;
    margin: 0 auto 30px auto;
  }
  .clip-video__container {
    margin: 0 auto;
  }
}
</style>
