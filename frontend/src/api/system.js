import request from '@/utils/request'
// 用户
// 查询用户getUserList
export function getUserList(params) {
  return request({
    url: '/api/users/',
    method: 'get',
    params
  })
}
// 新增用户createUser
export function createUser(data) {
  return request({
    url: '/api/users/',
    method: 'post',
    data
  })
}
// 修改用户updateUser
export function updateUser(id, data) {
  return request({
    url: '/api/users/' + id + '/',
    method: 'put',
    data
  })
}
// 删除用户deleteUser
export function deleteUser(id) {
  return request({
    url: '/api/users/' + id + '/',
    method: 'delete'
  })
}

// 角色
//查询角色getRoleList
export function getRoleList(params) {
  return request({
    url: '/api/roles/',
    method: 'get',
    params
  })
}
// 新增角色createRole
export function createRole(data) {
  return request({
    url: '/api/roles/',
    method: 'post',
    data
  })
}
// 修改角色updateRole
export function updateRole(id, data) {
  return request({
    url: '/api/roles/' + id + '/',
    method: 'put',
    data
  })
}
// 删除角色deleteRole
export function deleteRole(id) {
  return request({
    url: '/api/roles/' + id + '/',
    method: 'delete'
  })
}
// 查询部门getDeptList
export function getDeptList(params) {
  return request({
    url: '/api/departments/',
    method: 'get',
    params
  })
}
// 新增部门createDept
export function createDept(data) {
  return request({
    url: '/api/departments/',
    method: 'post',
    data
  })
}
// 修改部门updateDept
export function updateDept(id, data) {
  return request({
    url: '/api/departments/' + id + '/',
    method: 'put',
    data
  })
}
// 删除部门deleteDept
export function deleteDept(id) {
  return request({
    url: '/api/departments/' + id + '/',
    method: 'delete'
  })
}
