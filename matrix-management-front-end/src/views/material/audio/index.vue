<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="音频名称" prop="audioName">
        <el-input
          v-model="queryParams.audioName"
          placeholder="请输入音频素材名称"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="素材状态" prop="audioStatus">
        <el-select v-model="queryParams.audioStatus" placeholder="请选择素材状态" clearable size="small">
          <el-option
            v-for="dict in audioStatusOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="音频类型" prop="audioType">
        <el-select v-model="queryParams.audioType" placeholder="请选择音频素材类型" clearable size="small">
          <el-option
            v-for="dict in audioTypeOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="音频版权" prop="isCopyright">
        <el-select v-model="queryParams.isCopyright" placeholder="请选择音频素材版权" clearable size="small">
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
          v-if="this.importAudio === 1"
          type="primary"
          disabled
          icon="el-icon-loading"
          size="mini"
          v-hasPermi="['material:audio:add']"
        >导入素材
        </el-button>
        <el-button
          v-else
          type="primary"
          icon="el-icon-plus"
          size="mini"
          @click="handleOption(1)"
          v-hasPermi="['material:audio:add']"
        >导入素材
        </el-button>
      </el-col>
<!--      <el-col :span="1.5">-->
<!--        <el-button-->
<!--          type="primary"-->
<!--          icon="el-icon-plus"-->
<!--          size="mini"-->
<!--          @click="handleAdd"-->
<!--          v-hasPermi="['material:audio:add']"-->
<!--        >新增-->
<!--        </el-button>-->
<!--      </el-col>-->
      <el-col :span="1.5">
        <el-button
          type="success"
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['material:audio:edit']"
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
          v-hasPermi="['material:audio:remove']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-if="this.batchAudio === 2"
          type="warning"
          disabled
          icon="el-icon-loading"
          size="mini"
          @click=""
          v-hasPermi="['material:audio:add']"
        >处理素材
        </el-button>
        <el-button
          v-else
          type="warning"
          icon="el-icon-magic-stick"
          size="mini"
          @click="handleOption(2)"
          v-hasPermi="['material:audio:add']"
        >处理素材
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>
    <el-table v-loading="loading" :data="audioList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="音频素材名称" align="center" prop="audioName"/>
      <el-table-column label="音频素材作者" align="center" prop="audioAuthor"/>
      <el-table-column label="音频素材类型" align="center" prop="audioType" :formatter="audioTypeFormat">
        <template slot-scope="scope">
          <el-tag :type="scope.row.audioType | typeFilter">
            {{ scope.row.audioType | typeNameFilter}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="音频素材状态" align="center" prop="audioStatus" :formatter="audioStatusFormat">
        <template slot-scope="scope">
          <el-tag :type="scope.row.audioStatus | statusFilter">
            {{ scope.row.audioStatus | statusNameFilter}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="音频情感标签" align="center" prop="audioEmotion" min-width="100px">
        <template slot-scope="scope">
          <el-tag class="mini-tag" v-for="ikey in scope.row.audioEmotion" :key="ikey" type="success">
            {{ikey}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="音频素材版权" align="center" prop="isCopyright" :formatter="isCopyrightFormat">
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
            @change="AudioSwitch(scope.row)"
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
            @change="AudioSwitch(scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            v-show="scope.row.audioStatus !== '3'"
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['material:audio:edit']"
          >修改
          </el-button>
          <el-button
            v-show="scope.row.audioStatus !== '3'"
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['material:audio:remove']"
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

    <!-- 添加或修改音频素材对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="音频名称" prop="audioName">
          <el-input v-model="form.audioName" placeholder="请输入音频素材名称"/>
        </el-form-item>
        <el-form-item label="音频作者" prop="audioAuthor">
          <el-input v-model="form.audioAuthor" placeholder="请输入音频素材作者"/>
        </el-form-item>
        <el-form-item label="音频类型" prop="audioType">
          <el-select v-model="form.audioType" placeholder="请选择音频素材类型" v-if="form.audioStatus !== '0'">
            <el-option
              v-for="dict in audioTypeOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="dict.dictValue"
            ></el-option>
          </el-select>
          <el-select v-model="form.audioType" disabled placeholder="请选择音频素材类型" v-else>
            <el-option
              v-for="dict in audioTypeOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="dict.dictValue"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="音频预览">
          <audio controls="controls" :src="audio_url + form.audioPath + '.mp3'" style="width: 100%;"></audio>
        </el-form-item>
        <el-form-item label="伴奏预览" v-show="form.audioType==='1' && form.audioStatus === '0'">
          <audio controls="controls" :src="audio_url_off + form.audioPath + '.mp3'" style="width: 100%;"></audio>
        </el-form-item>
        <el-form-item label="音频标签" prop="audioEmotion">
          <el-tag
            :key="index"
            v-for="(tag, index) in form.audioEmotion"
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
          <!--          <el-input v-model="form.audioEmotion" placeholder="请输入素材标签"/>-->
        </el-form-item>
        <el-form-item label="音频备注" prop="audioNote">
          <el-input v-model="form.audioNote" type="textarea" placeholder="请输入音频素材备注"/>
        </el-form-item>
        <el-form-item label="音频时长" disabled prop="audioTime">
          <el-input v-model="form.audioTime" placeholder="请输入音频素材时长" :disabled="true"/>
        </el-form-item>
        <div class="clip-info">
          <el-form-item label="音频版权" prop="isCopyright">
            <el-select v-model="form.isCopyright" placeholder="请选择音频版权">
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
  </div>
</template>

<script>
  import {
    statusButton,
    listAudio,
    getAudio,
    delAudio,
    addAudio,
    updateAudio,
    exportAudio,
    optionAudio,
    changeStatusAudio
  } from "@/api/material/audio";

  export default {
    name: "Audio",
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
      statusNameFilter(status) {
        const statusMap = {
          0: '处理完毕',
          1: '待处理',
          2: '无需处理',
          3: '正在处理'
        }
        return statusMap[status]
      },
      statusFilter(status) {
        const statusMap = {
          0: 'success',
          1: 'error',
          2: 'info',
          3: 'warning',
        }
        return statusMap[status]
      },
      typeNameFilter(status) {
        const statusMap = {
          1: '歌曲',
          0: '纯音乐',
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
        // 输入标签
        inputVisible: false,
        // 具体内容
        inputValue: '',
        // 临时标签列表
        audioTapTemp: undefined,
        audio_url: process.env.VUE_APP_BASE_API + "/profile/audio_music/",
        audio_url_off: process.env.VUE_APP_BASE_API + "/profile/audio_music/audio_off_vocal/",
        // 导入处理
        importAudio: 0,
        // 批量处理
        batchAudio: 0,
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
        // 音频素材表格数据
        audioList: [],
        // 弹出层标题
        title: "",
        // 是否显示弹出层
        open: false,
        // 音频素材类型字典
        audioTypeOptions: [],
        // 音频素材状态字典
        audioStatusOptions: [],
        // 音频素材版权字典
        isCopyrightOptions: [],
        // 是否上架字典
        isShowOptions: [],
        // 查询参数
        queryParams: {
          pageNum: 1,
          pageSize: 10,
          audioStatus: null,
          audioName: null,
          audioType: null,
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
      this.getDicts("audio_classify").then(response => {
        this.audioTypeOptions = response.data;
      });
      this.getDicts("mat_audio_status").then(response => {
        this.audioStatusOptions = response.data;
      });
      this.getDicts("material_copyright").then(response => {
        this.isCopyrightOptions = response.data;
      });
      this.getDicts("material_public").then(response => {
        this.isShowOptions = response.data;
      });
    },
    methods: {
      /** 查询音频素材列表 */
      getList() {
        this.loading = true;
        statusButton().then(response => {
            if (response.data.importAudio) {
              this.importAudio = response.data.importAudio
            }
            if (response.data.batchAudio) {
              this.batchAudio = response.data.batchAudio
            }
          }
        )
        listAudio(this.queryParams).then(response => {
          this.audioList = response.rows;
          Object.keys(this.audioList).forEach(key => {
            this.audioList[key].audioEmotion = JSON.parse(this.audioList[key].audioEmotion)
            this.audioList[key].audioEmotionTemp = []
            if (this.audioList[key].audioEmotion){
              Object.keys(this.audioList[key].audioEmotion).forEach(ikey => {
                if (this.audioList[key].audioEmotion[ikey] && this.getLength(this.audioList[key].audioEmotion[ikey]) <= 4) {
                  this.audioList[key].audioEmotionTemp.push(this.audioList[key].audioEmotion[ikey])
                }
              })
            }
          });
          this.total = response.total;
          this.loading = false;
        });
      },
      getLength(str) {
        let realLength = 0, len = str.length, charCode = -1;
        for (let i = 0; i < len; i++) {
          charCode = str.charCodeAt(i);
          if (charCode >= 0 && charCode <= 128) realLength += 1;
          else realLength += 1;
        }
        return realLength;
      },
      // 音频素材类型字典翻译
      audioTypeFormat(row, column) {
        return this.selectDictLabel(this.audioTypeOptions, row.audioType);
      },
      // 音频素材状态字典翻译
      audioStatusFormat(row, column) {
        return this.selectDictLabel(this.audioStatusOptions, row.audioStatus);
      },
      // 音频素材版权字典翻译
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
          audioId: null,
          audioPath: null,
          audioName: null,
          audioAuthor: null,
          audioType: null,
          audioStatus: null,
          audioEmotion: null,
          audioNote: null,
          audioTime: null,
          isCopyright: null,
          isShow: null
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
        this.ids = selection.map(item => item.audioId)
        this.single = selection.length !== 1
        this.multiple = !selection.length
      },
      /** 新增按钮操作 */
      handleAdd() {
        this.reset();
        this.open = true;
        this.title = "添加音频素材";
      },
      /** 修改按钮操作 */
      handleUpdate(row) {
        this.reset();
        const audioId = row.audioId || this.ids
        getAudio(audioId).then(response => {
          this.form = response.data;
          this.audioTapTemp = this.form.audioEmotion;
          this.form.audioEmotion = JSON.parse(this.audioTapTemp);
          this.open = true;
          this.title = "修改音频素材";
        });
      },
      AudioSwitch(row_temp) {
        this.loading = true;
        const new_row = {};
        new_row.isCopyright = row_temp.isCopyright;
        new_row.isShow = row_temp.isShow;
        new_row.audioId = row_temp.audioId;
        changeStatusAudio(new_row).then(response => {
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
        // console.log(new_row)
      },
      handleClose(tag) {
        this.form.audioEmotion.splice(this.form.audioEmotion.indexOf(tag), 1);
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
          this.form.audioEmotion.push(inputValue);
        }
        this.inputVisible = false;
        this.inputValue = '';
      },
      /** 提交按钮 */
      submitForm() {
        this.$refs["form"].validate(valid => {
          if (valid) {
            this.audioTapTemp = this.form.audioEmotion;
            if (this.form.audioId != null) {
              if (this.form.audioStatus !== "0") {
                if (this.form.audioType === "0") {
                  this.form.audioStatus = "2"
                }
                else {
                  this.form.audioStatus = "1"
                }
              }
              // this.form.audioEmotion = JSON.stringify(this.audioTapTemp);
              updateAudio({
                ...this.form,
                audioEmotion: JSON.stringify(this.audioTapTemp)
              }).then(response => {
                if (response.code === 200) {
                  this.msgSuccess("修改成功");
                  this.open = false;
                  this.getList();
                }
              });
            } else {
              // this.form.audioEmotion = JSON.stringify(this.audioTapTemp);
              addAudio({
                ...this.form,
                audioEmotion: JSON.stringify(this.audioTapTemp)
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

      /** 进行批处理 */
      handleOption(optionalId) {
        this.$confirm('是否确认执行该处理操作？', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(()=>{
          optionAudio(optionalId).then(response => {
              console.log(response);
              this.msgSuccess("处理指令推送成功！");
              this.getList();
            }
          )
        })
      },

      /** 删除按钮操作 */
      handleDelete(row) {
        const audioIds = row.audioId || this.ids;
        this.$confirm('是否确认删除音频素材编号为"' + audioIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return delAudio(audioIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        }).catch(function () {
        });
      },
      /** 导出按钮操作 */
      handleExport() {
        const queryParams = this.queryParams;
        this.$confirm('是否确认导出所有音频素材数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return exportAudio(queryParams);
        }).then(response => {
          this.download(response.msg);
        }).catch(function () {
        });
      }
    }
  };
</script>
<style>
  .clip-info {
    display: flex;
    margin-bottom: 20px;
  }
  .mini-tag {
    -webkit-transform: scale(0.8);
    margin: 4px;
  }

  .tag-up {
    margin-bottom: 20px;
  }

  .el-tag {
    margin: 5px;
  }

  .input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }
  .clip-info-status{
    display: flex;
  }
  .button-new-tag {
    margin: 5px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }
</style>
