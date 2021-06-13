<template>
  <div class="custom-video" v-if="videoShow">
    <div class="custom-video_container" ref="custom-video_container">
      <div class="custom-video_video">
        <video ref="custom-video" :src="blobURL">
          <p>设备不支持</p>
        </video>
      </div>
    </div>
    <!-- 缩略图，裁剪区域 -->
    <div class="video-controls" @mousedown="handleClick">
      <div class="thumbs" ref="thumbs">
        <div class="inner" v-if="thumbCount" ref="thumbs-inner">
          <div
            class="inner-item"
            :style="`width:${videoUnitWidth}px;`"
            v-for="(item, index) in thumbArr"
            :key="index"
          >
            <video
              width="100%"
              preload="metadata"
              :src="item.url"
              @canplay="item.loading = false"
            ></video>
            <div class="inner-loading" v-if="item.loading">
              <div class="loading">
                <div class="loading-con"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="control-bars" ref="control-bars">
        <div
          class="control-bars-mask left"
          data-direction="left"
          :style="`width:${leftMovePercentage}%;`"
        ></div>
        <div
          class="control-bars-mask right"
          data-direction="right"
          :style="`width:${rightMovePercentage}%;`"
        ></div>
        <div
          class="control-bars-progress"
          :style="`left:${videoEdit.currentPosition}%;`"
          :class="{ animate: videoEdit.play }"
        >
          <svg
            width="54px"
            height="24px"
            viewBox="0 0 54 24"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
          >
            <g
              id="Page-1"
              stroke="none"
              stroke-width="1"
              fill="none"
              fill-rule="evenodd"
            >
              <path
                d="M27,23 L27,24 L26,24 L26,23 C26,20.2385763 23.7614237,18 21,18 L9,18 C4.02943725,18 0,13.9705627 0,9 C0,4.02943725 4.02943725,0 9,0 L45,0 C49.9705627,0 54,4.02943725 54,9 C54,13.9705627 49.9705627,18 45,18 L32,18 L32,18 C29.2385763,18 27,20.2385763 27,23 Z"
                id="time_bg"
                fill="#FFFFFF"
              ></path>
            </g>
          </svg>
          <span class="text">{{ timeTranslate(currentTime) }}</span>
        </div>
        <div
          class="control-bars-wrapper"
          :style="`left:${leftMovePercentage}%;right:${rightMovePercentage}%;`"
        >
          <div
            ref="move-left-icon"
            class="control-bars-move left"
            @mousedown="handleMoveDown($event, 'left')"
          ></div>
          <div
            ref="move-right-icon"
            class="control-bars-move right"
            @mousedown="handleMoveDown($event, 'right')"
          ></div>
        </div>
      </div>
    </div>
    <!-- 按钮区域 -->
    <div class="video-btn">
      <div class="toggle" @click="togglePlayStatus">
        <div class="toggle-icon" :class="{ playing: videoEdit.play }"></div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'ClipCut',
    props: {
      url: {
        type: String,
        required: true
      },
      startPoint: {
        type: Number,
      },
      endPoint: {
        type: Number,
      }
    },
    data() {
      return {
        blobURL: '',
        videoState: {
          play: false, // 播放状态
          currentPosition: 0 // 当前播放点距离左边的百分比
        },
        videoEdit: {
          start: 0,
          end: 0,
          duration: 0,
          play: false, // 播放状态
          currentPosition: 0 // 当前播放点距离左边的百分比
        },
        videoDom: null, // video
        duration: 0, // 视频总时长
        currentTime: 0, // 视频当前播放时长 = this.videoDom.currentTime
        objectURL: '',
        videoUnit: 0,
        videoUnitWidth: 0,
        videoRatio: 0,
        isPortraitVideo: false,
        thumbCount: 0,
        thumbArr: [], // 缩略图数组
        leftMovePercentage: 0,
        leftMoveInit: 0,
        rightMovePercentage: 0,
        rightMoveInit: 0,
        videoShow: true
      }
    },
    mounted() {
      this.init()
      window.onresize = () => {
        this.throttle(this.init(), 300)
      }
    },
    computed: {
      inputStartLeftTime: {
        set(val) {
          val = val * 60 + this.toInt(document.getElementById('range-1').value)
          if (val >= this.videoEdit.end || val < 0) {
            val = 0
          }
          this.videoEdit.start = val
        },
        get() {
          return this.timeTranslate(this.videoEdit.start).split(':')[0]
        }
      },
      inputStartRightTime: {
        set(val) {
          val = this.toInt(document.getElementById('range-0').value) * 60 + val
          if (val >= this.videoEdit.end || val < 0) {
            val = 0
          }
          this.videoEdit.start = val
        },
        get() {
          return this.timeTranslate(this.videoEdit.start).split(':')[1]
        }
      },
      inputEndLeftTime: {
        set(val) {
          val = val * 60 + this.toInt(document.getElementById('range-3').value)
          if (val <= this.videoEdit.start || val > this.videoEdit.duration) {
            val = this.videoEdit.duration
          }
          this.videoEdit.end = val
        },
        get() {
          return this.timeTranslate(this.videoEdit.end).split(':')[0]
        }
      },
      inputEndRightTime: {
        set(val) {
          val = this.toInt(document.getElementById('range-2').value) * 60 + val
          if (val <= this.videoEdit.start || val > this.videoEdit.duration) {
            val = this.videoEdit.duration
          }
          this.videoEdit.end = val
        },
        get() {
          return this.timeTranslate(this.videoEdit.end).split(':')[1]
        }
      }
    },
    watch: {
      'videoEdit.start': {
        handler(val) {
          this.currentTime = val
          this.videoEdit.currentPosition =
            (this.currentTime / this.videoEdit.duration) * 100
          this.leftMovePercentage = this.videoEdit.currentPosition
          this.$emit('getTime', {
            start: val,
            end: this.videoEdit.end
          })
        },
        deep: true
      },
      'videoEdit.end': {
        handler(val) {
          this.currentTime = val
          this.videoEdit.currentPosition =
            (this.currentTime / this.videoEdit.duration) * 100
          this.rightMovePercentage = 100 - this.videoEdit.currentPosition
          this.$emit('getTime', {
            start: this.videoEdit.start,
            end: val
          })
        },
        deep: true
      }
    },
    methods: {
      throttle(fn, threshold, scope) {
        let timer
        return function () {
          const context = scope || this
          const args = arguments
          if (!timer) {
            timer = setTimeout(function () {
              fn.apply(context, args)
              timer = null
            }, threshold)
          }
        }
      },
      init() {
        // 初始化相关元数据
        this.videoDom = this.$refs['custom-video']
        this.leftIconDom = this.$refs['move-left-icon']
        this.rightIconDom = this.$refs['move-right-icon']
        this.thumbsWidth = this.$refs.thumbs.clientWidth
        this.leftMoveInit = this.getOffset(this.leftIconDom).left + 5
        this.rightMoveInit = this.getOffset(this.rightIconDom).left + 5
        this.minWidthPercentage = ((20 / this.thumbsWidth) * 100).toFixed(4) // 最小裁剪区域所占百分比
        this.initMedaData()

        this.transformBlob()
        document.addEventListener('mouseup', ev => {
          this.handleMoveStatus = false
        })
        document.addEventListener('mousemove', ev => {
          if (!this.handleMoveStatus) return
          if (this.handleMoveDirection === 'left') {
            const distanceMoveXLeft = ev.clientX - this.leftMoveInit

            this.leftMovePercentage =
              distanceMoveXLeft > 0
                ? ((distanceMoveXLeft / (this.thumbsWidth - 20)) * 100).toFixed(4)
                : 0

            // 控制裁剪百分比最小值
            if (
              this.leftMovePercentage >
              100 - this.rightMovePercentage - this.minWidthPercentage
            ) {
              this.leftMovePercentage =
                100 - this.rightMovePercentage - this.minWidthPercentage
            }

            this.videoEdit.start = (
              (this.videoEdit.duration * this.leftMovePercentage) /
              100
            ).toFixed(4)
          }
          if (this.handleMoveDirection === 'right') {
            const distanceMoveXRight = this.rightMoveInit - ev.clientX

            this.rightMovePercentage =
              distanceMoveXRight > 0
                ? ((distanceMoveXRight / (this.thumbsWidth - 20)) * 100).toFixed(
                4
                )
                : 0

            // 控制裁剪百分比最小值
            if (
              this.rightMovePercentage >
              100 - this.leftMovePercentage - this.minWidthPercentage
            ) {
              this.rightMovePercentage =
                100 - this.leftMovePercentage - this.minWidthPercentage
            }

            this.videoEdit.end = (
              this.videoEdit.duration *
              (1 - this.rightMovePercentage / 100)
            ).toFixed(4)
          }
          this.handleClick(ev, this.handleMoveDirection)
        })
      },
      toInt(val) {
        return parseInt(val) || 0
      },
      togglePlayStatus() {
        // 播放暂停按钮事件
        this.videoEdit.play ? this.toggleVideoPause() : this.toggleVideoPlay()
      },
      toggleVideoPlay() {
        // 处理当前位置在末尾的时候先初始化开始播放时间
        if (this.videoEdit.end - this.currentTime < 0.01) {
          this.videoDom.currentTime = this.videoEdit.start
        }
        // 为了取消当前点平滑移动到开始点的过渡
        setTimeout(() => {
          this.videoDom.play()
          this.videoEdit.play = true
        }, 50)
      },
      toggleVideoPause() {
        this.videoDom.pause()
        this.videoEdit.play = false
      },
      playEnd() {
        this.videoDom.currentTime = this.videoEdit.start
        this.videoDom.pause()
        this.videoEdit.play = false
      },
      transformBlob() {
        const self = this
        const xhr = new XMLHttpRequest()
        xhr.open('GET', this.url, true)
        xhr.responseType = 'blob'
        xhr.onload = function (e) {
          if (this.status === 200) {
            // 获取blob对象
            const myBlob = this.response
            self.blobURL = URL.createObjectURL(myBlob)
          } else {
            alert('视频转换失败')
          }
        }
        xhr.send()
      },
      initMedaData() {
        // 初始化video相关事件
        this.videoDom.addEventListener('loadedmetadata', () => {
          // 获取视频总时长
          this.videoEdit.duration = this.videoDom.duration // 视频总时长
          if (this.startPoint){
            this.videoEdit.start = this.startPoint
          }
          if (this.endPoint) {
            this.videoEdit.end = this.endPoint
          }
          else{
            this.videoEdit.end = this.videoEdit.duration
          }
          // console.log(this.videoEdit.duration)

        })
        const self = this
        this.videoDom.addEventListener('canplay', function () {
          // 监听视频可播放时的状态
          self.videoRatio = this.videoHeight / this.videoWidth
          self.isPortraitVideo = self.videoRatio > 1.5 // 是否是竖向视频
          self.videoUnitWidth = self.isPortraitVideo ? 28 : 88 // 单个缩略图宽度
          self.thumbCount = Math.ceil(self.thumbsWidth / self.videoUnitWidth) // 缩略图个数
          self.videoUnit = self.videoEdit.duration / self.thumbCount

          // 缩略图
          if (self.thumbArr.length !== self.thumbCount) {
            self.thumbArr = []
            for (let i = 0; i < self.thumbCount; i++) {
              self.thumbArr.push({
                url: `${self.blobURL}#t=${self.videoUnit * i}`,
                loading: true
              })
            }
          }
          const innerMoveLeft = Math.round(
            (self.thumbCount * self.videoUnitWidth - self.thumbsWidth) / 2
          )
          self.$nextTick(() => {
            self.$refs['thumbs-inner'].style.marginLeft = `${-innerMoveLeft}px`
          })
        })

        this.videoDom.addEventListener('timeupdate', () => {
          // 监听视频播放过程中的时间
          this.videoEdit.currentPosition =
            (this.videoDom.currentTime / this.videoEdit.duration) * 100
          this.currentTime = this.videoDom.currentTime
          if (
            this.videoEdit.end - this.currentTime < 0.01 &&
            this.videoEdit.play
          ) {
            this.playEnd()
          }
        })
      },
      handleMoveDown(ev, direction) {
        this.handleMoveStatus = true
        this.handleMoveDirection = direction
        this.toggleVideoPause()
        this.handleClick(ev, direction)
      },
      handleClick(ev, direction) {
        // 区分各种情况是为了获取各种情况的当前播放点更准确
        if (direction === 'left') {
          this.videoEdit.currentPosition = this.leftMovePercentage
        } else if (direction === 'right') {
          this.videoEdit.currentPosition = 100 - this.rightMovePercentage
        } else {
          // 点击中间剪辑区域
          this.videoEdit.currentPosition =
            ((ev.clientX - this.leftMoveInit) / this.thumbsWidth) * 100
        }
        this.currentTime = (
          (this.videoEdit.currentPosition * this.videoEdit.duration) /
          100
        ).toFixed(4)
        this.videoDom.currentTime = this.currentTime
        // 处理两边 mask 点击而非滑动时,拖拽区域的处理
        if (ev.target.dataset.direction === 'left' && !this.handleMoveStatus) {
          this.leftMovePercentage = this.videoEdit.currentPosition
          this.videoEdit.start = this.currentTime
        }
        if (ev.target.dataset.direction === 'right' && !this.handleMoveStatus) {
          this.rightMovePercentage = 100 - this.videoEdit.currentPosition
          this.videoEdit.end = this.currentTime
        }
        // 百分比取最大值：100 最小值：0
        this.videoEdit.currentPosition =
          this.videoEdit.currentPosition > 100
            ? 100
            : this.videoEdit.currentPosition
        this.videoEdit.currentPosition =
          this.videoEdit.currentPosition < 0 ? 0 : this.videoEdit.currentPosition
      },
      getOffset(node, offset) {
        // 获取当前屏幕下进度条的左偏移量和又偏移量
        if (!offset) {
          offset = {}
          offset.left = 0
          offset.top = 0
        }
        if (node === document.body || node === null) {
          return offset
        }
        offset.top += node.offsetTop
        offset.left += node.offsetLeft
        return this.getOffset(node.offsetParent, offset)
      },
      timeTranslate(t) {
        // 时间转化
        let m = Math.floor(t / 60)
        m < 10 && (m = '0' + m)
        return m + ':' + ((t % 60) / 100).toFixed(2).slice(-2)
      }
    }
  }
