<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="频道名称" prop="channelOwner">
        <el-input
          v-model="queryParams.channelOwner"
          placeholder="请输入频道所有者"
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
          v-hasPermi="['business:channel:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['business:channel:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['business:channel:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['business:channel:export']"
        >导出</el-button>
      </el-col>
	  <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="channelList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="频道图标" align="center" prop="channelLogo">
        <template slot-scope="scope">
          <img :src="channel_pic_url + scope.row.channelLogo" alt="" class="pic-in-list">
        </template>
      </el-table-column>
      <el-table-column label="频道所有者" align="center" prop="channelOwner">
        <template slot-scope="scope">
          <a v-if="scope.row.channelUrl" target="_blank" :href="scope.row.channelUrl" class="link-type" style="margin-right: 10px;">
            <span>{{ scope.row.channelOwner }}</span>
          </a>
          <span v-else>{{ scope.row.channelOwner }}</span>
        </template>
      </el-table-column>
      <el-table-column label="频道视频数" align="center" prop="channelVideoCount" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['business:channel:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['business:channel:remove']"
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

    <!-- 添加或修改频道管理对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="频道链接" prop="channelUrl">
          <el-input v-model="form.channelUrl" placeholder="请输入频道链接" />
        </el-form-item>
        <el-form-item label="频道名称" prop="channelOwner">
          <el-input v-model="form.channelOwner" placeholder="请输入频道所有者" />
        </el-form-item>
        <el-form-item label="频道图标" prop="channelLogo">
          <el-button v-show="!form.channelLogo" type="primary" size="mini" @click="imageCropperShow()">
            上传图片
          </el-button>
          <el-button v-show="form.channelLogo" type="primary" size="mini" @click="imageCropperShow()">
            更新图片
          </el-button>
          <el-button v-show="form.channelLogo" type="primary" size="mini" @click="picShow(form.channelLogo)">
            预览
          </el-button>
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
      v-model="upload.cropperShow"
      :headers="upload.headers"
      :width=400
      :height=400
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
import { getToken } from "@/utils/auth";
import { listChannel, getChannel, delChannel, addChannel, updateChannel, exportChannel } from "@/api/business/channel";
import 'babel-polyfill'; // es6 shim
import myUpload from 'vue-image-crop-upload';

export default {
  name: "Channel",
  components: { myUpload },
  data() {
    return {
      upload: {
        headers: { Authorization: "Bearer " + getToken() },
        // 显示上传图片的弹出框
        cropperShow: false,
        // 图标路径
        logo_url: process.env.VUE_APP_BASE_API + "/common/video_matrix_upload",
      },
      // 图片预览框
      picVisible: false,
      // 拼接
      answerPicImageUrl: "",
      // 路径
      channel_pic_url: process.env.VUE_APP_BASE_API + "/profile/video_matrix/",
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
      // 频道管理表格数据
      channelList: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        channelOwner: null,
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询频道管理列表 */
    getList() {
      this.loading = true;
      listChannel(this.queryParams).then(response => {
        this.channelList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        channelId: null,
        channelUrl: null,
        channelLogo: null,
        channelOwner: null,
        channelVideoCount: null
      };
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
      this.ids = selection.map(item => item.channelId)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加频道管理";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const channelId = row.channelId || this.ids
      getChannel(channelId).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改频道管理";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.channelId != null) {
            updateChannel(this.form).then(response => {
              if (response.code === 200) {
                this.msgSuccess("修改成功");
                this.open = false;
                this.getList();
              }
            });
          } else {
            addChannel(this.form).then(response => {
              if (response.code === 200) {
                this.msgSuccess("新增成功");
                this.open = false;
                this.getList();
              }
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const channelIds = row.channelId || this.ids;
      this.$confirm('是否确认删除频道管理编号为"' + channelIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return delChannel(channelIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        }).catch(function() {});
    },
    /** 导出按钮操作 */
    handleExport() {
      const queryParams = this.queryParams;
      this.$confirm('是否确认导出所有频道管理数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return exportChannel(queryParams);
        }).then(response => {
          this.download(response.msg);
        }).catch(function() {});
    },
    // 显示图片上传模块
    imageCropperShow() {
      this.upload.cropperShow = !this.upload.cropperShow
    },
    // 图片上传成功后执行
    cropUploadSuccess(jsonData, field){
      // console.log(jsonData)
      this.form.channelLogo = jsonData.fileName
    },
    picShow(pic) {
      this.picVisible = !this.picVisible
      this.answerPicImageUrl = this.channel_pic_url + pic
    },
  }
};
</script>
