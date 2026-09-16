import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/login/',
    method: 'post',
    data
  })
}
export function getDashboard() {
  return request({
    url: '/api/dashboard/',
    method: 'get'
  })
}
export function getInfo() {
  return request({
    url: '/api/user/info/',
    method: 'get'
  })
}
export function logout() {
  return Promise.resolve({ code: 200, data: 'success' })
}
