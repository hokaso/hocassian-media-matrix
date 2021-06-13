import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)
import Layout from '@/layout'

export const showRouteList = [
  {
    path: '/',
    component: Layout,
    redirect: '/newest',
    children: [{
      path: 'newest',
      name: 'Newest',
      component: () => import('@/views/newest/index'),
      meta: { title: '最新', icon: 'dashboard', affix: true }
    }]
  },
  {
    path: '/clip',
    component: Layout,
    children: [{
      path: '',
      name: 'clip',
      component: () => import('@/views/clip/index'),
      meta: { title: '视频素材', icon: 'video', affix: true }
    }]
  },
  {
    path: '/musicMaterial',
    component: Layout,
    children: [{
      path: '',
      name: 'musicMaterial',
      component: () => import('@/views/musicMaterial/index'),
      meta: { title: '音频素材', icon: 'music', affix: true }
    }]
  },
  {
    path: '/pictureMaterial',
    component: Layout,
    children: [{
      path: '',
      name: 'pictureMaterial',
      component: () => import('@/views/pictureMaterial/index'),
      meta: { title: '图片素材', icon: 'image', affix: true }
    }]
  },
  {
    path: '/about',
    component: Layout,
    children: [{
      path: '',
      name: 'about',
      component: () => import('@/views/about/index'),
      meta: { title: '关于我们', icon: 'subordinate', affix: true }
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
    redirect: '/newest',
    children: [{
      path: 'newest',
      name: 'Newest',
      component: () => import('@/views/newest/index'),
      meta: { title: '最新', icon: 'dashboard', affix: true }
    }]
  },
  {
    path: '/clip',
    component: Layout,
    children: [{
      path: '',
      name: 'clip',
      component: () => import('@/views/clip/index'),
      meta: { title: '视频素材', icon: 'video', affix: true }
    }]
  },
  {
    path: '/musicMaterial',
    component: Layout,
    children: [{
      path: '',
      name: 'musicMaterial',
      component: () => import('@/views/musicMaterial/index'),
      meta: { title: '音频素材', icon: 'music', affix: true }
    }]
  },
  {
    path: '/pictureMaterial',
    component: Layout,
    children: [{
      path: '',
      name: 'pictureMaterial',
      component: () => import('@/views/pictureMaterial/index'),
      meta: { title: '图片素材', icon: 'image', affix: true }
    }]
  },
  {
    path: '/about',
    component: Layout,
    children: [{
      path: '',
      name: 'about',
      component: () => import('@/views/about/index'),
      meta: { title: '关于我们', icon: 'subordinate', affix: true }
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
