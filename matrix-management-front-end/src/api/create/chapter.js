import request from '@/utils/request'

// 查询篇章管理列表
export function listChapter(query) {
  return request({
    url: '/create/chapter/list',
    method: 'get',
    params: query
  })
}

// 查询篇章管理详细
export function getChapter(chapterStoryId) {
  return request({
    url: '/create/chapter/' + chapterStoryId,
    method: 'get'
  })
}

// 新增篇章管理
export function addChapter(data) {
  return request({
    url: '/create/chapter',
    method: 'post',
    data: data
  })
}

// 修改篇章管理
export function updateChapter(data) {
  return request({
    url: '/create/chapter',
    method: 'put',
    data: data
  })
}

// 删除篇章管理
export function delChapter(chapterStoryId) {
  return request({
    url: '/create/chapter/' + chapterStoryId,
    method: 'delete'
  })
}

// 导出篇章管理
export function exportChapter(query) {
  return request({
    url: '/create/chapter/export',
    method: 'get',
    params: query
  })
}