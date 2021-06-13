import request from '@/utils/request'

// 查询图片素材列表
export function listImage(query) {
  return request({
    url: '/material/image/list',
    method: 'get',
    params: query
  })
}

// 查询图片素材详细
export function getImage(imageId) {
  return request({
    url: '/material/image/' + imageId,
    method: 'get'
  })
}

// 新增图片素材
export function addImage(data) {
  return request({
    url: '/material/image',
    method: 'post',
    data: data
  })
}

// 修改图片素材
export function updateImage(data) {
  return request({
    url: '/material/image',
    method: 'put',
    data: data
  })
}

// 删除图片素材
export function delImage(imageId) {
  return request({
    url: '/material/image/' + imageId,
    method: 'delete'
  })
}

// 导出图片素材
export function exportImage(query) {
  return request({
    url: '/material/image/export',
    method: 'get',
    params: query
  })
}

// 改变视频状态
export function changeStatusImage(data) {
  return request({
    url: '/material/image/mode',
    method: 'put',
    data: data
  })
}

// 初始化时调用，确定批处理那两个按钮的状态
export function statusButton() {
  return request({
    url: '/material/image/status',
    method: 'get'
  })
}

// 导入/处理素材（批操作，其中：1导入，2处理）
export function optionImage(optionalId) {
  return request({
    url: '/material/image/option/' + optionalId,
    method: 'get'
  })
}
