<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="视频简介" prop="videoProfile">
        <el-input
          v-model="queryParams.videoProfile"
          placeholder="请输入视频简介"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="视频分类" prop="videoClass">
        <el-input
          v-model="queryParams.videoClass"
          placeholder="请输入视频分类"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="视频作者" prop="videoAuthor">
        <el-input
          v-model="queryParams.channelOwner"
          placeholder="请输入视频作者"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="cyan" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['business:video:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['business:video:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['business:video:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['business:video:export']"
        >导出</el-button>
      </el-col>
	  <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="videoList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="视频标题" align="center" prop="videoTitle" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <a v-if="scope.row.videoUrl" target="_blank" :href="scope.row.videoUrl" class="link-type" style="margin-right: 10px;">
            <span>{{ scope.row.videoTitle }}</span>
          </a>
          <span v-else>{{ scope.row.videoTitle }}</span>
        </template>
      </el-table-column>
      <el-table-column label="视频简介" align="center" prop="videoProfile" :show-overflow-tooltip="true"/>
      <el-table-column label="视频封面" align="center">
        <template slot-scope="scope">
          <img v-if="scope.row.videoIsHuge === '1'" :src="video_pic_url + scope.row.videoPic" alt="" class="pic-in-list">
          <img v-else-if="scope.row.videoIsHuge === '2'" :src="video_pic_url + scope.row.videoHugePic" alt="" class="pic-in-list">
        </template>
      </el-table-column>
      <el-table-column label="视频分类" align="center" prop="videoClass">
        <template slot-scope="scope">
          <el-tag v-for="ikey in scope.row.videoClass" :key="ikey" type="success" style="margin: 10px;">
            {{ikey}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="视频作者" align="center" prop="busChannel.channelOwner">
        <template slot-scope="scope">
          <a v-if="scope.row.busChannel.channelUrl" target="_blank" :href="scope.row.busChannel.channelUrl" class="link-type" style="margin-right: 10px;">
            <span>{{ scope.row.busChannel.channelOwner }}</span>
          </a>
          <span v-else>{{ scope.row.busChannel.channelOwner }}</span>
        </template>
      </el-table-column>
      <el-table-column label="视频种类" align="center" prop="videoIsHuge" :formatter="videoIsHugeFormat">
        <template slot-scope="scope">
          <el-tag :type="scope.row.videoIsHuge | statusFilter">
            {{ scope.row.videoIsHuge | statusNameFilter}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="视频状态" align="center" width="100">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.videoStatus"
            active-value="1"
            inactive-value="0"
            @change="updateVideoStatus(scope.row)"
            v-hasPermi="['business:video:status']"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['business:video:edit']"
          >修改</el-button>
          <router-link target="_blank" :to="video_pic_url + scope.row.videoJson" class="link-type" style="margin: 0 10px 0 10px;">
            <el-button
              size="mini"
              type="text"
              icon="el-icon-download"
              v-hasPermi="['business:video:export']"
            >详情</el-button>
          </router-link>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['business:video:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改视频管理对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="视频标题" prop="videoTitle">
          <el-input v-model="form.videoTitle" type="textarea" placeholder="请输入内容" />
        </el-form-item>
        <el-form-item label="视频简介" prop="videoProfile">
          <el-input v-model="form.videoProfile" type="textarea" placeholder="请输入视频简介" />
        </el-form-item>
        <el-form-item label="视频链接" prop="videoUrl">
          <el-input v-model="form.videoUrl" placeholder="请输入视频链接" />
        </el-form-item>
        <el-form-item label="视频种类" prop="videoIsHuge">
          <el-select v-model="form.videoIsHuge" placeholder="是否为带制作视频">
            <el-option
              v-for="dict in videoIsHugeOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="dict.dictValue"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="form.videoIsHuge === '1'" label="视频封面" prop="videoPic">
          <el-button v-show="!form.videoPic" type="primary" size="mini" @click="imageCropperShow(form.videoIsHuge)">
            上传图片
          </el-button>
          <el-button v-show="form.videoPic" type="primary" size="mini" @click="imageCropperShow(form.videoIsHuge)">
            更新图片
          </el-button>
          <el-button v-show="form.videoPic" type="primary" size="mini" @click="picShow(form.videoPic)">
            预览
          </el-button>
        </el-form-item>
        <el-form-item v-else-if="form.videoIsHuge === '2'" label="视频封面" prop="videoPic">
          <el-button v-show="!form.videoHugePic" type="primary" size="mini" @click="imageCropperShow(form.videoIsHuge)">
            上传图片
          </el-button>
          <el-button v-show="form.videoHugePic" type="primary" size="mini" @click="imageCropperShow(form.videoIsHuge)">
            更新图片
          </el-button>
          <el-button v-show="form.videoHugePic" type="primary" size="mini" @click="picShow(form.videoHugePic)">
            预览
          </el-button>
        </el-form-item>
        <el-form-item label="上传视频" prop="videoPath">
          <el-upload
            :action="this.upload.logo_url"
            :headers="upload.headers"
            :show-file-list="false"
            list-type="picture-card"
            :on-success="answerVideoSuccess"
            :before-upload="beforeUpload"
            :on-progress="uploadVideoProcess"
            :on-remove="handleRemove"
            :on-error="handleError"
            accept="video/mp4,video/flv,video/avi,video/wmv"
            style="margin-top: 5%;">
            <video v-if="answerVideoUrl && videoFlag === false" controls="controls" :src="answerVideoUrl" class="avatar"></video>
            <i v-if="!answerVideoUrl && videoFlag === false" class="el-icon-plus avatar-uploader-icon"></i>
            <el-progress v-if="videoFlag === true" type="circle" :percentage="percent" style="margin-top: 10px"></el-progress>
          </el-upload>
        </el-form-item>
<!--        <el-form-item label="视频分类" prop="videoClass">-->
<!--          <el-input v-model="form.videoClass" placeholder="请输入视频分类" />-->
<!--        </el-form-item>-->
        <el-form-item label="视频标签" prop="videoClass">
          <el-tag
            :key="index"
            v-for="(tag, index) in form.videoClass"
            closable
            :disable-transitions="false"
            @close="handleClose(tag)">
            {{tag}}
          </el-tag>
          <el-input
            class="input-new-tag"
            v-if="inputVisible"
            v-model="inputValue"
            ref="saveTagInput"
            size="small"
            @keyup.enter.native="handleInputConfirm"
            @blur="handleInputConfirm"
          >
          </el-input>
          <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 新标签</el-button>
        </el-form-item>

        <el-form-item label="视频作者">
          <el-select
            v-model="form.videoAuthor"
            class="filter-item"
            filterable
            remote
            reserve-keyword
            clearable
            :placeholder="form.busChannel.channelOwner"
            :remote-method="remoteMethod"
            :loading="selectLoading" value="">
            <el-option
              v-for="item in options"
              :key="item.channelId"
              :label="item.channelOwner"
              :value="item.channelId">
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <my-upload
      method="POST"
      field="file"
      v-model="upload.cropperShowHuge"
      :headers="upload.headers"
      :width=600
      :height=800
      :url= "this.upload.logo_url"
      lang-type='zh'
      img-format='jpg'
      img-bgc='#FFF'
      :no-circle=true
      @crop-upload-success="cropUploadSuccess">
    </my-upload>

    <my-upload
      method="POST"
      field="file"
      v-model="upload.cropperShowNormal"
      :headers="upload.headers"
      :width=1280
      :height=720
      :url= "this.upload.logo_url"
      lang-type='zh'
      img-format='jpg'
      img-bgc='#FFF'
      :no-circle=true
      @crop-upload-success="cropUploadSuccess">
    </my-upload>

    <el-dialog title="图片预览" :visible.sync="picVisible" width="500px" center>
      <div style="text-align: center">
        <img :src="answerPicImageUrl" alt="" class="pic-in-dialog">
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="picVisible = false">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { listVideo, getVideo, delVideo, addVideo, updateVideo, exportVideo, changeStatusVideo } from "@/api/business/video";
import { listChannel } from "@/api/business/channel";
import { getToken } from "@/utils/auth";
import 'babel-polyfill'; // es6 shim
import myUpload from 'vue-image-crop-upload';

export default {
  name: "Video",
  components: { myUpload },
  filters: {
    statusNameFilter(status) {
      const statusMap = {
        1: '普通视频',
        2: '带制作',
      }
      return statusMap[status]
    },
    statusFilter(status) {
      const statusMap = {
        1: 'success',
        2: 'primary',
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      selectLoading: false,
      options: [],
      upload: {
        headers: { Authorization: "Bearer " + getToken() },
        // 显示上传图片的弹出框
        cropperShowNormal: false,
        cropperShowHuge:false,
        // 图标路径
        logo_url: process.env.VUE_APP_BASE_API + "/common/video_matrix_upload",
      },
      videoFlag: false,
      percent: 0,
      answerVideoUrl: '',
      // 图片预览框
      picVisible: false,
      // 拼接
      answerPicImageUrl: "",
      // 路径
      video_pic_url: process.env.VUE_APP_BASE_API + "/profile/video_matrix/",
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 视频管理表格数据
      videoList: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 是否为带制作视频字典
      videoIsHugeOptions: [],
      // 输入标签
      inputVisible: false,
      // 具体内容
      inputValue: '',
      // 临时标签列表
      videoTagTemp: undefined,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        videoTitle: null,
        videoProfile: null,
        videoClass: null,
        channelOwner: null
      },
      // 第二查询参数
      searchQueryParams: {
        pageNum: 1,
        pageSize: 100,
        channelOwner: null,
      },
      // 表单参数
      form: {
        busChannel:{
          channelOwner: null
        }
      },
      // 表单校验
      rules: {
        videoTitle: [{
          required: true,
          message: '标题为必填项',
          trigger: 'blur'
        }],
        videoPath: [{
          required: true,
          message: '视频必须上传',
          trigger: 'change'
        }],
        videoPic: [{
          required: true,
          message: '封面图为必填项',
          trigger: 'change'
        }],
        videoHugePic: [{
          required: true,
          message: '封面图为必填项',
          trigger: 'change'
        }],
        videoIsHuge: [{
          required: true,
          message: '分类为必填项',
          trigger: 'change'
        }],
      }
    };
  },
  created() {
    this.getList();
    this.getDicts("bus_video_type").then(response => {
      this.videoIsHugeOptions = response.data;
    });
  },
  methods: {
    /** 查询视频管理列表 */
    getList() {
      this.loading = true;
      listVideo(this.queryParams).then(response => {
        this.videoList = response.rows;
        Object.keys(this.videoList).forEach(key => (this.videoList[key].videoClass = JSON.parse(this.videoList[key].videoClass)));
        this.total = response.total;
        this.loading = false;
      });
    },
    // 选择频道时，用于根据关键字查找活动
    remoteMethod (query) {
      if (query === '') {
        this.options = []
        return
      }
      this.selectLoading = true;
      this.searchQueryParams.channelOwner = query;
      listChannel(this.searchQueryParams).then(data => {
        this.selectLoading = false;
        this.options = data.rows;
      })
    },
    // 是否为带制作视频字典翻译
    videoIsHugeFormat(row, column) {
      return this.selectDictLabel(this.videoIsHugeOptions, row.videoIsHuge);
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        videoId: null,
        videoTitle: null,
        videoProfile: null,
        videoUrl: null,
        videoPic: null,
        videoStatus: "0",
        videoClass: [],
        videoAuthor: null,
        videoIsHuge: null,
        videoHugePic: null,
        videoPath: null,
        videoJson: null,
        busChannel: {
          channelOwner: null
        }
      };
      this.answerPicImageUrl = null;
      this.answerVideoUrl = null;
      this.resetForm("form");
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.videoId)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加视频管理";
    },
    /** 改变视频状态 */
    updateVideoStatus(row_temp) {
      const new_row = {};
      new_row.videoStatus = row_temp.videoStatus;
      new_row.videoId = row_temp.videoId;
      // const videoId = row.videoId || this.ids;
      changeStatusVideo(new_row).then(response => {
        if (response.code === 200){
          this.$message({
            message: '状态已更新~',
            type: 'success'
          })
        }
        else{
          this.$message({
            message: '服务器开小差了……',
            type: 'warning'
          })
        }
        this.getList();
      });
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const videoId = row.videoId || this.ids;
      getVideo(videoId).then(response => {
        this.form = response.data;
        this.videoTagTemp = this.form.videoClass;
        this.form.videoClass = JSON.parse(this.videoTagTemp);
        if(this.form.videoPath){
          this.answerVideoUrl = this.video_pic_url + this.form.videoPath
        }
        this.open = true;
        this.title = "修改视频管理";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          this.open = false;
          if (this.form.videoId != null) {
            this.videoTagTemp = this.form.videoClass;
            this.form.videoClass = JSON.stringify(this.videoTagTemp);
            updateVideo(this.form).then(response => {
              if (response.code === 200) {
                this.msgSuccess("修改成功");
                this.getList();
              }
            });
          } else {
            this.videoTagTemp = this.form.videoClass;
            this.form.videoClass = JSON.stringify(this.videoTagTemp);
            addVideo(this.form).then(response => {
              if (response.code === 200) {
                this.msgSuccess("新增成功");
                this.getList();
              }
            });
            this.form.videoClass = this.videoTagTemp;
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const videoIds = row.videoId || this.ids;
      this.$confirm('是否确认删除视频管理编号为"' + videoIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return delVideo(videoIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        }).catch(function() {});
    },
    /** 导出按钮操作 */
    handleExport() {
      const queryParams = this.queryParams;
      this.$confirm('是否确认导出所有视频管理数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return exportVideo(queryParams);
        }).then(response => {
          this.download(response.msg);
        }).catch(function() {});
    },
    // 显示图片上传模块
    imageCropperShow(isHuge) {
      if (isHuge === "1"){
        this.upload.cropperShowNormal = !this.upload.cropperShowNormal
      }
      else{
        this.upload.cropperShowHuge = !this.upload.cropperShowHuge
      }

    },
    // 图片上传成功后执行
    cropUploadSuccess(jsonData, field){
      if (this.form.videoIsHuge==='1'){
        this.form.videoPic = jsonData.fileName
      }
      else{
        this.form.videoHugePic = jsonData.fileName
      }
      // console.log(jsonData)
    },
    picShow(pic) {
      this.picVisible = !this.picVisible;
      this.answerPicImageUrl = this.video_pic_url + pic
    },
    uploadVideoProcess(event, file, fileList){
      this.videoFlag = true;
      this.percent = Math.floor(event.percent)
    },
    handleRemove(file, fileList) {
      this.temp.videoPath = '';
    },
    answerVideoSuccess(res, file){
      this.form.videoPath = res.fileName;
      this.answerVideoUrl = this.video_pic_url + res.fileName;
      this.videoFlag = false;
    },
    beforeUpload (file) {
      // 只允许上传2GB以内大小的图片
      const isLt4G = file.size / 1024 / 1024 / 1024 < 4;
      if (!isLt4G) {
        this.$message.error('上传视频大小不能超过4GB!');
      }
      return isLt4G;
    },
    handleError(err, file, fileList) {
      // 上传失败异常处理
      const error = JSON.parse(JSON.stringify(err));
      console.log(err)
      console.log(error)
      this.$message.error(error.status.toString());
      this.videoFlag = false;
      this.percent = 0;
    },
    handleClose(tag) {
      this.form.videoClass.splice(this.form.videoClass.indexOf(tag), 1);
    },
    showInput() {
      this.inputVisible = true;
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.form.videoClass.push(inputValue);
      }
      this.inputVisible = false;
      this.inputValue = '';
    },
  }
};
</script>
<style>
  /*.avatar-uploader .el-upload {*/
  /*  border: 1px dashed #d9d9d9;*/
  /*  border-radius: 6px;*/
  /*  cursor: pointer;*/
  /*  position: relative;*/
  /*  overflow: hidden;*/
  /*}*/

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }

  .avatar-uploader-icon {
    line-height: 140px;
  }

  .avatar {
    height: 144px;
  }

  .image-preview {
    width: 178px;
    height: 178px;
    position: relative;
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    float: left;
  }

  .image-preview .image-preview-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
  }

  .image-preview .image-preview-wrapper img {
    width: 100%;
    height: 100%;
  }

  .image-preview .image-preview-action {
    position: absolute;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    cursor: default;
    text-align: center;
    color: #fff;
    opacity: 0;
    font-size: 20px;
    background-color: rgba(0, 0, 0, .5);
    transition: opacity .3s;
    cursor: pointer;
    text-align: center;
    line-height: 200px;
  }
  .image-preview .image-preview-action .el-icon-delete {
    font-size: 32px;
  }
  .image-preview:hover .image-preview-action {
    opacity: 1;
  }
  .el-upload--picture-card{
    display: block;
    width: 258px;
    height: 146px;
    overflow: hidden;
  }
  .input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }
  .el-tag + .el-tag {
    margin-left: 10px;
  }

  .button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }

</style>
