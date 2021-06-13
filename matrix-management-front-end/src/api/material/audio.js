import request from '@/utils/request'

// 查询音频素材列表
export function listAudio(query) {
  return request({
    url: '/material/audio/list',
    method: 'get',
    params: query
  })
}

// 初始化时调用，确定批处理那两个按钮的状态
export function statusButton() {
  return request({
    url: '/material/audio/status',
    method: 'get'
  })
}

// 导入/处理素材（批操作，其中：1导入，2处理）
export function optionAudio(optionalId) {
  return request({
    url: '/material/audio/option/' + optionalId,
    method: 'get'
  })
}

// 查询音频素材详细
export function getAudio(audioId) {
  return request({
    url: '/material/audio/' + audioId,
    method: 'get'
  })
}

// 新增音频素材
export function addAudio(data) {
  return request({
    url: '/material/audio',
    method: 'post',
    data: data
  })
}

// 修改音频素材
export function updateAudio(data) {
  return request({
    url: '/material/audio',
    method: 'put',
    data: data
  })
}

// 删除音频素材
export function delAudio(audioId) {
  return request({
    url: '/material/audio/' + audioId,
    method: 'delete'
  })
}

// 导出音频素材
export function exportAudio(query) {
  return request({
    url: '/system/audio/export',
    method: 'get',
    params: query
  })
}

// 改变视频状态
export function changeStatusAudio(data) {
  return request({
    url: '/material/audio/mode',
    method: 'put',
    data: data
  })
}
