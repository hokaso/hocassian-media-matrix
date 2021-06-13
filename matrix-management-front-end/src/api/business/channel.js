import request from '@/utils/request'

// 查询频道管理列表
export function listChannel(query) {
  return request({
    url: '/business/channel/list',
    method: 'get',
    params: query
  })
}

// 查询频道管理详细
export function getChannel(channelId) {
  return request({
    url: '/business/channel/' + channelId,
    method: 'get'
  })
}

// 新增频道管理
export function addChannel(data) {
  return request({
    url: '/business/channel',
    method: 'post',
    data: data
  })
}

// 修改频道管理
export function updateChannel(data) {
  return request({
    url: '/business/channel',
    method: 'put',
    data: data
  })
}

// 删除频道管理
export function delChannel(channelId) {
  return request({
    url: '/business/channel/' + channelId,
    method: 'delete'
  })
}

// 导出频道管理
export function exportChannel(query) {
  return request({
    url: '/business/channel/export',
    method: 'get',
    params: query
  })
}
