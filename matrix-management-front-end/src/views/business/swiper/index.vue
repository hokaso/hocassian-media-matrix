<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="按名查找" prop="swiperName">
        <el-input
          v-model="queryParams.swiperName"
          placeholder="请输入轮播图名称"
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
          v-hasPermi="['business:swiper:edit']"
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
          v-hasPermi="['business:swiper:remove']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['business:swiper:export']"
        >导出
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table-editabled v-model="swiperList" :columns="['swiperName', 'swiperPic', 'swiperStatus']" ref="editTable">
      <el-table v-loading="loading" :data="swiperList" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center"/>
        <el-table-column label="轮播图名称" align="center" prop="swiperName">
          <template slot-scope="{row}">
            <el-table-editabled-cell :row="row" prop="swiperName">
              <template slot-scope="{ rowStates, validateOwn }">
                <span v-show="!rowStates.editing">{{row.swiperName}}</span>
                <el-input v-show="rowStates.editing" v-model="row.swiperName" clearable @input="validateOwn">
                </el-input>
              </template>
            </el-table-editabled-cell>
          </template>
        </el-table-column>
        <el-table-column label="轮播图详情" align="center" prop="swiperPic">
          <template slot-scope="{row}">
            <el-table-editabled-cell :row="row" prop="swiperPic">
              <template slot-scope="{ rowStates, validateOwn }">
                <el-button v-if="rowStates.editing && !row.swiperPic" type="primary" size="mini"
                           @click="imageCropperShow()">
                  上传图片
                </el-button>
                <el-button v-if="rowStates.editing && row.swiperPic" type="primary" size="mini"
                           @click="imageCropperShow()">
                  更新图片
                </el-button>
                <img v-if="!rowStates.editing && row.swiperPic" :src="swiper_pic_url + row.swiperPic"
                     alt="" class="pic-in-list-swiper">
              </template>
            </el-table-editabled-cell>
          </template>
        </el-table-column>
        <el-table-column label="轮播图状态" align="center" prop="swiperStatus">
          <template slot-scope="{row}">
            <el-switch
              v-model="row.swiperStatus"
              active-value="1"
              inactive-value="0"
              @change="updateSwiperStatus(row)"
              v-hasPermi="['business:swiper:status']"
            ></el-switch>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
          <template slot-scope="{row}">
            <el-table-editabled-cell :row="row">
              <template slot-scope="{ rowStates }">
                <el-button
                  v-if="!rowStates.editing && row.swiperId"
                  size="mini"
                  type="text"
                  icon="el-icon-edit"
                  @click="handleUpdate(row)"
                  v-hasPermi="['business:swiper:edit']"
                >修改
                </el-button>
                <el-button
                  v-if="!rowStates.editing && row.swiperId"
                  size="mini"
                  type="text"
                  icon="el-icon-delete"
                  @click="handleDelete(row)"
                  v-hasPermi="['business:swiper:remove']"
                >删除
                </el-button>
                <el-button
                  v-if="rowStates.editing && !row.swiperId"
                  size="mini"
                  type="text"
                  icon="el-icon-edit"
                  @click="submitForm(row)"
                >保存
                </el-button>
                <el-button
                  v-if="rowStates.editing && !row.swiperId"
                  size="mini"
                  type="text"
                  icon="el-icon-edit"
                  @click="handleCancel(row)"
                >取消
                </el-button>
                <el-button
                  v-if="rowStates.editing && row.swiperId"
                  size="mini"
                  type="text"
                  icon="el-icon-edit"
                  @click="submitForm(row)"
                >更新
                </el-button>
                <el-button
                  v-if="rowStates.editing && row.swiperId"
                  size="mini"
                  type="text"
                  icon="el-icon-edit"
                  @click="handleCancel(row)"
                >撤销
                </el-button>
              </template>
            </el-table-editabled-cell>
          </template>
        </el-table-column>
      </el-table>
    </el-table-editabled>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <my-upload
      method="POST"
      field="file"
      v-model="upload.cropperShow"
      :headers="upload.headers"
      :width=1920
      :height=450
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
  import {
    listSwiper,
    getSwiper,
    delSwiper,
    addSwiper,
    updateSwiper,
    exportSwiper,
    changeStatusSwiper
  } from "@/api/business/swiper";

  import { getToken } from "@/utils/auth";
  import 'babel-polyfill'; // es6 shim
  import myUpload from 'vue-image-crop-upload';

  export default {
    name: "Swiper",
    components: {myUpload},
    computed: {
      editTable() {
        return this.$refs.editTable
      }
    },
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
        swiper_pic_url: process.env.VUE_APP_BASE_API + "/profile/video_matrix/",
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
        // 主页轮播图表格数据
        swiperList: [],
        // 弹出层标题
        title: "",
        // 是否显示弹出层
        open: false,
        // 查询参数
        queryParams: {
          pageNum: 1,
          pageSize: 10,
          swiperName: null,
        },
        // 表单参数
        form: {},
        // 表单校验
        rules: {}
      };
    },
    created() {
      this.getList();
    },
    methods: {
      /** 查询主页轮播图列表 */
      getList() {
        this.loading = true;
        listSwiper(this.queryParams).then(response => {
          this.swiperList = response.rows;
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
          swiperId: null,
          swiperPic: null,
          swiperName: null,
          swiperStatus: "0",
          createAt: null,
          createBy: null,
          updateAt: null,
          updateBy: null
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
        this.ids = selection.map(item => item.id);
        this.single = selection.length !== 1;
        this.multiple = !selection.length;
      },
      /** 新增按钮操作 */
      handleAdd() {
        this.reset();
        const newRow = this.form;
        this.editTable.newRows([newRow]);
      },
      /** 改变状态 */
      updateSwiperStatus(row) {
        changeStatusSwiper(row).then(response => {
          if (response.code === 200) {
            this.$message({
              message: '状态已更新~',
              type: 'success'
            })
          } else {
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
        this.editTable.editRows([row])
      },
      /** 提交按钮 */
      submitForm(row) {
        this.$refs.editTable.validateRows([row],valid => {
          if (valid) {
            row.swiperPic = this.form.swiperPic;
            if (row.swiperId != null) {
              updateSwiper(row).then(response => {
                if (response.code === 200) {
                  this.msgSuccess("修改成功");
                  this.open = false;
                  this.getList();
                }
              });
            } else {
              addSwiper(row).then(response => {
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
      /** 取消操作 */
      handleCancel(row) {
        if (row.swiperId != null) {
          this.editTable.cancelRows([row])
        }
        else{
          this.editTable.delRows([row])
        }
      },
      /** 删除按钮操作 */
      handleDelete(row) {
        const swiperIds = row.swiperId || this.ids;
        this.$confirm('是否确认删除主页轮播图编号为"' + swiperIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return delSwiper(swiperIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        }).catch(function () {
        });
      },
      /** 导出按钮操作 */
      handleExport() {
        const queryParams = this.queryParams;
        this.$confirm('是否确认导出所有主页轮播图数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return exportSwiper(queryParams);
        }).then(response => {
          this.download(response.msg);
        }).catch(function () {
        });
      },
      // 图片上传成功后执行
      cropUploadSuccess(jsonData, field) {
        this.form.swiperPic = jsonData.fileName
      },
      // 显示图片上传模块
      imageCropperShow() {
        this.upload.cropperShow = !this.upload.cropperShow
      },
    }
  };
</script>
