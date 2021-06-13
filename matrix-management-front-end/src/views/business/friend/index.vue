<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="友链名称" prop="friendName">
        <el-input
          v-model="queryParams.friendName"
          placeholder="请输入友链名称"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="友链信息" prop="friendInfo">
        <el-input
          v-model="queryParams.friendInfo"
          placeholder="请输入友链信息"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="友链类型" prop="friendType">
        <el-select v-model="queryParams.friendType" placeholder="请选择友链类型" clearable size="small">
          <el-option
            v-for="dict in friendTypeOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="友链状态" prop="friendStatus">
        <el-select v-model="queryParams.friendStatus" placeholder="请选择友链状态" clearable size="small">
          <el-option
            v-for="dict in friendStatusOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
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
          v-hasPermi="['business:friend:add']"
        >新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['business:friend:edit']"
        >修改
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['business:friend:remove']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['business:friend:export']"
        >导出
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="friendList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="友链名称" align="center" prop="friendName">
        <template slot-scope="scope">
          <a v-if="scope.row.friendUrl" target="_blank" :href="scope.row.friendUrl" class="link-type" style="margin-right: 10px;">
            <span>{{ scope.row.friendName }}</span>
          </a>
          <span v-else>{{ scope.row.friendName }}</span>
        </template>
      </el-table-column>
      <el-table-column label="友链信息" align="center" prop="friendInfo" :show-overflow-tooltip="true"/>
      <el-table-column label="友链图片" align="center" prop="friendPic">
        <template slot-scope="scope">
          <img :src="friends_pic_url + scope.row.friendPic" alt="" class="pic-in-list">
        </template>
      </el-table-column>
      <el-table-column label="友链类型" align="center" prop="friendType" :formatter="friendTypeFormat"/>
      <el-table-column label="友链状态" align="center" prop="friendStatus" :formatter="friendStatusFormat"/>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['business:friend:edit']"
          >修改
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['business:friend:remove']"
          >删除
          </el-button>
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

    <el-dialog title="图片预览" :visible.sync="picVisible" width="500px" center>
      <div style="text-align: center">
        <img :src="answerPicImageUrl" alt="" class="pic-in-dialog">
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="picVisible = false">确定</el-button>
      </span>
    </el-dialog>

    <!-- 添加或修改友情链接对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="友链名称" prop="friendName">
          <el-input v-model="form.friendName" placeholder="请输入友链名称"/>
        </el-form-item>
        <el-form-item label="友链信息" prop="friendInfo">
          <el-input v-model="form.friendInfo" placeholder="请输入友链信息" type="textarea"/>
        </el-form-item>
        <el-form-item label="友链链接" prop="friendUrl">
          <el-input v-model="form.friendUrl" placeholder="请输入友链链接"/>
        </el-form-item>
        <el-form-item label="友链图片" prop="friendPic">
          <el-button v-show="!form.friendPic" type="primary" size="mini" @click="imageCropperShow()">
            上传图片
          </el-button>
          <el-button v-show="form.friendPic" type="primary" size="mini" @click="imageCropperShow()">
            更新图片
          </el-button>
          <el-button v-show="form.friendPic" type="primary" size="mini" @click="picShow(form.friendPic)">
            预览
          </el-button>
        </el-form-item>
<!--        <el-form-item label="友链图片" prop="friendPic">-->
<!--          <el-input v-model="form.friendPic" placeholder="请输入友链图片"/>-->
<!--        </el-form-item>-->
        <el-form-item label="友链类型" prop="friendType">
          <el-select v-model="form.friendType" placeholder="请选择友链类型">
            <el-option
              v-for="dict in friendTypeOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="dict.dictValue"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="友链状态" prop="friendStatus">
          <el-select v-model="form.friendStatus" placeholder="请选择友链状态">
            <el-option
              v-for="dict in friendStatusOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="dict.dictValue"
            ></el-option>
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
      v-model="upload.cropperShow"
      :headers="upload.headers"
      :width=300
      :height=300
      :url="this.upload.logo_url"
      lang-type='zh'
      img-format='jpg'
      img-bgc='#FFF'
      :no-circle=true
      @crop-upload-success="cropUploadSuccess">
    </my-upload>

  </div>
