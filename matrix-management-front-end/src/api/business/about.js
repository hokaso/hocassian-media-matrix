import request from '@/utils/request'

// 查询信息管理列表
export function listAbout(query) {
  return request({
    url: '/business/about/list',
    method: 'get',
    params: query
  })
}

// 查询信息管理详细
export function getAbout(aboutId) {
  return request({
    url: '/business/about/' + aboutId,
    method: 'get'
  })
}

// 新增信息管理
export function addAbout(data) {
  return request({
    url: '/business/about',
    method: 'post',
    data: data
  })
}

// 修改信息管理
export function updateAbout(data) {
  return request({
    url: '/business/about',
    method: 'put',
    data: data
  })
}

// 删除信息管理
export function delAbout(aboutId) {
  return request({
    url: '/business/about/' + aboutId,
    method: 'delete'
  })
}

// 导出信息管理
export function exportAbout(query) {
  return request({
    url: '/business/about/export',
    method: 'get',
    params: query
  })
}

// 读取当前信息管理列表
export function findAboutInfo() {
  return request({
    url: '/client/about/info',
    method: 'get'
  })
}
