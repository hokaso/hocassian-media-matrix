<template>
    <div>
        <el-carousel
                v-if="!isMobile"
                :interval="5000"
                arrow="always"
                trigger="click"
                height="450px"
        >
            <el-carousel-item v-for="item in list" :key="item.id" class="img-container">
                <img :src="item.swiperPic" class="banner_img" alt=""/>
            </el-carousel-item>
        </el-carousel>
        <swiper v-else class="home_swiper" :options="swiperOption">
            <swiper-slide class="swiper-item" v-for="banner in list" :key="banner.id">
                <img :src="banner.swiperPic" class="full"/>
            </swiper-slide>
            <div class="swiper-button-prev" slot="button-prev"></div>
            <div class="swiper-button-next" slot="button-next"></div>
        </swiper>
    </div>
</template>

<script>
    import WebApi from "@/api/WebApi";
    import {mapState} from "vuex";

    export default {
        data() {
            return {
                newArr: [],
                total: "",
                swiperPic: "",
                list: [],
                swiperOption: {
                    spaceBetween: 30,
                    centeredSlides: true,
                    autoplay: {
                        delay: 2500,
                        disableOnInteraction: false
                    },
                    navigation: {
                        nextEl: ".swiper-button-next",
                        prevEl: ".swiper-button-prev"
                    }
                },
                form: {
                    pageNum: 1,
                    pageSize: 10
                }
            };
        },
        created() {
            this.getRefresh();
        },
        methods: {
            getRefresh() {
                WebApi.findAllSwiper(this.form).then(data => {
                    this.list = data.rows;
                    Object.keys(this.list).forEach(
                        key => {
                            this.list[key].swiperPic =
                                "/prod-api/profile/video_matrix/" + this.list[key].swiperPic
                        }
                    );
                });
            }
        },
        computed: {
            ...mapState('app', ["isMobile"])
        }
    };
</script>

<style lang="scss" scoped>
    .home_swiper {
        // max-height: 450px;
        .swiper-item {
            height: 100%;
            text-align: center;
            font-size: 18px;
            background: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
        }
    }

    .full {
        width: 100%;
        height: 100%;
    }

    .img-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
