<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="素材标签" prop="materialTag">
        <el-input
          v-model="queryParams.materialTag"
          placeholder="请输入素材标签"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="素材状态" prop="materialStatus">
        <el-select v-model="queryParams.materialStatus" placeholder="请选择素材状态" clearable size="small">
          <el-option
            v-for="dict in materialStatusOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="素材类型" prop="materialType">
        <el-select v-model="queryParams.materialType" placeholder="请选择素材类型" clearable size="small">
          <el-option
            v-for="dict in materialTypeOptions"
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
        <el-select v-model="queryParams.isShow" placeholder="请选择素材版权" clearable size="small">
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
          v-if="this.importClip === 1"
          type="primary"
          disabled
          icon="el-icon-loading"
          size="mini"
          v-hasPermi="['material:clip:add']"
        >导入素材
        </el-button>
        <el-button
          v-else
          type="primary"
          icon="el-icon-plus"
          size="mini"
          @click="handleOption(1)"
          v-hasPermi="['material:clip:add']"
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
          v-hasPermi="['material:clip:edit']"
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
          v-hasPermi="['material:clip:remove']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-if="this.batchClip === 2"
          type="warning"
          disabled
          icon="el-icon-loading"
          size="mini"
          @click=""
          v-hasPermi="['material:clip:add']"
        >处理素材
        </el-button>
        <el-button
          v-else
          type="warning"
          icon="el-icon-magic-stick"
          size="mini"
          @click="handleOption(2)"
          v-hasPermi="['material:clip:add']"
        >处理素材
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-if="this.translateClip === 3"
          type="primary"
          disabled
          icon="el-icon-loading"
          size="mini"
          @click=""
          v-hasPermi="['material:clip:add']"
        >导出素材
        </el-button>
        <el-button
          v-else
          type="primary"
          icon="el-icon-magic-stick"
          size="mini"
          @click="handleOption(3)"
          v-hasPermi="['material:clip:add']"
        >导出素材
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>
    <el-table v-loading="loading" :data="clipList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="素材截图" align="center">
        <template slot-scope="scope">
          <div
            class="image__block"
            @mouseover="showPic(clip_pic_url + scope.row.materialPath + '_cover.jpg')"
            @mouseout="hidePic()"
            v-if="scope.row.materialStatus === '0'">
            <img :src="clip_pic_url + scope.row.materialPath + '_cover.jpg'" alt="" class="pic-in-list">
          </div>
          <img src="../../../assets/image/unset.jpg" alt="" class="pic-in-list" v-else>
        </template>
      </el-table-column>
      <el-table-column label="素材标签" align="center" prop="materialTag" min-width="100px">
        <template slot-scope="scope">
          <el-tag class="mini-tag" v-for="ikey in scope.row.materialTagTemp" :key="ikey" type="success">
            {{ikey}}
          </el-tag>
        </template>
      </el-table-column>
      <!--      <el-table-column label="素材尺寸" align="center" prop="materialSize" />-->
      <!--      <el-table-column label="素材时长" align="center" prop="materialTime" />-->
      <!--      <el-table-column label="素材打分" align="center" prop="materialMark" />-->
      <el-table-column label="素材标注" align="center" prop="materialNote" :show-overflow-tooltip="true"/>
      <el-table-column label="素材状态" align="center" prop="materialStatus" :formatter="materialStatusFormat">
        <template slot-scope="scope">
          <el-tag :type="scope.row.materialStatus | statusFilter">
            {{ scope.row.materialStatus | statusNameFilter}}
          </el-tag>
        </template>
      </el-table-column>

      <!--      <el-table-column label="创建时间" align="center" prop="materialCreate" width="180">-->
      <!--        <template slot-scope="scope">-->
      <!--                <span>{{ parseTime(scope.row.materialCreate, '{y}-{m}-{d}') }}</span>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
      <el-table-column label="素材类型" align="center" prop="materialType" :formatter="materialTypeFormat">
        <template slot-scope="scope">
          <div class="tag-up">
            <el-tag :type="scope.row.materialType | typeFilter">
              {{ scope.row.materialType | typeNameFilter}}
            </el-tag>
          </div>
          <el-switch
            v-model="scope.row.materialType"
            active-value="0"
            inactive-value="1"
            @change="ClipSwitch(scope.row)"
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
            @change="ClipSwitch(scope.row)"
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
            @change="ClipSwitch(scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="是否归档" align="center" prop="isMerge" :formatter="isMergeFormat">
        <template slot-scope="scope">
          <el-tag :type="scope.row.isMerge | mergeFilter">
            {{ scope.row.isMerge | mergeNameFilter}}
          </el-tag>
        </template>

      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            v-show="scope.row.materialStatus !== '2'"
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['material:clip:edit']"
          >修改
          </el-button>
          <el-button
            v-show="scope.row.materialStatus !== '2'"
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['material:clip:remove']"
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

    <!-- 添加或修改视频素材对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="1200px" append-to-body v-if="form.materialStatus !== '0'">
      <el-row :gutter="36">
        <el-form ref="form" :model="form" :rules="rules" label-width="150px">
          <el-col :span="10">
            <el-form-item label="素材标注" prop="materialNote">
              <el-input v-model="form.materialNote" type="textarea" placeholder="请输入素材标注"/>
            </el-form-item>
            <el-form-item label="素材打分" prop="materialNote">
              <el-input v-model="form.materialMark" :disabled="true"/>
            </el-form-item>
            <el-form-item label="素材标签" prop="materialTag">
              <el-tag
                :key="index"
                v-for="(tag, index) in form.materialTag"
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
            <el-form-item label="创建时间" prop="materialCreate">
              <el-date-picker clearable size="small" style="width: 200px"
                              v-model="form.materialCreate"
                              type="datetime"
                              format="yyyy-MM-dd HH:mm:ss"
                              value-format="yyyy-MM-dd HH:mm:ss"
                              placeholder="选择创建时间">
              </el-date-picker>
            </el-form-item>
            <el-form-item label="素材类型" prop="materialType">
              <el-select v-model="form.materialType" placeholder="请选择素材类型">
                <el-option
                  v-for="dict in materialTypeOptions"
                  :key="dict.dictValue"
                  :label="dict.dictLabel"
                  :value="dict.dictValue"
                ></el-option>
              </el-select>
            </el-form-item>
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
              <el-select v-model="form.isShow" placeholder="请选择是否归档">
                <el-option
                  v-for="dict in isShowOptions"
                  :key="dict.dictValue"
                  :label="dict.dictLabel"
                  :value="dict.dictValue"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="是否归档" prop="isMerge">
              <el-select v-model="form.isMerge" disabled placeholder="请选择是否归档">
                <el-option
                  v-for="dict in isMergeOptions"
                  :key="dict.dictValue"
                  :label="dict.dictLabel"
                  :value="dict.dictValue"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <div class="clip-info">
              <el-form-item label="素材尺寸" prop="materialNote" label-width="80px">
                <el-input v-model="form.materialSize" :disabled="true"/>
              </el-form-item>
              <el-form-item label="素材时长" prop="materialNote" label-width="90px">
                <el-input v-model="form.materialTime" :disabled="true"/>
              </el-form-item>
            </div>
            <clip-cut
              v-if="videoShow"
              :start-point="form.materialStart"
              :end-point="form.materialEnd"
              :url="clip_url + form.materialPath + '.mp4'"
              @getTime="getTime"
              ref="VideoClip"
            ></clip-cut>
            <div style="display:flex">
              <el-form-item label="素材起始" prop="materialNote" label-width="80px">
                <el-input v-model="current.start" :disabled="true"/>
              </el-form-item>
              <el-form-item label="素材终点" prop="materialNote" label-width="90px">
                <el-input v-model="current.end" :disabled="true"/>
              </el-form-item>
            </div>
          </el-col>
        </el-form>
      </el-row>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body v-else>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="素材标注" prop="materialNote">
          <el-input v-model="form.materialNote" type="textarea" placeholder="请输入素材标注"/>
        </el-form-item>
        <el-form-item label="素材打分" prop="materialNote">
          <el-input v-model="form.materialMark" :disabled="true"/>
        </el-form-item>
        <div class="clip-info-status">
          <el-form-item label="素材尺寸" prop="materialSize">
            <el-input v-model="form.materialSize" :disabled="true"/>
          </el-form-item>
          <el-form-item label="素材时长" prop="materialTime">
            <el-input v-model="form.materialTime" :disabled="true"/>
          </el-form-item>
        </div>
        <el-form-item label="素材预览">
          <video controls="controls" :src="clip_url + form.materialPath + '.mp4'" style="width: 100%;"></video>
        </el-form-item>
        <el-form-item label="素材标签" prop="materialTag">
          <el-tag
            :key="index"
            v-for="(tag, index) in form.materialTag"
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
        <el-form-item label="创建时间" prop="materialCreate">
          <el-date-picker clearable size="small" style="width: 200px"
                          v-model="form.materialCreate"
                          type="datetime"
                          format="yyyy-MM-dd HH:mm:ss"
                          value-format="yyyy-MM-dd HH:mm:ss"
                          placeholder="选择创建时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="素材类型" prop="materialType">
          <el-select v-model="form.materialType" placeholder="请选择素材类型">
            <el-option
              v-for="dict in materialTypeOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="dict.dictValue"
            ></el-option>
          </el-select>
        </el-form-item>
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
          <el-select v-model="form.isShow" placeholder="请选择是否归档">
            <el-option
              v-for="dict in isShowOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="dict.dictValue"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="是否归档" prop="isMerge">
          <el-select v-model="form.isMerge" disabled placeholder="请选择是否归档">
            <el-option
              v-for="dict in isMergeOptions"
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

    <div v-show="openHuge" class="pic-handle">
      <div class="pic-outline">
        <img :src="hugePicUrl" class="pic-show">
      </div>
    </div>
  </div>
