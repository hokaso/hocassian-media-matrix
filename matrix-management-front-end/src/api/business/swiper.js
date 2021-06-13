import request from '@/utils/request'

// 查询主页轮播图列表
export function listSwiper(query) {
  return request({
    url: '/business/swiper/list',
    method: 'get',
    params: query
  })
}

// 查询主页轮播图详细
export function getSwiper(id) {
  return request({
    url: '/business/swiper/' + id,
    method: 'get'
  })
}

// 新增主页轮播图
export function addSwiper(data) {
  return request({
    url: '/business/swiper',
    method: 'post',
    data: data
  })
}

// 修改主页轮播图
export function updateSwiper(data) {
  return request({
    url: '/business/swiper',
    method: 'put',
    data: data
  })
}

// 删除主页轮播图
export function delSwiper(id) {
  return request({
    url: '/business/swiper/' + id,
    method: 'delete'
  })
}

// 导出主页轮播图
export function exportSwiper(query) {
  return request({
    url: '/business/swiper/export',
    method: 'get',
    params: query
  })
}

// 改变视频状态
export function changeStatusSwiper(data) {
  return request({
    url: '/business/swiper/status',
    method: 'put',
    data: data
  })
}
