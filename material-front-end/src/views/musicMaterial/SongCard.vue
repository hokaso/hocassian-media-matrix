<template>
  <div>
    <el-card
      shadow="never"
      class="card__wrap">
      <h2 class="card__name ml-30">{{ name }}</h2>
      <div class="card__container">
        <div
          v-for="(item, index) in list"
          :key="item.id"
          class="card-image__block"
          :style="{
            'height': height + 'px',
            'width': width + 'px'
          }">
          <div
            class="card-image__parent"
            @mouseover="showPlayIcon(index)"
            @mouseleave="hidePlayIcon(index)">
            <div
              :style="{
                'height': height + 'px',
                'width': width + 'px',
                'background-image': `url(${item.picUrl})`,
                'filter': 'blur(1px)',
              }"
              class="image">
            </div>
            <div
              :class="{'actived': !item.canShow}"
              class="card-image__info">
              <p class="name">{{ item.audioName }}</p>
              <p class="author">{{ item.audioAuthor }}</p>
            </div>
            <img
              v-show="showCopyRight"
              class="card-image__icon"
              :src="item.isCopyright === '0' ? require('@/assets/images/copyright.png') : require('@/assets/images/no-copyright.png')"  alt=""/>
            <div
              class="play-icon__container"
              :class="{'actived': item.canShow}">
              <div
                v-show="showAccompany || item.audioType === '1'"
                class="accompany__box"
                @click="$emit('getPlayListIndex', index, true)">
                <svg-icon
                  icon-class="accompany"
                  class="accompany-icon" />
                伴奏
              </div>
              <play-icon
                :icon-size="18"
                :width="30"
                :height="30"
                background="rgba(255,255,255, 0.7)"
                arrowColor="#d33a31"
                class="play-icon"
                @click.native="$emit('getPlayListIndex', index, false)" />
            </div>
          </div>
        </div>
      </div>
      <el-pagination
        v-if="pageShow"
        @current-change="$emit('handleCurrentChange', $event)"
        :current-page="currentPage"
        layout="total, prev, pager, next, jumper"
        :page-size="pageSize"
        :total="total"
        class="card__page">
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
import PlayIcon from './PlayIcon.vue';

export default {
  props: {
    name: {
      type: String,
      default: ''
    },
    list: {
      type: Array,
      default: () => []
    },
    width: {
      type: Number,
      default: 120
    },
    height: {
      type: Number,
      default: 120
    },
    total: {
      type: Number,
      default: 0
    },
    currentPage: {
      type: Number,
      default: 0
    },
    pageShow: {
      type: Boolean,
      default: false
    },
    showAccompany: {
      type: Boolean,
      default: false
    },
    showCopyRight: {  // 是否展示版权icon
      type: Boolean,
      default: false
    },
    pageSize: {
      type: Number,
      default: 0
    }
  },
  components: { PlayIcon },
  data() {
    return {

    }
  },
  methods: {
    showPlayIcon(i) {
      this.list[i].canShow = true;
    },

    hidePlayIcon(i) {
      this.list[i].canShow = false;
    },
  },
}
</script>

<style lang="scss">
.card__wrap {
  width: 1300px;
  margin: 0 auto;
  &.el-card {
    border: none;
    border-radius: 8px;
    background: none;
  }
  .card__name {
    color: #333;
  }
  .card__container {
    width: 1260px;
    margin: auto;
    height: 560px;
    .card-image__block {
      margin: 10px;
      display: inline-block;
      vertical-align: middle;
      .card-image__parent {
        position: relative;
        border-radius: 8px;
        overflow: hidden;
        cursor: pointer;
        .image {
          border-radius: 8px;
          background-size: 200%;
          background-repeat: no-repeat;
          margin: 0 auto;
          background-position: center center;
          background-color: #373737;
        }
        .card-image__info {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 100%;
          // height: 100%;
          padding: 15px;
          line-height: 25px;
          opacity: 0;
          visibility: hidden;
          transition: .3s all ease-in-out;
          .name, .author {
            color: #e5e5e5;
            font-size: 12px;
            word-break: break-all;
            overflow: hidden; //超出的文本隐藏
            text-overflow: ellipsis; //溢出用省略号显示
            white-space: nowrap; //溢出不换行
            margin: 0;
            text-align: center;
          }
        }
        .card-image__icon {
          position: absolute;
          bottom: 10px;
          right: 10px;
          display: block;
          width:18px;
          height: 18px;
        }
        .play-icon__container {
          opacity: 0;
          visibility: hidden;
          transition: .3s all ease-in-out;
          .play-icon {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
          }
          .accompany__box {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.7);
            position: absolute;
            top: 5px;
            right: 5px;
            padding: 3px;
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.3);
            display: flex;
            align-items: center;
            letter-spacing: 1px;
            transform: scale(0.9);
            .accompany-icon {
              margin-right: 5px;
            }
          }
        }
        .actived {
          opacity: 1;
          visibility: visible;
        }
      }
      .image--name {
        margin: 5px 0 0 0;
        font-size: 14px;
        color: #333;
      }
    }
  }
  .card__page {
    float: right;
    margin: 20px 20px 30px 0;
  }
}
</style>
