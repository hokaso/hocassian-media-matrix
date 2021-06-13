import request from '@/utils/request'

// 查询媒体单位列表
export function listUnit(query) {
  return request({
    url: '/publish/unit/list',
    method: 'get',
    params: query
  })
}

// 查询媒体单位详细
export function getUnit(unitId) {
  return request({
    url: '/publish/unit/' + unitId,
    method: 'get'
  })
}

// 新增媒体单位
export function addUnit(data) {
  return request({
    url: '/publish/unit',
    method: 'post',
    data: data
  })
}

// 修改媒体单位
export function updateUnit(data) {
  return request({
    url: '/publish/unit',
    method: 'put',
    data: data
  })
}

// 删除媒体单位
export function delUnit(unitId) {
  return request({
    url: '/publish/unit/' + unitId,
    method: 'delete'
  })
}

// 导出媒体单位
export function exportUnit(query) {
  return request({
    url: '/publish/unit/export',
    method: 'get',
    params: query
  })
}