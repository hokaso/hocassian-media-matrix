import request from '@/utils/request'

// 查询视频素材列表
export function listClip(query) {
  return request({
    url: '/material/clip/list',
    method: 'get',
    params: query
  })
}

// 初始化时调用，确定批处理那两个按钮的状态
export function statusButton() {
  return request({
    url: '/material/clip/status',
    method: 'get'
  })
}

// 导入/处理素材（批操作，其中：1导入，2处理）
export function optionClip(optionalId) {
  return request({
    url: '/material/clip/option/' + optionalId,
    method: 'get'
  })
}

// 查询视频素材详细
export function getClip(materialId) {
  return request({
    url: '/material/clip/' + materialId,
    method: 'get'
  })
}

// 新增视频素材
export function addClip(data) {
  return request({
    url: '/material/clip',
    method: 'post',
    data: data
  })
}

// 修改视频素材
export function updateClip(data) {
  return request({
    url: '/material/clip',
    method: 'put',
    data: data
  })
}

// 删除视频素材
export function delClip(materialId) {
  return request({
    url: '/material/clip/' + materialId,
    method: 'delete'
  })
}

// 导出视频素材
export function exportClip(query) {
  return request({
    url: '/material/clip/export',
    method: 'get',
    params: query
  })
}

// 改变视频状态
export function changeStatusClip(data) {
  return request({
    url: '/material/clip/mode',
    method: 'put',
    data: data
  })
}
