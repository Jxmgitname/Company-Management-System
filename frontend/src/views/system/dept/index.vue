<template>
  <div class="app-container">
    <el-form :inline="true" :model="query" @submit.native.prevent>
      <el-form-item label="部门">
        <el-input v-model="query.name" placeholder="部门名称 / 负责人" clearable @keyup.enter.native="handleSearch" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">查询</el-button>
        <el-button @click="resetQuery">重置</el-button>
        <el-button type="success" @click="openCreate">新增</el-button>
      </el-form-item>
    </el-form>
    <el-table v-loading="loading" :data="list" border row-key="id" default-expand-all :tree-props="{ children: 'children' }">
      <el-table-column prop="name" label="部门名称" />
      <el-table-column prop="leader" label="负责人" width="140" />
      <el-table-column prop="sort" label="排序" width="90" align="center" />
      <el-table-column label="状态" width="90" align="center">
        <template slot-scope="{ row }">
          <el-tag :type="row.status ? 'success' : 'info'" size="mini">{{ row.status ? '启用' : '停用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="140" align="center">
        <template slot-scope="{ row }">
          <el-button type="text" @click="openEdit(row)">编辑</el-button>
          <el-button type="text" style="color:#f56c6c" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="editId ? '编辑部门' : '新增部门'" :visible.sync="dialogVisible" width="400px">
      <el-form label-width="90px">
        <el-form-item label="部门名称">
          <el-input v-model="createForm.name" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="createForm.leader" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input v-model="createForm.sort" />
        </el-form-item>
        <el-form-item label="上级部门">
          <el-select v-model="createForm.parent" clearable placeholder="不选就是顶级">
            <el-option
              v-for="item in allDepts"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
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
import { getDeptList,createDept,updateDept,deleteDept } from '@/api/system'

export default {
  name: 'SystemDept',
  data() {
    return {
      loading: false,
      list: [],
      allDepts: [],
      query: { name: '' },
      dialogVisible: false,
      editId: null,
      createForm: { name: '', leader: '', sort: 0, parent: null }
    }
  },
   created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.loading = true
      getDeptList(this.query).then(res => {
        this.allDepts = res.data.results
        this.list = this.buildTree(res.data.results)
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    buildTree(items, parentId = null) {
      const ids = items.map(item => item.id)
      return items
        .filter(item => {
          if (parentId === null) {
            return item.parent == null || ids.indexOf(item.parent) === -1
          }
          return item.parent === parentId
        })
        .map(item => ({
          ...item,
          children: this.buildTree(items, item.id)
        }))
    },
    openCreate() {
      this.editId = null
      this.createForm = { name: '', leader: '', sort: 0,parent: null  }
      this.dialogVisible = true
    },
    openEdit(row) {
      this.editId = row.id
      this.createForm = {
        name: row.name,
        leader: row.leader || '',
        sort: row.sort,
        parent: row.parent
      }
      this.dialogVisible = true
    },
    submitCreate() {
      const req = this.editId
        ? updateDept(this.editId, this.createForm)
        : createDept(this.createForm)
      req.then(() => {
        this.$message.success(this.editId ? '部门已更新' : '部门已新增')
        this.dialogVisible = false
        this.fetchData()
      })
    },
    handleSearch() {
      this.fetchData()
    },
    resetQuery() {
      this.query.name = ''
      this.fetchData()
    },
    handleDelete(row) {
      this.$confirm('确定删除部门 ' + row.name + ' 吗？', '提示', {
        type: 'warning'
      }).then(() => {
        return deleteDept(row.id)
      }).then(() => {
        this.$message.success('删除成功')
        this.fetchData()
      }).catch(() => {})
    },
    
  }
}
</script>
