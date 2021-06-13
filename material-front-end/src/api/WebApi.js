import request from '@/utils/request'

// 获取矩阵基本信息
export function findAboutInfo() {
  return request({
    url: '/client/about/info',
    method: 'get'
  })
}

// 获取音频素材的轮播图
export function findAllSwiper(data) {
  return request({
    url: '/client/swiper/list',
    method: 'post',
    data: data
  })
}

// 获取音频素材
export function musicList(data) {
  return request({
    url: '/client/material/audio/list',
    method: 'get',
    params: data
  })
}

// 获取音频图片
export function musicPic() {
  return request({
    url: '/client/material/image/colorful',
    method: 'get'
  })
}

// 会员获取音频素材
export function memberMusicList(data) {
  return request({
    url: '/material/audio/list',
    method: 'get',
    params: data
  })
}

// 获取音频素材关键字
export function musicKeyword() {
  return request({
    url: '/client/material/audio/keywords',
    method: 'get'
  })
}

export function findAllClip(query) {
  return request({
    url: '/client/material/clip/list',
    method: 'get',
    params: query
  })
}

export function queryMemberVideoList(data) {
  return request({
    url: '/material/clip/list',
    method: 'get',
    params: data
  })
}

export function keyword() {
  return request({
    url: '/client/material/clip/keywords',
    methods: 'get'
  })
}
