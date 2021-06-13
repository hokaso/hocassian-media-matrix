<template>
  <div
    :style="{ width: width * rowIndex + 40 * rowIndex + 20 + 'px'}"
    class="pic-video__wrap">
    <div
      v-for="(item, index) in syncList"
      :key="index + item.materialPath"
      :style="{
        width: width + 'px',
        height: width * 9 / 16 + 'px'
      }"
      class="pic-video__block id-copy"
      @click.left="copy($event, item.materialPath)"
      @contextmenu.prevent="handleShow(item)"
      @mouseover="videoPlayback(index)"
      @mouseout="videoStopped(index)">
      <img
        v-show="!item.isShow"
        :src="item.materialPicPath" alt=""/>
      <video
        v-show="item.isShow"
        autoplay muted loop>
        <source :src="item.videoPath" type="video/mp4">
      </video>
      <div
        v-show="!item.isShow && showVideoInfo"
        class="pic-video__tag">
        <p class="pic-video__time">
          {{ item.materialTime }}
        </p>
        <img
          v-show="showCopyRight"
          :src="item.isCopyright === '0' ? require('@/assets/images/copyright.png') : require('@/assets/images/no-copyright.png')"/>
      </div>
    </div>
    <el-pagination
      v-show="needPage"
      @current-change="$emit('handleCurrentChange', $event)"
      :current-page="currentPage"
      layout="total, prev, pager, next, jumper"
      :total="total"
      class="pic-video__page">
    </el-pagination>
    <!-- 添加或修改视频素材对话框 -->
    <el-dialog title="素材详情" :visible.sync="open" width="1200px" append-to-body class="pic-video__form">
      <el-row :gutter="24">
        <el-form ref="form" :model="form" label-width="80px">
          <el-col :span="14">
            <el-form-item label="素材标注" prop="materialNote">
              <el-input v-model="form.materialNote" type="textarea" placeholder="请输入素材标注" :disabled="true"/>
            </el-form-item>
            <div class="pic-video__labels">
              <el-form-item label="素材打分" prop="materialNote">
                <el-input v-model="form.materialMark" :disabled="true"/>
              </el-form-item>
              <el-form-item label="创建时间" prop="materialCreate">
                <el-date-picker clearable size="small" style="width: 200px"
                                v-model="form.materialCreate"
                                type="datetime"
                                format="yyyy-MM-dd HH:mm:ss"
                                value-format="yyyy-MM-dd HH:mm:ss"
                                placeholder="选择创建时间"
                                :disabled="true">
                </el-date-picker>
              </el-form-item>
            </div>
            <div class="pic-video__labels">
              <el-form-item label="素材类型" prop="materialType">
                <el-select v-model="form.materialType" placeholder="请选择素材类型" :disabled="true" class="select">
                  <el-option
                    v-for="dict in materialTypeOptions"
                    :key="dict.dictValue"
                    :label="dict.dictLabel"
                    :value="dict.dictValue"
                  ></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="素材版权" prop="isCopyright">
                <el-select v-model="form.isCopyright" placeholder="请选择素材版权" :disabled="true" class="select">
                  <el-option
                    v-for="dict in isCopyrightOptions"
                    :key="dict.dictValue"
                    :label="dict.dictLabel"
                    :value="dict.dictValue"
                  ></el-option>
                </el-select>
              </el-form-item>
            </div>
            <el-form-item label="素材标签" prop="materialTag">
              <el-tag
                :key="index"
                v-for="(tag, index) in form.materialTag">
                {{tag}}
              </el-tag>
            </el-form-item>
          </el-col>
          <el-col :span="10">
            <div class="pic-video__labels">
              <el-form-item label="素材尺寸" prop="materialNote" label-width="80px">
                <el-input v-model="form.materialSize" :disabled="true"/>
              </el-form-item>
              <el-form-item label="素材时长" prop="materialNote" label-width="90px">
                <el-input v-model="form.materialTime" :disabled="true"/>
              </el-form-item>
            </div>
            <el-form-item label="素材预览">
              <video controls="controls" :src="clip_url + form.materialPath + '.mp4'" style="width: 100%;"></video>
            </el-form-item>
            <el-form-item label="素材截图">
              <div class="pic-video__show">
                <div class="pic">
                  <img :src="clip_pic_url + form.materialPath + '_0.jpg'" alt="" style="max-width: 100%;"/>
                </div>
                <div class="pic">
                  <img :src="clip_pic_url + form.materialPath + '_1.jpg'" alt="" style="max-width: 100%;"/>
                </div>
                <div class="pic">
                  <img :src="clip_pic_url + form.materialPath + '_2.jpg'" alt="" style="max-width: 100%;"/>
                </div>
              </div>
            </el-form-item>
          </el-col>
        </el-form>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
  import Clipboard from 'clipboard'

  export default {
    props: {
      list: {
        type: Array,
        default: () => []
      },
      width: {
        type: Number,
        default: 300
      },
      rowIndex: {
        type: Number,
        default: 3
      },
      total: {
        type: Number,
        default: 0
      },
      currentPage: {
        type: Number,
        default: 1
      },
      needPage: {
        type: Boolean,
        default: false
      },
      showVideoInfo: {
        type: Boolean,
        default: false
      },
      showCopyRight: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        // 是否显示弹出层
        open: false,
        // 表单参数
        form: {},
        clip_url: process.env.VUE_APP_BASE_API + '/profile/video_clip/preview/',
        // 图片路径
        clip_pic_url: process.env.VUE_APP_BASE_API + "/profile/video_clip/clip_slot/",
        materialTypeOptions: [{
          'searchValue': null,
          'createBy': 'admin',
          'createTime': '2021-02-21 01:30:29',
          'updateBy': null,
          'updateTime': null,
          'remark': null,
          'params': {},
          'dictCode': 117,
          'dictSort': 0,
          'dictLabel': '高质素材',
          'dictValue': '0',
          'dictType': 'material_type',
          'cssClass': null,
          'listClass': null,
          'isDefault': 'N',
          'status': '0',
          'default': false
        }, {
          'searchValue': null,
          'createBy': 'admin',
          'createTime': '2021-02-21 01:30:57',
          'updateBy': null,
          'updateTime': null,
          'remark': null,
          'params': {},
          'dictCode': 118,
          'dictSort': 1,
          'dictLabel': '普通素材',
          'dictValue': '1',
          'dictType': 'material_type',
          'cssClass': null,
          'listClass': null,
          'isDefault': 'N',
          'status': '0',
          'default': false
        }],
        isCopyrightOptions: [{
          'searchValue': null,
          'createBy': 'admin',
          'createTime': '2021-02-21 19:43:22',
          'updateBy': null,
          'updateTime': null,
          'remark': null,
          'params': {},
          'dictCode': 126,
          'dictSort': 0,
          'dictLabel': '有版权',
          'dictValue': '0',
          'dictType': 'material_copyright',
          'cssClass': null,
          'listClass': null,
          'isDefault': 'N',
          'status': '0',
          'default': false
        }, {
          'searchValue': null,
          'createBy': 'admin',
          'createTime': '2021-02-21 19:43:32',
          'updateBy': null,
          'updateTime': null,
          'remark': null,
          'params': {},
          'dictCode': 127,
          'dictSort': 1,
          'dictLabel': '无版权',
          'dictValue': '1',
          'dictType': 'material_copyright',
          'cssClass': null,
          'listClass': null,
          'isDefault': 'N',
          'status': '0',
          'default': false
        }],
        syncList: []
      };
    },

    methods: {
      copy(e, text) {
        const clipboard = new Clipboard(e.target, { text: () => text });
        clipboard.on("success", e => {
          this.$message.success(text + ' 已复制到剪贴板！')

          // 释放内存
          clipboard.off("error");
          clipboard.off("success");
          clipboard.destroy();
        });

        clipboard.on("error", e => {
          console.log(e)
          this.$message.error('不支持自动复制！')

          // 释放内存
          clipboard.off("error");
          clipboard.off("success");
          clipboard.destroy();
        });

        clipboard.onClick(e);
      },
      handleShow(info) {
        // info.materialTag = JSON.parse(info.materialTag)
        const newTag = []
        Object.keys(info.materialTag).forEach(key => {
          if (this.getLength(info.materialTag[key]) > 0) {
            newTag.push(info.materialTag[key])
          }
        })
        info.materialTag = newTag
        this.form = info
        this.open = true
      },
      getLength(str) {
        // console.log(str)
        let realLength = 0, len = str.length, charCode = -1
        for (let i = 0; i < len; i++) {
          charCode = str.charCodeAt(i)
          if (charCode >= 0 && charCode <= 128) {
            realLength += 1
          } else {
            realLength += 2
          }
        }
        return realLength
      },
      videoPlayback(index) {
        this.syncList[index].isShow = true
      },
      videoStopped(index) {
        this.syncList[index].isShow = false
      }
    },
    created() {

    },
    // beforeDestroy() {
    //
    // },
    mounted() {
      // const clipboard = new Clipboard('.id-copy')
      // clipboard.on('success', e => {
      //   this.$message.success(e.text + ' 已复制到剪贴板！')
      //   // 释放内存
      //   clipboard.off('error')
      //   clipboard.off('success')
      //   clipboard.destroy()
      // })
    },
    watch: {
      list: {
        handler(nv) {
          // debugger
           this.syncList = nv.map(item => ({
             ...item,
             materialTag: JSON.parse(item.materialTag),
            })
          );
        },
        deep: true,
        immediate: true
      }
    },
  }
