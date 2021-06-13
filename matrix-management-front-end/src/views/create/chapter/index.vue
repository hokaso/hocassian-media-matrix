<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="作品编号" prop="chapterWorkId">
        <el-input
          v-model="queryParams.chapterWorkId"
          placeholder="请输入作品编号"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="段落标题" prop="chapterStoryName">
        <el-input
          v-model="queryParams.chapterStoryName"
          placeholder="请输入段落标题"
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
          v-hasPermi="['create:chapter:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['create:chapter:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['create:chapter:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['create:chapter:export']"
        >导出</el-button>
      </el-col>
	  <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="chapterList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="段落编号" align="center" prop="chapterStoryId" />
      <el-table-column label="作品编号" align="center" prop="chapterWorkId" />
      <el-table-column label="段落标题" align="center" prop="chapterStoryName" />
      <el-table-column label="段落描述" align="center" prop="chapterStoryDescription" />
      <el-table-column label="段落类型" align="center" prop="chapterStoryType" />
      <el-table-column label="附加信息" align="center" prop="chapterStoryAddtional" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['create:chapter:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['create:chapter:remove']"
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

    <!-- 添加或修改篇章管理对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="作品编号" prop="chapterWorkId">
          <el-input v-model="form.chapterWorkId" placeholder="请输入作品编号" />
        </el-form-item>
        <el-form-item label="段落标题" prop="chapterStoryName">
          <el-input v-model="form.chapterStoryName" placeholder="请输入段落标题" />
        </el-form-item>
        <el-form-item label="段落描述" prop="chapterStoryDescription">
          <el-input v-model="form.chapterStoryDescription" placeholder="请输入段落描述" />
        </el-form-item>
        <el-form-item label="段落周目" prop="chapterStoryTimes">
          <el-input v-model="form.chapterStoryTimes" placeholder="请输入段落周目" />
        </el-form-item>
        <el-form-item label="结局编号" prop="chapterStoryEnding">
          <el-input v-model="form.chapterStoryEnding" placeholder="请输入段落结局编号" />
        </el-form-item>
        <el-form-item label="段落类型" prop="chapterStoryType">
          <el-select v-model="form.chapterStoryType" placeholder="请选择段落类型">
            <el-option label="请选择字典生成" value="" />
          </el-select>
        </el-form-item>
        <el-form-item label="段落条件" prop="chapterStoryCondiation">
          <el-input v-model="form.chapterStoryCondiation" placeholder="请输入段落条件" />
        </el-form-item>
        <el-form-item label="段落变更" prop="chapterStoryOperation">
          <el-input v-model="form.chapterStoryOperation" placeholder="请输入段落变更" />
        </el-form-item>
        <el-form-item label="下一段落" prop="chapterStoryNext">
          <el-input v-model="form.chapterStoryNext" placeholder="请输入下一段落" />
        </el-form-item>
        <el-form-item label="上一段落" prop="chapterStoryPrevious">
          <el-input v-model="form.chapterStoryPrevious" placeholder="请输入上一段落" />
        </el-form-item>
        <el-form-item label="附加信息" prop="chapterStoryAddtional">
          <el-input v-model="form.chapterStoryAddtional" placeholder="请输入附加信息" />
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
import { listChapter, getChapter, delChapter, addChapter, updateChapter, exportChapter } from "@/api/create/chapter";

export default {
  name: "Chapter",
  data() {
    return {
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
      // 篇章管理表格数据
      chapterList: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        chapterWorkId: null,
        chapterStoryName: null,
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
    /** 查询篇章管理列表 */
    getList() {
      this.loading = true;
      listChapter(this.queryParams).then(response => {
        this.chapterList = response.rows;
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
        chapterStoryId: null,
        chapterWorkId: null,
        chapterStoryName: null,
        chapterStoryDescription: null,
        chapterStoryTimes: null,
        chapterStoryEnding: null,
        chapterStoryType: null,
        chapterStoryCondiation: null,
        chapterStoryOperation: null,
        chapterStoryNext: null,
        chapterStoryPrevious: null,
        chapterStoryAddtional: null
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
      this.ids = selection.map(item => item.chapterStoryId)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加篇章管理";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const chapterStoryId = row.chapterStoryId || this.ids
      getChapter(chapterStoryId).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改篇章管理";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.chapterStoryId != null) {
            updateChapter(this.form).then(response => {
              if (response.code === 200) {
                this.msgSuccess("修改成功");
                this.open = false;
                this.getList();
              }
            });
          } else {
            addChapter(this.form).then(response => {
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
      const chapterStoryIds = row.chapterStoryId || this.ids;
      this.$confirm('是否确认删除篇章管理编号为"' + chapterStoryIds + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return delChapter(chapterStoryIds);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        }).catch(function() {});
    },
    /** 导出按钮操作 */
    handleExport() {
      const queryParams = this.queryParams;
      this.$confirm('是否确认导出所有篇章管理数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return exportChapter(queryParams);
        }).then(response => {
          this.download(response.msg);
        }).catch(function() {});
    }
  }
};
</script>
