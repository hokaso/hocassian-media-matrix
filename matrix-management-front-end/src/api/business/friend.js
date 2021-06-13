import request from '@/utils/request'

// 查询友情链接列表
export function listFriend(query) {
  return request({
    url: '/business/friend/list',
    method: 'get',
    params: query
  })
}

// 查询友情链接详细
export function getFriend(friendId) {
  return request({
    url: '/business/friend/' + friendId,
    method: 'get'
  })
}

// 新增友情链接
export function addFriend(data) {
  return request({
    url: '/business/friend',
    method: 'post',
    data: data
  })
}

// 修改友情链接
export function updateFriend(data) {
  return request({
    url: '/business/friend',
    method: 'put',
    data: data
  })
}

// 删除友情链接
export function delFriend(friendId) {
  return request({
    url: '/business/friend/' + friendId,
    method: 'delete'
  })
}

// 导出友情链接
export function exportFriend(query) {
  return request({
    url: '/business/friend/export',
    method: 'get',
    params: query
  })
}