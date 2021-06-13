import request from '@/utils/request'

// 游客 - 获取图片素材
export function imageList(data) {
  return request({
    url: '/client/material/image/list',
    method: 'get',
    params: data
  })
}

// 获取图片关键词
export function imageKeyword() {
  return request({
    url: '/client/material/image/keywords',
    method: 'get'
  })
}

// 会员 - 获取图片素材
export function memberImageList(data) {
  return request({
    url: '/material/image/list',
    method: 'get',
    params: data
  })
}