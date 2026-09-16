<template>
  <div class="app-container">
    <el-form :inline="true" :model="query" @submit.native.prevent>
      <el-form-item label="岗位">
        <el-input v-model="query.name" placeholder="名称 / 编码" clearable @keyup.enter.native="handleSearch" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">查询</el-button>
        <el-button @click="resetQuery">重置</el-button>
        <el-button type="success" @click="openCreate">新增</el-button>
      </el-form-item>
    </el-form>
    <el-table v-loading="loading" :data="list" border>
      <el-table-column prop="id" label="ID" width="70" align="center" />
      <el-table-column prop="name" label="岗位名称" />
      <el-table-column prop="code" label="岗位编码" width="140" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="userCount" label="员工数" width="90" align="center" />
      <el-table-column label="状态" width="90" align="center">
        <template slot-scope="{ row }">
          <el-tag :type="row.status ? 'success' : 'info'" size="mini">{{ row.status ? '启用' : '停用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="170" />
    <el-table-column label="操作" width="140" align="center">
      <template slot-scope="{ row }">
        <el-button type="text" @click="openEdit(row)">编辑</el-button>
        <el-button type="text" style="color:#f56c6c" @click="handleDelete(row)">删除</el-button>
      </template>
    </el-table-column>
    </el-table>
    <el-dialog :title="editId ? '编辑岗位' : '新增岗位'" :visible.sync="dialogVisible" width="400px">
      <el-form label-width="90px">
        <el-form-item label="岗位名称">
          <el-input v-model="createForm.name" />
        </el-form-item>
        <el-form-item label="岗位编码">
          <el-input v-model="createForm.code" placeholder="英文，如 finance" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="createForm.description" />
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCreate">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getRoleList, createRole,updateRole,deleteRole } from '@/api/system'

export default {
  name: 'SystemRole',
  data() {
    return {
      loading: false,
      list: [],
      dialogVisible: false,editId: null,
      query: { name: '' },
      createForm: {
        name: '',
        code: '',
        description: ''
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.loading = true
      getRoleList(this.query).then(res => {
        this.list = res.data.results
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    handleSearch() {
      this.fetchData()
    },
    resetQuery() {
      this.query.name = ''
      this.fetchData()
    },
    openCreate() {
      this.editId = null
      this.createForm = { name: '', code: '', description: '' }
      this.dialogVisible = true
    },
    openEdit(row) {
      this.editId = row.id
      this.createForm = {
        name: row.name,
        code: row.code,
        description: row.description || ''
      }
      this.dialogVisible = true
    },
    submitCreate() {
      const req = this.editId
        ? updateRole(this.editId, this.createForm)
        : createRole(this.createForm)
      req.then(() => {
        this.$message.success(this.editId ? '岗位已更新' : '岗位已新增')
        this.dialogVisible = false
        this.fetchData()
      })
    },
    handleDelete(row) {
      this.$confirm('确定删除岗位 ' + row.name + ' 吗？', '提示', {
        type: 'warning'
      }).then(() => {
        return deleteRole(row.id)
      }).then(() => {
        this.$message.success('删除成功')
        this.fetchData()
      }).catch(() => {})
    },
  }
}
</script>