</script>
<style scoped lang="scss">
  .custom-video {
    width: 100%;
    /*user-select: none;*/
    /*margin: 0 auto;*/
    /*min-height: 100%;*/
    /*padding: 20px;*/
    /*border-radius: 20px;*/
    /*min-width: 500px;*/
    &_container {
      /*height: 400px;*/
      /*margin: 0 auto;*/
      /*position: relative;*/
      /*overflow: hidden;*/
    }

    &_video {

      /*height: 100%;*/
      video {
        width: 100%;
      }
    }
  }

  .thumbs {
    white-space: nowrap;
    overflow: hidden;
    height: 47px;
    background: #ffc7d1;

    .inner {
      height: 47px;
      display: flex;

      &-item {
        position: relative;
      }

      &-loading {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
      }
    }

    video {
      object-fit: cover;
    }
  }

  .video-controls {
    position: relative;
    margin: 40px 0;
  }

  .control-bars {
    position: absolute;
    right: 0;
    bottom: 0;
    top: 0;
    left: 0;

    &-wrapper {
      position: absolute;
      right: 0;
      bottom: 0;
      top: 0;
      left: 0;
      border: 1px solid #04f0fb;
      z-index: 10;
      min-width: 20px;
    }

    &-mask {
      position: absolute;
      top: 0;
      bottom: 0;
      background-color: rgba(25, 30, 64, 0.8);

      &.left {
        left: 0;
      }

      &.right {
        right: 0;
      }
    }

    &-progress {
      position: absolute;
      height: 80px;
      top: -15px;
      width: 1px;
      background: #ffffff;
      border-radius: 100px;

      &.animate {
        transition: all 0.3s;
      }

      svg {
        position: absolute;
        top: -10px;
        left: -26px;
      }

      .text {
        position: absolute;
        width: 54px;
        height: 18px;
        top: -10px;
        left: -26px;
        font-size: 12px;
        line-height: 18px;
      }
    }

    &-move {
      position: absolute;
      width: 10px;
      height: 10px;
      background: #04f0fb;
      top: 50%;
      transform: translateY(-50%);
      border-radius: 50%;
      cursor: ew-resize;
      z-index: 2;

      &:active {
        background: #fff;
      }

      &.left {
        left: -5px;
      }

      &.right {
        right: -5px;
      }
    }
  }

  .video-btn {
    position: absolute;
    top: 336px;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .toggle {
      margin-left: 18px;
      width: 100px;
      height: 45px;
      line-height: 45px;
      border-radius: 30px;
      background-color: rgba(0, 0, 0, 0.3);
      position: relative;
      transition: background-color 0.2s;
      cursor: pointer;

      &-icon {
        position: absolute;
        display: inline-block;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 0;
        height: 0;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
        border-left: 12px solid #fff;
        opacity: 1;
        transition: all 0.2s;

        &.playing {
          width: 12px;
          height: 15px;
          border-left: solid 4px #fff;
          border-right: solid 4px #fff;
          border-top: solid 0 transparent;
          border-bottom: solid 0 transparent;
          box-sizing: border-box;
        }
      }
    }

    .crop {
      &-range {
        display: flex;
        align-items: center;
        font-size: 14px;
      }

      &-input {
        height: 30px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        overflow: hidden;
        padding: 0 24px;
        display: flex;
        align-items: center;

        input {
          float: left;
          width: 18px;
          outline: none;
          background: transparent;
          border: none;
          font-size: 14px;
          color: #fff;
        }

        span {
          width: 8px;
          line-height: 28px;
          height: 28px;
          float: left;
          margin: 0;
          padding: 0;
          color: #fff;
        }
      }
    }
  }

  .loading {
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;

    &-con {
      position: absolute;
      animation: loading 1s linear infinite;
      width: 25px;
      height: 25px;
      border-radius: 50%;
      box-shadow: 0 2px 0 0 #fff; // ffc7d1
      transform-origin: 50% 50%;
    }
  }

  @keyframes loading {
    0% {
      transform: rotate(0deg);
    }
    50% {
      transform: rotate(180deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
