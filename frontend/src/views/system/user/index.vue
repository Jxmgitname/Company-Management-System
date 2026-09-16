<template>
  <div class="app-container">
    <el-form :inline="true" :model="query" @submit.native.prevent>
      <el-form-item label="员工">
        <el-input v-model="query.username" placeholder="账号 / 姓名" clearable @keyup.enter.native="handleSearch" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">查询</el-button>
        <el-button @click="resetQuery">重置</el-button>
        <el-button type="success" @click="openCreate">新增</el-button>
      </el-form-item>
    </el-form>
    <!-- 添加“新增”按钮 -->
    <el-table v-loading="loading" :data="list" border>
      <el-table-column prop="id" label="ID" width="70" align="center" />
      <el-table-column prop="username" label="账号" />
      <el-table-column prop="nickname" label="姓名" />
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column prop="department_name" label="部门" />
      <el-table-column label="岗位" width="110">
        <template slot-scope="{ row }">
          {{ (row.role_names || []).join('、') }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="90" align="center">
      <template slot-scope="{ row }">
        <el-switch :value="row.status" @change="val => handleStatusChange(row, val)" />
      </template>
    </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="170" />
    <!-- 表格加「删除」按钮 -->
    <el-table-column label="操作" width="140" align="center">
      <template slot-scope="{ row }">
        <el-button type="text" @click="openEdit(row)">编辑</el-button>
        <el-button type="text" style="color:#f56c6c" @click="handleDelete(row)">删除</el-button>
      </template>
    </el-table-column>
    </el-table>
  
    
    <el-pagination
      class="pager"
      background
      layout="total, prev, pager, next, sizes"
      :total="total"
      :page-size="query.limit"
      :current-page="query.page"
      @current-change="handlePageChange"
      @size-change="handleSizeChange"
    />
    <el-dialog :title="editId ? '编辑员工' : '新增员工'" :visible.sync="dialogVisible" width="400px">
      <el-form label-width="80px">
        <el-form-item label="账号">
          <el-input v-model="createForm.username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="createForm.password" type="password" placeholder="新增必填；编辑不填则不改密码" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="createForm.nickname" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="createForm.phone" placeholder="选填" />
        </el-form-item>
        <el-form-item label="部门">
          <el-select v-model="createForm.department" clearable placeholder="请选择部门">
            <el-option
              v-for="item in allDepts"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="岗位">
          <el-select v-model="createForm.roles" multiple placeholder="请选择岗位">
            <el-option
              v-for="item in allRoles"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="createForm.status" active-text="启用" inactive-text="停用" />
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

import { getUserList, createUser, deleteUser, updateUser,getDeptList, getRoleList } from '@/api/system'

export default {
  name: 'SystemUser',
  data() {
    return {
      loading: false,
      allDepts: [],
      allRoles: [],
      list: [],
      total: 0,
      query: {
        username: '',
        page: 1,
        limit: 10
      },
      dialogVisible: false,editId: null,
      createForm: {
        username: '',
        password: '',
        nickname: '',
        phone: '',
        department: null,
        status: true,
        roles: []
      }
    }
  },
  created() {
    this.fetchData()
    getDeptList({ page_size: 100 }).then(res => { this.allDepts = res.data.results })
    getRoleList({ page_size: 100 }).then(res => { this.allRoles = res.data.results })
  },
  methods: {
    fetchData() {
      this.loading = true
      getUserList(this.query).then(res => {
        this.list = res.data.results// 人
        this.total = res.data.count//总数
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    openCreate() {
      this.editId = null
      this.createForm = { username: '', password: '', nickname: '', phone: '', department: null, roles: [],status: true }
      this.dialogVisible = true
    },
    openEdit(row) {
      this.editId = row.id
      this.createForm = {
        username: row.username,
        password: '',
        nickname: row.nickname || '',
        phone: row.phone || '',
        department: row.department,
        roles: row.roles || [],
        status: row.status !== false
      }
      this.dialogVisible = true
    },
    submitCreate() {
      if (!this.editId && !this.createForm.password) {
        this.$message.warning('请输入密码')
        return
      }
      const data = {
        username: this.createForm.username,
        nickname: this.createForm.nickname,
        phone: this.createForm.phone,
        department: this.createForm.department,
        roles: this.createForm.roles,
        status: this.createForm.status,
      }
      if (this.createForm.password) {
        data.password = this.createForm.password
      }
      const req = this.editId
        ? updateUser(this.editId, data)
        : createUser(this.createForm)
      req.then(() => {
        this.dialogVisible = false
        this.fetchData()
      })
    },
    handleStatusChange(row, val) {
      if (row.username === this.$store.getters.username && !val) {
        this.$message.warning('不能停用当前登录账号')
        this.fetchData()
        return
      }
      updateUser(row.id, { status: val }).then(() => {
        this.$message.success(val ? '已启用' : '已停用')
        this.fetchData()
      }).catch(() => {
        this.fetchData()
      })
    },
    handleDelete(row) {
      if (row.username === this.$store.getters.username) {
        this.$message.warning('不能删除当前登录账号')
        return
      }
      this.$confirm('确定删除员工 ' + row.username + ' 吗？', '提示', {
        type: 'warning'
      }).then(() => {
        return deleteUser(row.id)
      }).then(() => {
        this.fetchData()
      }).catch(() => {})
    },
    handleSearch() {
      this.query.page = 1
      this.fetchData()
    },
    resetQuery() {
      this.query.username = ''
      this.handleSearch()
    },
    handlePageChange(page) {
      this.query.page = page
      this.fetchData()
    },
    handleSizeChange(limit) {
      this.query.limit = limit
      this.query.page = 1
      this.fetchData()
    }
  }
}
</script>

<style scoped>
.pager {
  margin-top: 16px;
  text-align: right;
}
</style>
