<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="图片标签" prop="imageTag">
        <el-input
          v-model="queryParams.imageTag"
          placeholder="请输入图片素材标签"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="图片类型" prop="imageType">
        <el-select v-model="queryParams.imageType" placeholder="请选择图片类型" clearable size="small">
          <el-option
            v-for="dict in imageTypeOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="素材版权" prop="isCopyright">
        <el-select v-model="queryParams.isCopyright" placeholder="请选择素材版权" clearable size="small">
          <el-option
            v-for="dict in isCopyrightOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="是否上架" prop="isShow">
        <el-select v-model="queryParams.isShow" placeholder="请选择是否上架" clearable size="small">
          <el-option
            v-for="dict in isShowOptions"
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
          v-if="this.importImage === 1"
          type="primary"
          disabled
          icon="el-icon-loading"
          size="mini"
          v-hasPermi="['material:image:add']"
        >导入素材
        </el-button>
        <el-button
          v-else
          type="primary"
          icon="el-icon-plus"
          size="mini"
          @click="handleOption(1)"
          v-hasPermi="['material:image:add']"
        >导入素材
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['material:image:edit']"
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
          v-hasPermi="['material:image:remove']"
        >删除
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>
    <el-table v-loading="loading" :data="imageList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="图片预览" align="center" prop="imagePath">
        <template slot-scope="scope">
          <div
            class="image__block"
            @mouseover="showPic(pic_url + scope.row.imagePath + '_mini.jpg')"
            @mouseout="hidePic()">
            <img :src="pic_url + scope.row.imagePath + '_mini.jpg'" alt="" class="pic-in-list">
          </div>
        </template>
      </el-table-column>
      <el-table-column label="图片标签" align="center" prop="imageTag" min-width="100px">
        <template slot-scope="scope">
          <el-tag class="mini-tag" v-for="ikey in scope.row.imageTagTemp" :key="ikey" type="success">
            {{ikey}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="图片打分" align="center" prop="imageMark"/>
      <!--      <el-table-column label="图片状态" align="center" prop="imageStatus" />-->
      <el-table-column label="图片类型" align="center" prop="imageType" :formatter="imageTypeFormat">
        <template slot-scope="scope">
          <div class="tag-up">
            <el-tag :type="scope.row.imageType | typeFilter">
              {{ scope.row.imageType | typeNameFilter}}
            </el-tag>
          </div>
          <el-switch
            v-model="scope.row.imageType"
            active-value="0"
            inactive-value="1"
            @change="ImageSwitch(scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="素材版权" align="center" prop="isCopyright" :formatter="isCopyrightFormat">
        <template slot-scope="scope">
          <div class="tag-up">
            <el-tag :type="scope.row.isCopyright | copyFilter">
              {{ scope.row.isCopyright | copyNameFilter}}
            </el-tag>
          </div>
          <el-switch
            v-model="scope.row.isCopyright"
            active-value="0"
            inactive-value="1"
            @change="ImageSwitch(scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="是否上架" align="center" prop="isShow" :formatter="isShowFormat">
        <template slot-scope="scope">
          <div class="tag-up">
            <el-tag :type="scope.row.isShow | showFilter">
              {{ scope.row.isShow | showNameFilter}}
            </el-tag>
          </div>
          <el-switch
            v-model="scope.row.isShow"
            active-value="0"
            inactive-value="1"
            @change="ImageSwitch(scope.row)"
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
            v-hasPermi="['material:image:edit']"
          >修改
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['material:image:remove']"
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

    <!-- 添加或修改图片素材对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="图片标注" type="textarea" prop="imageNote">
          <el-input v-model="form.imageNote" placeholder="请输入图片标注"/>
        </el-form-item>
        <el-form-item label="图片类型" prop="imageType">
          <el-select v-model="form.imageType" placeholder="请选择图片类型">
            <el-option
              v-for="dict in imageTypeOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="dict.dictValue"
            ></el-option>
          </el-select>
        </el-form-item>
        <div class="clip-info-status">
          <el-form-item label="图片尺寸" prop="imageSize">
            <el-input v-model="form.imageSize" :disabled="true"/>
          </el-form-item>
          <el-form-item label="图片打分" prop="imageMark">
            <el-input v-model="form.imageMark" :disabled="true"/>
          </el-form-item>
        </div>
        <el-form-item label="图片预览" prop="imagePath">
          <img :src="pic_url + form.imagePath + '.jpg'" alt="" class="pic-in-dialog">
        </el-form-item>
        <el-form-item label="图片标签" prop="imageTag">
          <el-tag
            :key="index"
            v-for="(tag, index) in form.imageTag"
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
        <div class="clip-info-status">
          <el-form-item label="素材版权" prop="isCopyright">
            <el-select v-model="form.isCopyright" placeholder="请选择素材版权">
              <el-option
                v-for="dict in isCopyrightOptions"
                :key="dict.dictValue"
                :label="dict.dictLabel"
                :value="dict.dictValue"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="是否上架" prop="isShow">
            <el-select v-model="form.isShow" placeholder="请选择是否上架">
              <el-option
                v-for="dict in isShowOptions"
                :key="dict.dictValue"
                :label="dict.dictLabel"
                :value="dict.dictValue"
              ></el-option>
            </el-select>
          </el-form-item>
        </div>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <div v-show="openHuge" class="pic-handle">
      <div class="pic-outline">
        <img :src="hugePicUrl" class="pic-show" alt="">
      </div>
    </div>
  </div>
</template>

<script>
  import {
    listImage,
    getImage,
    delImage,
    addImage,
    updateImage,
    exportImage,
    changeStatusImage,
    statusButton,
    optionImage
  } from "@/api/material/image";

  export default {
    name: "Image",
    filters: {
      copyNameFilter(status) {
        const statusMap = {
          1: '无版权',
          0: '有版权',
        }
        return statusMap[status]
      },
      copyFilter(status) {
        const statusMap = {
          0: 'success',
          1: 'warning',
        }
        return statusMap[status]
      },
      showNameFilter(status) {
        const statusMap = {
          1: '未上架',
          0: '已上架',
        }
        return statusMap[status]
      },
      showFilter(status) {
        const statusMap = {
          0: 'success',
          1: 'info',
        }
        return statusMap[status]
      },
      typeNameFilter(status) {
        const statusMap = {
          1: '普通图片',
          0: '高质图片',
        }
        return statusMap[status]
      },
      typeFilter(status) {
        const statusMap = {
          0: 'success',
          1: 'primary',
        }
        return statusMap[status]
      },
    },
    data() {
      return {
        hugePicUrl: "",
        openHuge: false,
        // 输入标签
        inputVisible: false,
        // 具体内容
        inputValue: '',
        // 临时标签列表
        imageTagTemp: undefined,
        // 导入处理
        importImage: 0,
        // 批量处理
        batchImage: 0,
        // 图片路径
        pic_url: process.env.VUE_APP_BASE_API + "/profile/image/",
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
        // 图片素材表格数据
        imageList: [],
        // 弹出层标题
        title: "",
        // 是否显示弹出层
        open: false,
        // 图片素材类型字典
        imageTypeOptions: [],
        // 素材版权字典
        isCopyrightOptions: [],
        // 是否上架字典
        isShowOptions: [],
        // 查询参数
        queryParams: {
          pageNum: 1,
          pageSize: 10,
          imageTag: null,
          imageType: null,
          isCopyright: null,
          isShow: null,
        },
        // 表单参数
        form: {},
        // 表单校验
        rules: {}
      };
    },
    created() {
      this.getList();
      this.getDicts("material_type").then(response => {
        this.imageTypeOptions = response.data;
      });
      this.getDicts("material_copyright").then(response => {
        this.isCopyrightOptions = response.data;
      });
      this.getDicts("material_public").then(response => {
        this.isShowOptions = response.data;
      });
    },
    methods: {
      /** 查询图片素材列表 */
      getList() {
        this.loading = true;
        statusButton().then(response => {
            if (response.data.importImage) {
              this.importImage = response.data.importImage
            }
            if (response.data.batchImage) {
              this.batchImage = response.data.batchImage
            }
          }
        )
        listImage(this.queryParams).then(response => {
          this.imageList = response.rows;
          Object.keys(this.imageList).forEach(key => {
            this.imageList[key].imageTag = JSON.parse(this.imageList[key].imageTag)
            this.imageList[key].imageTagTemp = []
            if (this.imageList[key].imageTag) {
              Object.keys(this.imageList[key].imageTag).forEach(ikey => {
                if (this.imageList[key].imageTag[ikey] && this.getLength(this.imageList[key].imageTag[ikey]) <= 8) {
                  this.imageList[key].imageTagTemp.push(this.imageList[key].imageTag[ikey])
                }
              })
            }
          });
          this.total = response.total;
          this.loading = false;
        });
      },
      showPic(pic) {
        this.hugePicUrl = pic;
        this.openHuge = true;
      },
      hidePic() {
        this.openHuge = false;
        // this.hugePicUrl = "";
      },
      getLength(str) {
        // console.log(str)
        let realLength = 0, len = str.length, charCode = -1;
        for (let i = 0; i < len; i++) {
          charCode = str.charCodeAt(i);
          if (charCode >= 0 && charCode <= 128) realLength += 1;
          else realLength += 2;
        }
        return realLength;
      },
      ImageSwitch(row_temp) {
        this.loading = true;
        const new_row = {};
        new_row.imageType = row_temp.imageType;
        new_row.isCopyright = row_temp.isCopyright;
        new_row.isShow = row_temp.isShow;
        new_row.imageId = row_temp.imageId;
        changeStatusImage(new_row).then(response => {
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
        // console.log(new_row)
      },
      /** 进行批处理 */
      handleOption(optionalId) {
        this.$confirm('是否确认执行该导入操作？', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(() => {
          optionImage(optionalId).then(response => {
              // console.log(response);
              this.msgSuccess("处理指令推送成功！");
              this.getList();
            }
          )
        })
      },
      handleClose(tag) {
        this.form.imageTag.splice(this.form.imageTag.indexOf(tag), 1);
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
          this.form.imageTag.push(inputValue);
        }
        this.inputVisible = false;
        this.inputValue = '';
      },
      // 图片素材类型字典翻译
      imageTypeFormat(row, column) {
        return this.selectDictLabel(this.imageTypeOptions, row.imageType);
      },
      // 素材版权字典翻译
      isCopyrightFormat(row, column) {
        return this.selectDictLabel(this.isCopyrightOptions, row.isCopyright);
      },
      // 是否上架字典翻译
      isShowFormat(row, column) {
        return this.selectDictLabel(this.isShowOptions, row.isShow);
      },
      // 取消按钮
      cancel() {
        this.open = false;
        this.reset();
      },
      // 表单重置
      reset() {
        this.form = {
          imageId: null,
          imagePath: null,
          imageNote: null,
          imageSize: null,
          imageTag: null,
          imageMark: null,
          imageStatus: "0",
          imageType: null,
          isCopyright: null,
          isShow: null,
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
        this.ids = selection.map(item => item.imageId)
        this.single = selection.length !== 1
        this.multiple = !selection.length
      },
      /** 新增按钮操作 */
      handleAdd() {
        this.reset();
        this.open = true;
        this.title = "添加图片素材";
      },
      /** 修改按钮操作 */
      handleUpdate(row) {
        this.reset();
        const imageId = row.imageId || this.ids
        getImage(imageId).then(response => {
          this.form = response.data;
          this.imageTagTemp = this.form.imageTag;
          this.form.imageTag = JSON.parse(this.imageTagTemp);
          this.open = true;
          this.title = "修改图片素材";
        });
      },
      /** 提交按钮 */
      submitForm() {
        this.$refs["form"].validate(valid => {
          if (valid) {
            this.imageTagTemp = this.form.imageTag;
            if (this.form.imageId != null) {
              // this.form.imageTag = JSON.stringify(this.imageTagTemp);
              updateImage({
                ...this.form,
                imageTag: JSON.stringify(this.imageTagTemp)
              }).then(response => {
                if (response.code === 200) {
                  this.msgSuccess("修改成功");
                  this.open = false;
                  this.getList();
                }
              });
            } else {
              addImage({
                ...this.form,
                imageTag: JSON.stringify(this.imageTagTemp)
              }).then(response => {
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
        const imageIds = row.imageId || this.ids;
        this.$confirm('是否确认删除图片素材编号为"' + imageIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return delImage(imageIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        }).catch(function () {
        });
      },
      /** 导出按钮操作 */
      handleExport() {
        const queryParams = this.queryParams;
        this.$confirm('是否确认导出所有图片素材数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return exportImage(queryParams);
        }).then(response => {
          this.download(response.msg);
        }).catch(function () {
        });
      }
    }
  };
</script>
<style>
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

  .button-new-tag {
    margin: 5px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }

  .clip-info {
    display: flex;
    margin-bottom: 20px;
  }

  .clip-info-status {
    display: flex;
  }

  .pic-show {
    margin-left: 0;
    margin-top: 0;
    max-height: 100%;
    max-width: 100%;
  }

  .pic-outline {
    width: 100%;
    height: 100%;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
  }

  .pic-handle {
    z-index: 2000;
    position: fixed;
    height: 100%;
    min-width: min-content;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  .image__block:hover {
    cursor: pointer;
  }
</style>
