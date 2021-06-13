import Vue from 'vue'

import Cookies from 'js-cookie'

import Element from 'element-ui'
import './assets/styles/element-variables.scss'

import '@/assets/styles/index.scss' // global css
import '@/assets/styles/hocassian.scss' // hocassian css
import App from './App'
import store from './store'
import router from './router'
import permission from './directive/permission'

import './assets/icons' // icon
import './permission' // permission control
import { getDicts } from "@/api/system/dict/data";
import { getConfigKey } from "@/api/system/config";
import { parseTime, resetForm, addDateRange, selectDictLabel, selectDictLabels, selectDictLabelOrigin, download, handleTree } from "@/utils/ruoyi";
import Pagination from "@/components/Pagination";
// 自定义表格工具扩展
import RightToolbar from "@/components/RightToolbar"
// import ClipCut from "@/components/ClipCut/index"
// import ClipCutIt from "./components/ClipCut/index.vue"
import ElTableEditabled from 'el-table-editabled'
import echarts from 'echarts'

// 全局方法挂载
Vue.prototype.$echarts = echarts
Vue.prototype.getDicts = getDicts
Vue.prototype.getConfigKey = getConfigKey
Vue.prototype.parseTime = parseTime
Vue.prototype.resetForm = resetForm
Vue.prototype.addDateRange = addDateRange
Vue.prototype.selectDictLabelOrigin = selectDictLabelOrigin
Vue.prototype.selectDictLabel = selectDictLabel
Vue.prototype.selectDictLabels = selectDictLabels
Vue.prototype.download = download
Vue.prototype.handleTree = handleTree

Vue.prototype.msgSuccess = function (msg) {
  this.$message({ showClose: true, message: msg, type: "success" });
}

Vue.prototype.msgError = function (msg) {
  this.$message({ showClose: true, message: msg, type: "error" });
}

Vue.prototype.msgInfo = function (msg) {
  this.$message.info(msg);
}

// 全局组件挂载
Vue.component('Pagination', Pagination)
Vue.component('RightToolbar', RightToolbar)
// Vue.component('ClipCut', ClipCut)


Vue.use(permission)
Vue.use(ElTableEditabled)
// Vue.use(ClipCut)

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online! ! !
 */

Vue.use(Element, {
  size: Cookies.get('size') || 'medium' // set element-ui default size
})

Vue.config.productionTip = false

/**
 * 设置浏览器头部标题
 */
export const setTitle = function(title) {
  title = title.aboutKeyword ? `${title.aboutKeyword}` + "新媒体矩阵" : '同和新媒体矩阵'
  window.document.title = title
}

router.afterEach(() => {
  setTimeout(() => {
    const browserHeaderTitle = store.getters.about
    console.log(browserHeaderTitle)
    setTitle(browserHeaderTitle)
  }, 1000)
})

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
