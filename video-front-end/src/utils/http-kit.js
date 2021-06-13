import {Message} from 'element-ui'
import axios from 'axios'
axios.defaults.withCredentials=true;

axios.defaults.baseURL = process.env.VUE_APP_BASE_API
axios.defaults.timeout = 30 * 1000 // 设置接口响应时间

/**
 * 功能描述：Http Request 拦截器
 */
axios.interceptors.request.use((config) => {
  return config
}, (error) => { // 请求错误时做些事(接口错误、超时等)
  Message.error(`请求参数错误`, 10)
  return Promise.reject(error) // 在调用的那边可以拿到(catch)你想返回的错误信息
})

/**
 * 功能描述：Http Response 拦截器
 */
axios.interceptors.response.use((res) => {
  let isTips = res.config.showMessage === undefined || res.config.showMessage === true
  let data = res.data

  /* 根据返回的code值来做不同的处理（和后端约定） */
  switch (data.code) {
    case 200:
      return Promise.resolve(data)
    default:
      isTips && Message.error(`服务器返回异常：${data.message}`, 10)
      return Promise.reject(res)
  }
}, (error) => {
  Message.error(`服务器返回异常：${error}`, 10)

  if (error && error.response) {
    switch (error.response.status) {
      case 400:
        break
      default:
        break
    }
  }

  return Promise.reject(error)
})

export default {
  get (url, data = {}) {
    return new Promise((resolve, reject) => {
      axios.get(url, data).then(response => {
        resolve(response)
      }).catch(err => {
        reject(err)
      })
    })
  },
  delete (url, data = {}) {
    return new Promise((resolve, reject) => {
      axios.delete(url, data).then(response => {
        resolve(response)
      }).catch(err => {
        reject(err)
      })
    })
  },
  post (url, data = {}) {
    return new Promise((resolve, reject) => {
      axios.post(url, data).then(response => {
        resolve(response)
      }, err => {
        reject(err)
      })
    })
  },
  put (url, data = {}) {
    return new Promise((resolve, reject) => {
      axios.put(url, data).then(response => {
        resolve(response)
      }, err => {
        reject(err)
      })
    })
  },
  patch (url, data = {}) {
    return new Promise((resolve, reject) => {
      axios.patch(url, data).then(response => {
        resolve(response)
      }, err => {
        reject(err)
      })
    })
  }
}
