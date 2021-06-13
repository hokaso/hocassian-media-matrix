import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
export const showRouteList =[
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [{
      path: 'home',
      name: 'Home',
      component: () => import('@/views/home/index'),
      meta: { title: '主页', icon: 'dashboard', affix: true }
    }]
  },
  // {
  //   path: '/article',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '',
  //       name: 'web_article',
  //       component: () => import('@/views/article/index'),
  //       meta: { title: '文章', icon: 'article' },
  //     },
  //     {
  //       path: ':id(\\d+)',
  //       name: 'web_article_detail',
  //       component: () => import('@/views/article/detail'),
  //       meta: { title: '文章详情', noCache: true, activeMenu: '/article/index', icon: 'article' },
  //       hidden: true
  //     }
  //   ]
  // },
  {
    path: '/video',
    component: Layout,
    children: [
      {
        path: '',
        name: 'web_video',
        component: () => import('@/views/video/index'),
        meta: { title: '视频', icon: 'video' },
      },
      {
        path: ':id(\\d+)',
        name: 'web_video_detail',
        component: () => import('@/views/video/detail'),
        meta: { title: '视频详情', noCache: true, activeMenu: '/video/index', icon: 'video' },
        hidden: true
      }
    ]
  },
  {
    path: '/company',
    component: Layout,
    children: [{
      path: '',
      name: 'web_company',
      component: () => import('@/views/company/index'),
      meta: { title: '关于我们', icon: 'subordinate' },
    }]
  }
]

export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path*',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [{
      path: 'home',
      name: 'Home',
      component: () => import('@/views/home/index'),
      meta: { title: '主页', icon: 'dashboard', affix: true }
    }]
  },
  // {
  //   path: '/article',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '',
  //       name: 'web_article',
  //       component: () => import('@/views/article/index'),
  //       meta: { title: '文章', icon: 'article' },
  //     },
  //     {
  //       path: ':id(\\d+)',
  //       name: 'web_article_detail',
  //       component: () => import('@/views/article/detail'),
  //       meta: { title: '文章详情', noCache: true, activeMenu: '/article/index', icon: 'article' },
  //       hidden: true
  //     }
  //   ]
  // },
  {
    path: '/video',
    component: Layout,
    children: [
      {
        path: '',
        name: 'web_video',
        component: () => import('@/views/video/index'),
        meta: { title: '视频', icon: 'video' },
      },
      {
        path: ':id(\\d+)',
        name: 'web_video_detail',
        component: () => import('@/views/video/detail'),
        meta: { title: '视频详情', noCache: true, activeMenu: '/video/index', icon: 'video' },
        hidden: true
      }
    ]
  },
  {
    path: '/company',
    component: Layout,
    children: [{
      path: '',
      name: 'web_company',
      component: () => import('@/views/company/index'),
      meta: { title: '关于我们', icon: 'subordinate' },
    }]
  }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
