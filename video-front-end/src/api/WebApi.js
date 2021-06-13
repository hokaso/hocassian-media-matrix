import HttpKit from '@/utils/http-kit'

export default {
  findAboutInfo () {
    return  HttpKit.get(`/client/about/info`).then(
        res => res.data
    )
  },
  findAllSwiper (form) {
    return HttpKit.post(`/client/swiper/list`, form).then(
      res => res
    )
  },
  findAllVideo (data) {
    const form = {
      params: data
    };
    return HttpKit.get(`/client/video/list`, form).then(
      res => res
    )
  },
  findOneVideo (videoId) {
    return HttpKit.get(`/client/video/${videoId}`).then(
      res => res.data
    )
  }
}