</template>

<script>
  import {listFriend, getFriend, delFriend, addFriend, updateFriend, exportFriend} from "@/api/business/friend"
  import {getToken} from "@/utils/auth";
  import 'babel-polyfill'; // es6 shim
  import myUpload from 'vue-image-crop-upload';

  export default {
    name: "Friend",
    components: {myUpload},
    data() {
      return {
        upload: {
          headers: {Authorization: "Bearer " + getToken()},
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
        friends_pic_url: process.env.VUE_APP_BASE_API + "/profile/video_matrix/",
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
        // 友情链接表格数据
        friendList: [],
        // 弹出层标题
        title: "",
        // 是否显示弹出层
        open: false,
        // 友链类型字典
        friendTypeOptions: [],
        // 友链状态字典
        friendStatusOptions: [],
        // 查询参数
        queryParams: {
          pageNum: 1,
          pageSize: 10,
          friendName: null,
          friendInfo: null,
          friendType: null,
          friendStatus: null
        },
        // 表单参数
        form: {},
        // 表单校验
        rules: {}
      };
    },
    created() {
      this.getList();
      this.getDicts("promotion_type").then(response => {
        this.friendTypeOptions = response.data;
      });
      this.getDicts("material_public").then(response => {
        this.friendStatusOptions = response.data;
      });
    },
    methods: {
      /** 查询友情链接列表 */
      getList() {
        this.loading = true;
        listFriend(this.queryParams).then(response => {
          this.friendList = response.rows;
          this.total = response.total;
          this.loading = false;
        });
      },
      // 友链类型字典翻译
      friendTypeFormat(row, column) {
        return this.selectDictLabel(this.friendTypeOptions, row.friendType);
      },
      // 友链状态字典翻译
      friendStatusFormat(row, column) {
        return this.selectDictLabel(this.friendStatusOptions, row.friendStatus);
      },
      // 取消按钮
      cancel() {
        this.open = false;
        this.reset();
      },
      // 表单重置
      reset() {
        this.form = {
          friendId: null,
          friendName: null,
          friendInfo: null,
          friendUrl: null,
          friendPic: null,
          friendType: "0",
          friendStatus: "0"
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
        this.ids = selection.map(item => item.friendId)
        this.single = selection.length !== 1
        this.multiple = !selection.length
      },
      /** 新增按钮操作 */
      handleAdd() {
        this.reset();
        this.open = true;
        this.title = "添加友情链接";
      },
      /** 修改按钮操作 */
      handleUpdate(row) {
        this.reset();
        const friendId = row.friendId || this.ids
        getFriend(friendId).then(response => {
          this.form = response.data;
          this.open = true;
          this.title = "修改友情链接";
        });
      },
      /** 提交按钮 */
      submitForm() {
        this.$refs["form"].validate(valid => {
          if (valid) {
            if (this.form.friendId != null) {
              updateFriend(this.form).then(response => {
                if (response.code === 200) {
                  this.msgSuccess("修改成功");
                  this.open = false;
                  this.getList();
                }
              });
            } else {
              addFriend(this.form).then(response => {
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
        const friendIds = row.friendId || this.ids;
        this.$confirm('是否确认删除友情链接编号为"' + friendIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return delFriend(friendIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        }).catch(function () {
        });
      },
      /** 导出按钮操作 */
      handleExport() {
        const queryParams = this.queryParams;
        this.$confirm('是否确认导出所有友情链接数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return exportFriend(queryParams);
        }).then(response => {
          this.download(response.msg);
        }).catch(function () {
        });
      },
      // 图片上传成功后执行
      cropUploadSuccess(jsonData, field) {
        this.form.friendPic = jsonData.fileName
      },
      // 显示图片上传模块
      imageCropperShow() {
        this.upload.cropperShow = !this.upload.cropperShow
      },
      picShow(pic) {
        this.picVisible = !this.picVisible;
        this.answerPicImageUrl = this.friends_pic_url + pic
      },
    }
  };
</script>
