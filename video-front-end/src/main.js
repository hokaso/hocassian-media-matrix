import Vue from "vue";
import "normalize.css/normalize.css"; // CSS重置的现代替代方法

import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import "@/styles/index.scss"; // global css

import App from "./App.vue";
import store from "./store";
import router from "./router";

import "@/icons"; // 图标
import VueAwesomeSwiper from "vue-awesome-swiper";

// import style
import "swiper/css/swiper.css";

// import VueXgplayer from './xgplayer-vue.vue'
import VueXgplayer from "xgplayer-vue";

Vue.component("VueXgplayer", VueXgplayer);

Vue.use(VueAwesomeSwiper);
import getPageTitle from "@/utils/get-page-title";
// import 'lib-flexible'
// import '@/utils/rem'
import "lib-flexible/flexible";
Vue.use(ElementUI);
Vue.config.productionTip = false;

/**
 * 设置浏览器头部标题
 */
export const setTitle = function(title) {
  title = title.aboutKeyword
    ? `${title.aboutKeyword}` + "视频矩阵"
    : "同和视频矩阵";
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

new Vue({
  el: "#app",
  router,
  store,
  render: h => h(App),
  components: { App },
  template: "<App/>"
});
