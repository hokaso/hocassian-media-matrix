import request from '@/utils/request'

// 查询视频管理列表
export function listVideo(data) {
  return request({
    url: '/business/video/list',
    method: 'get',
    params: data
  })
}

// 查询视频管理详细
export function getVideo(videoId) {
  return request({
    url: '/business/video/' + videoId,
    method: 'get'
  })
}

// 新增视频管理
export function addVideo(data) {
  return request({
    url: '/business/video',
    method: 'post',
    data: data
  })
}

// 修改视频管理
export function updateVideo(data) {
  return request({
    url: '/business/video',
    method: 'put',
    data: data
  })
}

// 删除视频管理
export function delVideo(videoId) {
  return request({
    url: '/business/video/' + videoId,
    method: 'delete'
  })
}

// 导出视频管理
export function exportVideo(query) {
  return request({
    url: '/business/video/export',
    method: 'get',
    params: query
  })
}

// 改变视频状态
export function changeStatusVideo(data) {
  return request({
    url: '/business/video/status',
    method: 'put',
    data: data
  })
}
