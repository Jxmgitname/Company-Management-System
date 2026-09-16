import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    redirect: '/stats/overview',
    hidden: true
  },
  {
    path: '/system',
    component: Layout,
    redirect: '/system/user',
    name: 'System',
    meta: { title: '组织人事', icon: 'el-icon-setting' },
    children: [
      {
        path: 'user',
        name: 'SystemUser',
        component: () => import('@/views/system/user/index'),
        meta: { title: '员工管理', icon: 'user' }
      },
      {
        path: 'role',
        name: 'SystemRole',
        component: () => import('@/views/system/role/index'),
        meta: { title: '岗位管理', icon: 'el-icon-s-custom' }
      },
      {
        path: 'dept',
        name: 'SystemDept',
        component: () => import('@/views/system/dept/index'),
        meta: { title: '部门管理', icon: 'tree' }
      }
    ]
  },
  {
    path: '/stats',
    component: Layout,
    redirect: '/stats/overview',
    name: 'Stats',
    meta: { title: '人员概况', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'overview',
        name: 'StatsOverview',
        component: () => import('@/views/stats/index'),
        meta: { title: '人员概况', icon: 'table' }
      }
    ]
  },
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher
}

export default router
