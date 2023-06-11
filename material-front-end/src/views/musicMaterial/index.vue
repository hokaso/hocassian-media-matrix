<template>
  <div class="mb-20">
    <PhotoScroll :imgList="imgList" />
    <div class="music-search__wrap">
      <search
        class="search"
        placeholder="搜索音频素材"
        placeholderSearch="搜索音频"
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
    <SongCard
      :list="musicList"
      :total="page.total"
      :pageSize="page.size"
      :pageShow="pageShow"
      :showAccompany="queryParams.audioType === '1'"
      :showCopyRight="getToken() !== '' && getToken() !== undefined"
      @handleCurrentChange="handleCurrentChange"
      @getPlayListIndex="getPlayListIndex" />
    <!--      :playList="initMusicList.length > 0 ? initMusicList : musicList"-->
    <AudioPlay
      v-if="canPlay"
      :playList="musicList"
      :currentIndex.sync="currentIndex"
      :isAccompany="isAccompany" />
  </div>
</template>

<script>
import { findAllSwiper, musicList, musicPic, memberMusicList, musicKeyword } from '@/api/WebApi';
import Search from '@/components/Search';
import PhotoScroll from './PhotoScroll.vue';
import SongCard from './SongCard.vue';
import ParamsFilter from '@/components/ParamsFilter/index.vue';
import KeywordShow from '@/components/KeywordShow/index.vue';
import { getToken } from '@/utils/auth';
import AudioPlay from './AudioPlay.vue';

export default {
  components: { Search, PhotoScroll, SongCard, ParamsFilter, KeywordShow, AudioPlay },
  data() {
    return {
      imgList: [],
      musicList: [],
      page: {
        num: 1,
        size: 36,
        total: 0
      },
      inputValue: '',
      keyWordList: [],
      currentIndex: 0,
      canPlay: false,
      paramsList: {
        audioType: [
          { label: '全部', value: '' },
          { label: '纯音乐', value: 0 },
          { label: '歌曲', value: 1 }
        ],
        isCopyright: [
          { label: '全部', value: '' },
          { label: '有版权', value: 0 },
          { label: '无版权', value: 1 }
        ],
      },
      translation: {
        audioType: '音频类型',
        isCopyright: '素材版权'
      },
      queryParams: {
        audioType: '',
        isCopyright: '',
        isShow: '0',
        audioStatus: '',
      },
      isClick: false,
      initMusicList: [], // 缓存musicList
      pageShow: true,
      isAccompany: false, // 是否为伴奏
    };
  },
  mounted() {
    this.getImgList();
    this.getKeyword();
    this.judgeSearch(true);
  },
  methods: {
    getToken,
    judgeSearch(isResetPage = false) {
      const token = this.getToken();
      if (token !== '' && token !== undefined) {
        this.getMemberMusicList(isResetPage);
      } else {
        this.getMusicList(isResetPage);
      }
    },
    // 获取banner
    async getImgList() {
      const { rows } = await findAllSwiper({
        pageNum: 1,
        pageSize: 10
      });
      this.imgList = rows.map((item, index) => ({
        ...item,
        url: process.env.VUE_APP_BASE_API + `/profile/video_matrix/${item.swiperPic}`,
        activeIndex: index + 1
      }));
    },
    resetPageShow() {
      this.pageShow = false;
      this.$nextTick(() => {
        this.pageShow = true;
      });
    },
    /**
     * 非会员
     */
    // 获取音频素材
    async getMusicList(isResetPage = false) {
      if (isResetPage) {
        this.page.num = 1;
        this.resetPageShow();
      }
      const picArr = await this.getMusicPic();
      const len = picArr.length;
      let i = 0;
      const { rows, total } = await musicList({
        audioName: this.inputValue,
        pageNum: this.page.num,
        pageSize: this.page.size,
      });
      this.page.total = total;
      this.musicList = rows.map(item => ({
        ...item,
        picUrl: process.env.VUE_APP_BASE_API + `/profile/image/${picArr[`${i > len ? i = 0 : i++ }`]}_color_mini.jpg`,
        canShow: false
      }));
    },
    async getMusicPic() {
      const { data } = await musicPic();
      return data;
    },
    // 获取关键字
    async getKeyword() {
      const { data } = await musicKeyword();
      this.keyWordList = data;
    },

    /**
     * 会员
     */
    // 会员获取音频素材
    async getMemberMusicList(isResetPage = false) {
      if (isResetPage) {
        this.page.num = 1;
        this.resetPageShow();
      }
      const picArr = await this.getMusicPic();
      const len = picArr.length;
      let i = 0;
      const { rows, total } = await memberMusicList({
        audioName: this.inputValue,
        pageNum: this.page.num,
        pageSize: this.page.size,
        ...this.queryParams,
      });
      this.page.total = total;
      this.musicList = rows.map(item => ({
        ...item,
        picUrl: process.env.VUE_APP_BASE_API + `/profile/image/${picArr[`${i > len ? i = 0 : i++ }`]}_color_mini.jpg`,
        canShow: false
      }));
    },

    handleCurrentChange(currentPage) {
      this.page.num = currentPage;
      this.isClick = false; // 重置点击状态
      this.judgeSearch();
    },
    getInputValue(value) {
      this.inputValue = value;
      this.judgeSearch(true);
    },
    /**
     * 获取搜索条件
     * 纯音乐 - audioStatus 2
     * 歌曲 - audioStatus 0
     * 全部 - audioStatus ''
     */
    getParams(key, value) {
      this.queryParams[key] = value.toString();
      if (this.queryParams.audioType === '1') {
        this.queryParams.audioStatus = '0';
      } else if (this.queryParams.audioType === '0') {
        this.queryParams.audioStatus = '2';
      } else {
        this.queryParams.audioStatus = '';
      }
      this.isClick = false; // 重置点击状态
      this.getMemberMusicList(true);
    },
    /**
     * @param index 当前索引
     * @param isAccompany 是否伴奏
     */
    getPlayListIndex(index, isAccompany) {
      this.isAccompany = isAccompany;
      this.isClick = true;
      this.canPlay = false;
      this.currentIndex = index;
      this.$nextTick(() => {
        this.canPlay = true;
      });
    },
  },
  watch: {
    isClick: {
      handler(v) {
        // 已点击 -> 缓存歌单等于当前歌单
        if(v) {
          this.initMusicList = JSON.parse(JSON.stringify(this.musicList));
        }
      },
      deep: true,
      immediate: true
    }
  },
}
</script>

<style lang="scss">
.music-search__wrap {
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
  width: 1260px;
  margin: 0 auto;
  padding: 20px 20px 0 20px;
}
.mb-20 {
  margin-bottom: 20px;
}
</style>
