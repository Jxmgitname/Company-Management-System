const Mock = require('mockjs')

const userList = Mock.mock({
  'items|36': [{
    'id|+1': 1,
    username: '@word(5, 10)',
    nickname: '@cname',
    phone: /^1[3-9]\d{9}$/,
    email: '@email',
    'status|1': [true, true, true, false],
    'role|1': ['管理员', '运维', '开发', '访客'],
    'dept|1': ['研发中心', '产品中心', '运营中心', '财务部'],
    created_at: '@datetime'
  }]
}).items

userList.unshift({
  id: 0,
  username: 'admin',
  nickname: '超级管理员',
  phone: '13800000000',
  email: 'admin@example.com',
  status: true,
  role: '管理员',
  dept: '研发中心',
  created_at: '2024-01-01 09:00:00'
})

const roleList = [
  { id: 1, name: '超级管理员', code: 'admin', description: '拥有全部权限', status: true, userCount: 1, created_at: '2024-01-01 09:00:00' },
  { id: 2, name: '运维人员', code: 'ops', description: '系统运维与监控', status: true, userCount: 8, created_at: '2024-02-12 10:20:00' },
  { id: 3, name: '开发人员', code: 'dev', description: '业务功能开发', status: true, userCount: 16, created_at: '2024-03-08 14:12:00' },
  { id: 4, name: '访客', code: 'guest', description: '只读访问', status: false, userCount: 5, created_at: '2024-04-18 16:40:00' }
]

const deptList = [
  { id: 1, name: '公司总部', parent_id: 0, leader: '张伟', sort: 1, status: true },
  { id: 2, name: '研发中心', parent_id: 1, leader: '李娜', sort: 1, status: true },
  { id: 3, name: '产品中心', parent_id: 1, leader: '王强', sort: 2, status: true },
  { id: 4, name: '运营中心', parent_id: 1, leader: '赵敏', sort: 3, status: true },
  { id: 5, name: '财务部', parent_id: 1, leader: '陈晨', sort: 4, status: true },
  { id: 6, name: '前端组', parent_id: 2, leader: '周杰', sort: 1, status: true },
  { id: 7, name: '后端组', parent_id: 2, leader: '吴磊', sort: 2, status: true }
]

module.exports = [
  {
    url: '/vue-admin-template/system/user/list',
    type: 'get',
    response: config => {
      const { username, page = 1, limit = 10 } = config.query
      let items = userList
      if (username) {
        items = items.filter(item => item.username.includes(username) || item.nickname.includes(username))
      }
      const start = (page - 1) * limit
      return {
        code: 20000,
        data: {
          total: items.length,
          items: items.slice(start, start + Number(limit))
        }
      }
    }
  },
  {
    url: '/vue-admin-template/system/role/list',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: {
          total: roleList.length,
          items: roleList
        }
      }
    }
  },
  {
    url: '/vue-admin-template/system/dept/list',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: {
          total: deptList.length,
          items: deptList
        }
      }
    }
  }
]
