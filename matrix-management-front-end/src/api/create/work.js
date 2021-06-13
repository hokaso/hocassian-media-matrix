import request from '@/utils/request'

// 查询作品管理列表
export function listWork(query) {
  return request({
    url: '/create/work/list',
    method: 'get',
    params: query
  })
}

// 查询作品管理详细
export function getWork(workStoryId) {
  return request({
    url: '/create/work/' + workStoryId,
    method: 'get'
  })
}

// 新增作品管理
export function addWork(data) {
  return request({
    url: '/create/work',
    method: 'post',
    data: data
  })
}

// 修改作品管理
export function updateWork(data) {
  return request({
    url: '/create/work',
    method: 'put',
    data: data
  })
}

// 删除作品管理
export function delWork(workStoryId) {
  return request({
    url: '/create/work/' + workStoryId,
    method: 'delete'
  })
}

// 导出作品管理
export function exportWork(query) {
  return request({
    url: '/create/work/export',
    method: 'get',
    params: query
  })
}