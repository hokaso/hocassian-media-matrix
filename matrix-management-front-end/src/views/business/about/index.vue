<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="组织简介" prop="aboutInfo">
        <el-input
          v-model="queryParams.aboutInfo"
          placeholder="请输入组织简介"
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
          v-hasPermi="['business:about:add']"
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
          v-hasPermi="['business:about:edit']"
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
          v-hasPermi="['business:about:remove']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['business:about:export']"
        >导出
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="aboutList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="组织名称" align="center" prop="aboutName" :show-overflow-tooltip="true"/>
      <el-table-column label="组织关键字" align="center" prop="aboutKeyword" :show-overflow-tooltip="true"/>
      <el-table-column label="组织简介" align="center" prop="aboutInfo" :show-overflow-tooltip="true"/>
      <el-table-column label="组织宣言" align="center" prop="aboutDeclaration" :show-overflow-tooltip="true"/>
      <el-table-column label="联系方式" align="center" prop="aboutContact" :show-overflow-tooltip="true"/>
      <el-table-column label="页脚声明" align="center" prop="aboutCopyright" :show-overflow-tooltip="true"/>
      <el-table-column label="页脚备案" align="center" prop="aboutRecord" :show-overflow-tooltip="true"/>
      <el-table-column label="是否上架" align="center" prop="aboutStatus" :formatter="aboutStatusFormat"/>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['business:about:edit']"
          >修改
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['business:about:remove']"
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

    <!-- 添加或修改信息管理对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="组织名称" prop="aboutName">
          <el-input v-model="form.aboutName" placeholder="请输入组织名称"/>
        </el-form-item>
        <el-form-item label="关键字" prop="aboutKeyword">
          <el-input v-model="form.aboutKeyword" placeholder="请输入组织关键字"/>
        </el-form-item>
        <el-form-item label="组织简介" prop="aboutInfo">
          <el-input v-model="form.aboutInfo" type="textarea" placeholder="请输入组织简介"/>
        </el-form-item>
        <el-form-item label="组织宣言" prop="aboutDeclaration">
          <el-input v-model="form.aboutDeclaration" type="textarea" placeholder="请输入组织宣言"/>
        </el-form-item>
        <el-form-item label="大众平台" prop="aboutQrcode">
          <!--          <el-input v-model="form.aboutQrcode" placeholder="请输入大众平台" />-->
          <el-upload
            class="upload-demo"
            :action="uploadUrl"
            :headers="headers"
            :file-list="qrListShow"
            :on-success="uploadSuccess"
            :on-remove="handleRemove"
            list-type="picture">
            <el-button size="small" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">只能上传jpg/png文件</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="联系方式" prop="aboutContact">
          <el-input v-model="form.aboutContact" type="textarea" placeholder="请输入联系方式"/>
        </el-form-item>
        <el-form-item label="页脚声明" prop="aboutCopyright">
          <el-input v-model="form.aboutCopyright" type="textarea" placeholder="示例：Copyright@ 2018-2021 同和新媒体矩阵·版权所有"/>
        </el-form-item>
        <el-form-item label="页脚备案" prop="aboutRecord">
          <el-input v-model="form.aboutRecord" placeholder="示例：粤ICP备18016897号"/>
        </el-form-item>
        <el-form-item label="组织图标" prop="aboutIcon">
          <el-upload
            class="avatar-uploader"
            :action="uploadUrl"
            :headers="headers"
            :show-file-list="false"
            :on-success="handleLogoSuccess"
            :before-upload="beforeLogoUpload">
            <img v-if="form.aboutIcon" :src="logoUrl" class="web-logo" alt="">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            <div slot="tip" class="el-upload__tip">只能上传png文件，建议尺寸：520*130，文件大小不超过200k</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="是否上架" prop="aboutStatus">
          <el-select v-model="form.aboutStatus" placeholder="请选择是否上架">
            <el-option
              v-for="dict in aboutStatusOptions"
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
  </div>
</template>