</script>

<style lang="scss">
  .pic-video__wrap {
    width: 100%;
    height: 100%;
    padding: 10px;

    .pic-video__block {
      display: inline-block;
      margin: 20px 20px;
      background: #e6e6e6;
      cursor: pointer;
      text-align: center;
      position: relative;
      vertical-align: top;

      & > img, & > video {
        display: inline-block;
        margin: auto;
        max-width: 100%;
        max-height: 100%;
        border-style: none;
        filter: brightness(120%) saturate(130%);
        -webkit-filter: brightness(120%) saturate(130%);
      }

      .pic-video__tag {
        position: absolute;
        z-index: 1;
        bottom: 0;
        display: flex;
        justify-content: space-between;
        width: 100%;
        align-items: center;
        padding: 0 10px;

        & > p {
          background: #333;
          color: #fff;
          padding: 5px;
          font-size: 12px;
          border-radius: 12px;
        }

        & > img {
          display: block;
          width: 24px;
          height: 24px;
        }
      }
    }
  }

  .pic-video__page {
    text-align: right;
    margin: 10px 0 30px 0;
  }

  .pic-video__form{


  }

  .mini-tag {
    -webkit-transform: scale(0.8);
    margin: 4px;
  }

  .tag-up {
    margin-bottom: 20px;
  }

  .input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }

  .el-tag {
    margin: 5px;
  }

  .select .el-input {
    .el-input__inner {
      max-width: 180px;
    }
  }

  .pic-video__show{
    width: 100%;
    display: flex;
    .pic {
      /*display: inline-block;*/
      /*position: relative;*/
      /*float: left;*/
      /*width: 33%;*/
      box-sizing: border-box;
      padding-right: 15px;
      min-width: 135px;
    }
  }

  .pic-video__labels {
    display: flex;
    margin-bottom: 20px;
  }
  /*.button-new-tag {*/
  /*  margin: 5px;*/
  /*  height: 32px;*/
  /*  line-height: 30px;*/
  /*  padding-top: 0;*/
  /*  padding-bottom: 0;*/
  /*}*/
</style>
