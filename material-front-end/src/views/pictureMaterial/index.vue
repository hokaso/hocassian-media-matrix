<template>
  <div class="pic-material__wrap">
    <Banner />
    <div class="pic-material__search">
      <Search
        class="search"
        placeholder="搜索图片素材"
        placeholderSearch="搜索图片"
        :value.sync="inputValue"
        @search="judgeSearch(true)" />
    </div>
    <KeywordShow
      :list="keyWordList"
      class="keyword__container"
      @search="getInputValue" />
    <ParamsFilter
      v-show="getToken() !== '' && getToken() !== undefined"
      :params="paramsList"
      :query-params="queryParams"
      :translation="translation"
      class="params-filter__container"
      @search="getParams" />
    <ImageCard
      :list="list"
      :urlList="urlList"
      :showCopyRight="getToken() !== '' && getToken() !== undefined"
      class="image-card__container" />
  </div>
</template>

<script>
import Banner from '@/components/Banner/index.vue';
import { imageList, imageKeyword, memberImageList } from '@/api/pic';
import ParamsFilter from '@/components/ParamsFilter/index.vue';
import KeywordShow from '@/components/KeywordShow/index.vue';
import { getToken } from '@/utils/auth';
import Search from '@/components/Search';
import ImageCard from './ImageCard.vue';

export default {
  components: { Search, Banner, KeywordShow, ParamsFilter, ImageCard },
  data() {
    return {
      list: [],
      keyWordList: [],
      paramsList: {
        imageType: [
          { label: '全部', value: '' },
          { label: '高质图片', value: 0 },
          { label: '普通图片', value: 1 }
        ],
        isCopyright: [
          { label: '全部', value: '' },
          { label: '有版权', value: 0 },
          { label: '无版权', value: 1 }
        ],
      },
      translation: {
        imageType: '图片类型',
        isCopyright: '素材版权'
      },
      queryParams: {
        imageType: '',
        isCopyright: '',
        isShow: '0',
        imageStatus: '0',
      },
      inputValue: '',
      pageParams: {
        page: 1,
        size: 20
      },
      noMore: false,
      urlList: [],
    };
  },
  mounted() {
    window.addEventListener('scroll', this.getSrcollTop);
    this.getImageKeywords();
    this.judgeSearch();
  },
  methods: {
    getToken,
    judgeSearch(isResetPage = false) {
      const token = this.getToken();
      if (token !== '' && token !== undefined) {
        this.getMemberImageList(isResetPage);
      } else {
        this.getImageList(isResetPage);
      }
    },
    getSrcollTop() {
      if(this.noMore) return;
      const documentScrollHeight = document.documentElement.scrollTop;
      const scrollHeight = document.body.scrollHeight;
      const windowHeight = document.documentElement.clientHeight;
      const scroll = documentScrollHeight + windowHeight - scrollHeight;
      if (scroll > -120) {
        this.$nextTick(() => {
          this.pageParams.page++;
          this.judgeSearch();
        })
      }
    },
    async getImageList(isResetPage = false) {
      if (isResetPage) {
        this.pageParams.page = 1;
        this.list = [];
        this.urlList = [];
      }
      const { rows, total } = await imageList({
        imageTag: this.inputValue,
        pageNum: this.pageParams.page,
        pageSize: this.pageParams.size,
      });
      const arr = rows.map((item) => {
        item.url = process.env.VUE_APP_BASE_API + `/profile/image/${item.imagePath}_mini.jpg`;
        item.width = item.imageSize.split('*')[0]/10;
        item.height = item.imageSize.split('*')[1]/10;
        this.urlList.push(process.env.VUE_APP_BASE_API + `/profile/image/${item.imagePath}.jpg`);
        return {...item};
      });
      this.list.push(...arr);
      if (this.pageParams.page * this.pageParams.size > total) {
        this.noMore = true;
      }
    },
    async getMemberImageList(isResetPage = false) {
      if (isResetPage) {
        this.pageParams.page = 1;
        this.list = [];
        this.urlList = [];
      }
      const { rows, total } = await memberImageList({
        pageNum: this.pageParams.page,
        pageSize: this.pageParams.size,
        isShow: '0',
        imageStatus: '0',
        // 选填
        imageTag: this.inputValue,
        ...this.queryParams,
      });
      const arr = rows.map((item) => {
        item.url = process.env.VUE_APP_BASE_API + `/profile/image/${item.imagePath}_mini.jpg`;
        item.width = item.imageSize.split('*')[0]/10;
        item.height = item.imageSize.split('*')[1]/10;
        this.urlList.push(process.env.VUE_APP_BASE_API + `/profile/image/${item.imagePath}.jpg`);
        return {...item};
      });
      this.list.push(...arr);
      if (this.pageParams.page * this.pageParams.size > total) {
        this.noMore = true;
      }
    },
    async getImageKeywords() {
      const { data } = await imageKeyword();
      this.keyWordList = data;
    },
    getInputValue(value) {
      this.inputValue = value;
      this.judgeSearch(true);
    },
    /**
     * 获取搜索条件
     */
    getParams(key, value) {
      this.queryParams[key] = value.toString();
      this.getMemberImageList(true);
    },
  },
}
</script>

<style lang="scss">
.pic-material__wrap {
  .pic-material__search {
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 30px 0 20px 0;
    .search {
      font-size: 16px;
      width: 1000px;
    }
  }
  .keyword__container {
    width: 1200px;
    margin: 0 auto 30px auto;
  }
  .params-filter__container {
    padding: 20px 70px;
    margin: 0;
    width: 100%;
  }
  .image-card__container {
    padding: 20px 50px;
    margin-bottom: 50px;
  }
}
</style>
