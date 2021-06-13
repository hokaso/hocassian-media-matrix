<template>
    <el-carousel
            :interval="5000"
            direction="vertical"
            arrow="always"
            trigger="click"
            height="450px"
    >
        <el-carousel-item v-for="item in list" :key="item.id" class="img-container">
            <img :src="item.swiperPic" class="banner_img" alt=""/>
        </el-carousel-item>
    </el-carousel>
    <!--  <el-carousel height="150px">-->
    <!--    <el-carousel-item v-for="item in 4" :key="item">-->
    <!--      <h3 class="small">{{ item }}</h3>-->
    <!--    </el-carousel-item>-->
    <!--  </el-carousel>-->
</template>

<script>
    import WebApi from "@/api/WebApi";

    export default {
        name: "Swiper",
        data() {
            return {
                newArr: [],
                total: '',
                swiperPic: '',
                list: [],
                form: {
                    pageNum: 1,
                    pageSize: 10
                }
            }
        },
        created() {
            this.getRefresh()
        },
        methods: {
            getRefresh() {
                WebApi.findAllSwiper(this.form).then(data => {
                    this.list = data.rows;
                    Object.keys(this.list).forEach(key => {
                            this.list[key].swiperPic = '/prod-api/profile/video_matrix/' + this.list[key].swiperPic
                        }
                    )
                })
            }
        }
    }
</script>
<style lang="scss" scoped>

    .img-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
