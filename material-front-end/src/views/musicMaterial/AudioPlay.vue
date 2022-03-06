<template>
  <div class="audio__wrap">
    <audio
      ref="audio"
      :src="currentPlay"
      @canplay="getDuration"
      @timeupdate="timeupdate"
      @play="play"
      @pause="pause">
    </audio>
    <div
      class="audio__progress"
      :class="[showCircle ? 'show' : 'notShow']"
      @mouseover="showCircle = true"
      @mouseleave="showCircle = false">
      <el-slider
        v-model="currentTime"
        :min="0"
        :max="endTime"
        :show-tooltip="false"
        :show-input-controls="false"
        @change="changeCurrentTime" />
    </div>
    <div class="audio__block">
      <div
        :style="{'background-image': `url(${playList[currentIndex].picUrl})`}"
        class="img">
      </div>
      <div class="info__block">
        <svg-icon
          v-show="isAccompany"
          icon-class="accompany"
          class="accompany-icon" />
        <span class="singerName">{{ playList[currentIndex].audioName }} </span>
        <span class="line">-</span>
        <span class="name">{{ playList[currentIndex].audioAuthor }}</span>
        <div class="time">{{ calTime(currentTime) }} / {{ calTime(endTime) }}</div>
      </div>
      <div class="icon-controls">
        <svg-icon
          icon-class="prevPlay"
          class="prev"
          @click="prevPlay()" />
        <play-icon
          :width="35"
          :height="35"
          :iconSize="20"
          :isPlay="isPlay"
          arrowColor="#fff"
          @click.native="controlPlay" />
        <svg-icon
          icon-class="nextPlay"
          class="next"
          @click="nextPlay()" />
      </div>
      <div class="list-controls">
<!--        v-show="getToken() !== '' && getToken() !== undefined"-->
        <svg-icon
          icon-class="down"
          class="download"
          @click="download()" />
      </div>
    </div>
  </div>
</template>

<script>
import PlayIcon from './PlayIcon.vue';
import { getToken } from '@/utils/auth';

/**
 * 计算时长
 */
function calTime(time) {
  let m = Math.floor(time / 60);
  let s = Math.round(time % 60);
  return `${m < 10 ? '0' + m : m}:${s < 10 ? '0' + s : s}`;
}

export default {
  props: {
    playList: {
      type: Array,
      default: () => []
    },
    currentIndex: {
      type: Number,
      default: 0
    },
    isAccompany: {
      type: Boolean,
      default: false,
    },
  },
  components: { PlayIcon },
  data() {
    return {
      currentTime: 0,
      endTime: 0,
      isPlay: false,
      showCircle: false
    }
  },
  computed: {
    currentPlay() {
      if (!this.isAccompany) {
        return process.env.VUE_APP_BASE_API + `/profile/audio_music/${this.playList[this.currentIndex].audioPath}.mp3`;
      } else {
        return process.env.VUE_APP_BASE_API + `/profile/audio_music/audio_off_vocal/${this.playList[this.currentIndex].audioPath}.mp3`;
      }
    },
  },
  mounted() {
    this.audioPlay();
  },
  methods: {
    calTime,
    getToken,
    /**
     * 播放音乐
     */
    audioPlay() {
      this.$refs.audio.play();
      this.isPlay = true;
    },
    /**
     * 获取音乐时长
     */
    getDuration() {
      this.endTime = this.$refs.audio.duration;
    },
    /**
     * 更新当前时间
     * 如果当前音频进度 = 总时长，则自动播放下一首
     */
    timeupdate(e) {
      this.currentTime = e.target.currentTime;
      if(e.target.currentTime === this.endTime ) {
        this.nextPlay();
      }
    },
    /**
     * 通过进度条改变当前音频进度
     * @param value 当前的值
     */
    changeCurrentTime(value) {
      this.$refs.audio.currentTime = value;
      this.currentTime = value;
    },
    play() {
      this.isPlay = true;
    },
    pause() {
      this.isPlay = false;
    },
    /**
     * 控制播放按钮
     */
    controlPlay() {
      const audio = this.$refs.audio;
      this.isPlay = !this.isPlay;
      if(!audio.paused) {
        audio.pause();
      } else {
        audio.play();
      }
    },
    /**
     * 上一首播放
     */
    prevPlay() {
      const index = this.currentIndex === 0 ? this.playList.length - 1 : this.currentIndex - 1;
      this.$emit('update:currentIndex', index);
      this.$nextTick(() => {
        this.audioPlay();
      });
    },
    /**
     * 下一首播放
     */
    nextPlay() {
      const index = this.currentIndex === this.playList.length - 1 ? 0 : this.currentIndex + 1;
      this.$emit('update:currentIndex', index);
      this.$nextTick(() => {
        this.audioPlay();
      });
    },
    /**
     * 下载歌曲
     */
    download() {
      window.open(this.currentPlay);
    },
  },
}
</script>

<style lang="scss">
.audio__wrap {
  position: fixed;
  bottom: 0;
  min-width: 1200px;
  width: 100%;
  background: #fff;
}
.audio__progress {
  .el-slider__runway {
    width: 100%;
    height: 5px;
    margin-bottom: 15px;
    border-radius: 3px;
    position: relative;
    cursor: pointer;
    vertical-align: middle;
    background: #f5f5f5;
  }
  .el-slider__bar {
    height: 6px;
    border-top-left-radius: 3px;
    border-bottom-left-radius: 3px;
    position: absolute;
    background: #d33a31;
  }
  .el-slider__button {
    display: inline-block;
    width: 20px;
    height: 20px;
    vertical-align: middle;
    border: 2px solid #d33a31;
    background-color: #d33a31;
    border-radius: 50%;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    -webkit-transition: .2s;
    transition: .2s;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }
}
.audio__block {
  display: flex;
  align-items: center;
  width: 100%;
  margin: 0 20px 15px 20px;
  font-size: 14px;
  background: #fff;
  .img {
    width: 50px;
    height: 50px;
    border-radius: 8px;
    background-size: 100% 100%;
    cursor: pointer;
    position: relative;
    &.mask:before {
      position: absolute;
      content: '';
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.6);
      border-radius: 8px;
    }
    .fangda {
      font-size: 35px !important;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 1;
      color: #fff;
      &.show {
        display: block;
      }
      &.notShow {
        display: none;
      }
    }
  }
  .info__block {
    margin-left: 20px;
    height: 50px;
    line-height: 25px;
    .accompany-icon {
      color: #d33a31;
      font-size: 16px;
      margin-right: 5px;
      vertical-align: middle;
    }
    .name {
      margin-left: 5px;
      color: #939393;
      &:hover {
        cursor: pointer;
        color: #313131;
      }
    }
    .time {
      color: #b7b7b7;
      font-size: 12px;
    }
  }
  .icon-controls {
    display: flex;
    align-items: center;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    .prev, .next {
      color: #d33a31;
      font-size: 30px !important;
      margin: 0 20px;
      cursor: pointer;
    }
  }
  .list-controls {
    position: absolute;
    right: 100px;
    .download {
      font-size: 24px;
      cursor: pointer;
    }
  }
}
.show .el-slider__button-wrapper {
  display: block;
}
.notShow .el-slider__button-wrapper {
  display: none;
}
</style>