</template>

<script>
  import ClipCut from '@/components/ClipCut';
  import {
    listClip,
    statusButton,
    optionClip,
    getClip,
    delClip,
    addClip,
    updateClip,
    exportClip,
    changeStatusClip
  } from "@/api/material/clip";

  // import {changeStatusVideo} from "@/api/business/video";

  export default {
    name: "Clip",
    components: {ClipCut},
    filters: {
      typeNameFilter(status) {
        const statusMap = {
          1: '普通素材',
          0: '高质素材',
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
          1: '初入库',
          2: '正在处理',
          3: '准备处理'
        }
        return statusMap[status]
      },
      statusFilter(status) {
        const statusMap = {
          0: 'success',
          1: 'error',
          2: 'warning',
          3: 'info',
        }
        return statusMap[status]
      },
      mergeNameFilter(status) {
        const statusMap = {
          0: '已归档',
          1: '未合并',
        }
        return statusMap[status]
      },
      mergeFilter(status) {
        const statusMap = {
          0: 'success',
          1: 'info',
        }
        return statusMap[status]
      },
    },
    data() {
      return {
        timerSTO: "",
        hugePicUrl: "",
        openHuge: false,
        videoShow: true,
        current_temp: {},
        current: {},
        clip_url: process.env.VUE_APP_BASE_API + "/profile/video_clip/preview/",
        // 图片路径
        clip_pic_url: process.env.VUE_APP_BASE_API + "/profile/video_clip/clip_slot/",
        // 输入标签
        inputVisible: false,
        // 具体内容
        inputValue: '',
        // 临时标签列表
        clipTagTemp: undefined,
        // 导入处理
        importClip: 0,
        // 批量处理
        batchClip: 0,
        // 转移处理
        translateClip: 0,
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
        // 视频素材表格数据
        clipList: [],
        // 弹出层标题
        title: "",
        // 是否显示弹出层
        open: false,
        // 素材状态字典
        materialStatusOptions: [],
        // 素材类型字典
        materialTypeOptions: [],
        // 素材版权字典
        isCopyrightOptions: [],
        // 是否归档字典
        isMergeOptions: [],
        // 是否上架字典
        isShowOptions: [],
        // 查询参数
        queryParams: {
          pageNum: 1,
          pageSize: 10,
          materialTag: null,
          materialStatus: null,
          materialType: null,
          isCopyright: null,
          isShow: null,
        },
        // 表单参数
        form: {},
        // 表单校验
        rules: {}
      };
    },
    // beforeDestroy() {
    //   clearTimeout(this.timerSTO)
    // },
    created() {
      this.getList();
      this.getDicts("material_status").then(response => {
        this.materialStatusOptions = response.data;
      });
      this.getDicts("material_type").then(response => {
        this.materialTypeOptions = response.data;
      });
      this.getDicts("material_copyright").then(response => {
        this.isCopyrightOptions = response.data;
      });
      this.getDicts("material_merge").then(response => {
        this.isMergeOptions = response.data;
      });
      this.getDicts("material_public").then(response => {
        this.isShowOptions = response.data;
      });
    },
    methods: {
      getTime(val) {
        this.current = val
        // this.current_temp = val
        // console.log(this.current)
      },
      /** 查询视频素材列表 */
      getList() {
        this.loading = true;
        statusButton().then(response => {
            if (response.data.importClip) {
              this.importClip = response.data.importClip
            }
            if (response.data.batchClip) {
              this.batchClip = response.data.batchClip
            }
            if (response.data.translateClip) {
              this.translateClip = response.data.translateClip
            }
          }
        );
        listClip(this.queryParams).then(response => {
          this.clipList = response.rows;
          Object.keys(this.clipList).forEach(key => {
            this.clipList[key].materialTag = JSON.parse(this.clipList[key].materialTag)
            this.clipList[key].materialTagTemp = []
            // if (this.clipList[key].material)
            // 去除列表最后一个值
            // this.clipList[key].materialTag.splice(-1, 1);
            if (this.clipList[key].materialTag) {
              Object.keys(this.clipList[key].materialTag).forEach(ikey => {
                if (this.clipList[key].materialTag[ikey] && this.getLength(this.clipList[key].materialTag[ikey]) <= 8) {
                  this.clipList[key].materialTagTemp.push(this.clipList[key].materialTag[ikey])
                  // this.clipList[key].materialTag.splice(ikey, 1);
                }
              })
            }
            // console.log(this.clipList[key].materialTagTemp)
          });
          this.total = response.total;
          this.loading = false;
        });
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
      ClipSwitch(row_temp) {
        this.loading = true;
        const new_row = {};
        new_row.materialType = row_temp.materialType;
        new_row.isCopyright = row_temp.isCopyright;
        new_row.isShow = row_temp.isShow;
        new_row.materialId = row_temp.materialId;
        changeStatusClip(new_row).then(response => {
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
      handleClose(tag) {
        this.form.materialTag.splice(this.form.materialTag.indexOf(tag), 1);
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
          this.form.materialTag.push(inputValue);
        }
        this.inputVisible = false;
        this.inputValue = '';
      },
      // 素材状态字典翻译
      materialStatusFormat(row, column) {
        return this.selectDictLabel(this.materialStatusOptions, row.materialStatus);
      },
      // 素材类型字典翻译
      materialTypeFormat(row, column) {
        return this.selectDictLabel(this.materialTypeOptions, row.materialType);
      },
      // 素材版权字典翻译
      isCopyrightFormat(row, column) {
        return this.selectDictLabel(this.isCopyrightOptions, row.isCopyright);
      },
      // 是否归档字典翻译
      isMergeFormat(row, column) {
        return this.selectDictLabel(this.isMergeOptions, row.isMerge);
      },
      // 是否归档字典翻译
      isShowFormat(row, column) {
        return this.selectDictLabel(this.isShowOptions, row.isShow);
      },
      // 取消按钮
      cancel() {
        this.open = false;
        // this.reset();
      },
      // 表单重置
      reset() {
        this.form = {
          materialId: null,
          materialPath: null,
          materialSize: null,
          materialTime: null,
          materialNote: null,
          materialMark: null,
          materialStatus: null,
          materialTag: [],
          materialTagTemp: null,
          materialCreate: null,
          materialType: null,
          materialStart: 0,
          materialEnd: 0,
          isCopyright: null,
          isShow: null,
          isMerge: null,
          errorInfo: null
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
        this.ids = selection.map(item => item.materialId)
        this.single = selection.length !== 1
        this.multiple = !selection.length
      },
      /** 新增按钮操作 */
      handleAdd() {
        this.reset();
        this.open = true;
        this.title = "添加视频素材";
      },

      /** 进行批处理 */
      handleOption(optionalId) {
        this.$confirm('是否确认执行该转码操作？', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(() => {
          optionClip(optionalId).then(response => {
              // console.log(response);
              this.msgSuccess("处理指令推送成功！");
              this.getList();
            }
          )
        })
      },
      /** 修改按钮操作 */
      handleUpdate(row) {
        this.videoShow = false
        if (row.materialStatus !== "0") {
          setTimeout(() => {
            this.videoShow = true
            this.$nextTick(() => {
              this.$refs.VideoClip.init()
            })
          }, 1000)
        }
        this.reset();
        const materialId = row.materialId || this.ids
        getClip(materialId).then(response => {
          this.form = response.data;
          this.clipTagTemp = this.form.materialTag;
          this.form.materialTag = JSON.parse(this.clipTagTemp);
          this.current.start = this.form.materialStart;
          this.current.end = this.form.materialEnd;
          this.open = true;
          this.title = "修改视频素材";
        });
      },
      /** 提交按钮 */
      submitForm() {
        this.loading = true;
        this.$refs["form"].validate(valid => {
          if (valid) {
            this.clipTagTemp = this.form.materialTag;
            if (this.form.materialId != null) {
              // this.form.materialTag = JSON.stringify(this.clipTagTemp);
              this.form.materialStart = parseFloat(this.current.start);
              this.form.materialEnd = parseFloat(this.current.end);
              if (this.form.materialStatus === "1") {
                this.form.materialStatus = "3"
              }
              // console.log(this.form)
              updateClip({
                ...this.form,
                materialTag: JSON.stringify(this.clipTagTemp)
              }).then(response => {
                if (response.code === 200) {
                  this.msgSuccess("修改成功");
                  this.open = false;
                  this.getList();
                }
              });
            } else {
              // this.form.materialTag = JSON.stringify(this.clipTagTemp);
              addClip({
                ...this.form,
                materialTag: JSON.stringify(this.clipTagTemp)
              }).then(response => {
                if (response.code === 200) {
                  this.msgSuccess("新增成功");
                  this.open = false;
                  this.getList();
                }
              });
              this.form.materialTag = this.clipTagTemp;
            }
          }
        });
        this.videoShow = false
        // setTimeout(() => {
        //   this.videoShow = true
        //   this.$nextTick(() => {
        //     this.$refs.VideoClip.init()
        //   })
        // }, 1000)
      },
      /** 删除按钮操作 */
      handleDelete(row) {
        const materialIds = row.materialId || this.ids;
        this.$confirm('是否确认删除视频素材编号为"' + materialIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return delClip(materialIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        }).catch(function () {
        });
      },
      /** 导出按钮操作 */
      handleExport() {
        const queryParams = this.queryParams;
        this.$confirm('是否确认导出所有视频素材数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function () {
          return exportClip(queryParams);
        }).then(response => {
          this.download(response.msg);
        }).catch(function () {
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