<script>
  import {listAbout, getAbout, delAbout, addAbout, updateAbout, exportAbout} from "@/api/business/about";
  import {getToken} from "@/utils/auth";

  export default {
    name: "About",
    data() {
      return {
        logoUrl: "",
        headers: {Authorization: "Bearer " + getToken()},
        uploadUrl: process.env.VUE_APP_BASE_API + "/common/video_matrix_upload",
        // 路径
        aboutPicUrl: process.env.VUE_APP_BASE_API + "/profile/video_matrix/",
        qrList: [],
        qrListShow: [],
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
        // 信息管理表格数据
        aboutList: [],
        // 弹出层标题
        title: "",
        // 是否显示弹出层
        open: false,
        // 是否上架字典
        aboutStatusOptions: [],
        // 查询参数
        queryParams: {
          pageNum: 1,
          pageSize: 10,
          aboutInfo: null,
        },
        // 表单参数
        form: {},
        // 表单校验
        rules: {}
      };
    },
    created() {
      this.getList();
      this.getDicts("material_public").then(response => {
        this.aboutStatusOptions = response.data;
      });
    },
    methods: {
      /** 查询信息管理列表 */
      getList() {
        this.loading = true;
        listAbout(this.queryParams).then(response => {
          this.aboutList = response.rows;
          this.total = response.total;
          this.loading = false;
        });
      },
      // 是否上架字典翻译
      aboutStatusFormat(row, column) {
        return this.selectDictLabel(this.aboutStatusOptions, row.aboutStatus);
      },
      // 取消按钮
      cancel() {
        this.open = false;
        this.reset();
      },
      // 表单重置
      reset() {
        this.form = {
          aboutId: null,
          aboutInfo: null,
          aboutKeyword: null,
          aboutDeclaration: null,
          aboutQrcode: null,
          aboutName: null,
          aboutContact: null,
          aboutIcon: null,
          aboutStatus: "0",
          aboutCopyright: null,
          aboutRecord: null,
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
        this.ids = selection.map(item => item.aboutId)
        this.single = selection.length !== 1
        this.multiple = !selection.length
      },
      /** 新增按钮操作 */
      handleAdd() {
        this.reset();
        this.open = true;
        this.title = "添加信息管理";
      },
      /** 修改按钮操作 */
      handleUpdate(row) {
        this.reset();
        this.qrListShow = []
        const aboutId = row.aboutId || this.ids
        getAbout(aboutId).then(response => {
          this.form = response.data;
          this.qrList = JSON.parse(this.form.aboutQrcode)
          // console.log(this.qrList)
          if (this.qrList != null) {
            Object.keys(this.qrList).forEach(key => {
              this.qrListShow.push({
                name: this.qrList[key].name,
                url: this.aboutPicUrl + this.qrList[key].url
              })
            })
          }

          this.logoUrl = this.aboutPicUrl + this.form.aboutIcon

          this.open = true;
          this.title = "修改信息管理";
        });
      },
      /** 提交按钮 */
      submitForm() {
        this.$refs["form"].validate(valid => {
          if (valid) {
            if (this.form.aboutId != null) {
              this.form.aboutQrcode = JSON.stringify(this.qrList)
              updateAbout(this.form).then(response => {
                if (response.code === 200) {
                  this.msgSuccess("修改成功");
                  this.open = false;
                  this.getList();
                }
              });
            } else {
              addAbout(this.form).then(response => {
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
        const aboutIds = row.aboutId || this.ids;
        this.$confirm('是否确认删除信息管理编号为"' + aboutIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return delAbout(aboutIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        }).catch(function () {
        });
      },
      /** 导出按钮操作 */
      handleExport() {
        const queryParams = this.queryParams;
        this.$confirm('是否确认导出所有信息管理数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return exportAbout(queryParams);
        }).then(response => {
          this.download(response.msg);
        }).catch(function () {
        });
      },
      uploadSuccess(response, file, fileList) {
        this.qrList = []
        console.log(response);
        // console.log(file);
        console.log(fileList);
        Object.keys(fileList).forEach(key => {
          if (fileList[key].hasOwnProperty("response")) {
            this.qrList.push({
              name: fileList[key].name,
              url: fileList[key].response.fileName
            })
          } else {
            const tempList = fileList[key].url.split("/")
            this.qrList.push({
              name: fileList[key].name,
              url: tempList[tempList.length - 1]
            })
          }
        })
      },
      handleLogoSuccess(response, file, fileList) {
        this.logoUrl = this.aboutPicUrl + response.fileName
        this.form.aboutIcon = response.fileName
      },
      beforeLogoUpload(file) {
        const isPNG = file.type === 'image/png';
        const isLt2K = file.size / 1024 / 1024 < 0.2;

        if (!isPNG) {
          this.$message.error('上传头像图片只能是PNG格式！');
        }
        if (!isLt2K) {
          this.$message.error('上传头像图片大小不能超过200k！');
        }
        return isPNG && isLt2K;
      },
      handleRemove(file, fileList) {
        this.qrList = []
        // console.log(file);
        console.log(fileList);
        Object.keys(fileList).forEach(key => {
          if (fileList[key].hasOwnProperty("response")) {
            this.qrList.push({
              name: fileList[key].name,
              url: fileList[key].response.fileName
            })
          } else {
            const tempList = fileList[key].url.split("/")
            this.qrList.push({
              name: fileList[key].name,
              url: tempList[tempList.length - 1]
            })
          }
        })
      }
    }
  };
</script>

<style>
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }

  .web-logo {
    width: 100%;
    display: block;
  }
</style>
