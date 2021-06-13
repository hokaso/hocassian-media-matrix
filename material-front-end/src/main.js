// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui';
import 'normalize.css/normalize.css' // CSS重置的现代替代方法
import 'element-ui/lib/theme-chalk/index.css';
import '@/assets/styles/index.scss' // global css
import App from './App'
import store from './store'
import router from './router'

import './assets/icons' // icon
import getPageTitle from '@/utils/get-page-title'
Vue.use(ElementUI);

Vue.config.productionTip = false

// router.beforeEach(async(to, from, next) => {
//   document.title = getPageTitle(to.meta.title)
//   next()
// })

/**
 * 设置浏览器头部标题
 */
export const setTitle = function(title) {
  title = title.aboutKeyword
    ? `${title.aboutKeyword}` + "素材矩阵"
    : "同和素材矩阵";
  window.document.title = getPageTitle(title);
};

router.afterEach(() => {
  setTimeout(() => {
    const browserHeaderTitle = store.getters.about;
    console.log(browserHeaderTitle);
    setTitle(browserHeaderTitle);
  }, 1000);

  // next();
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
