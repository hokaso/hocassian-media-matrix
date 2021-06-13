<template>
  <div>
    <my-swiper />
    <grid-switch />
    <irregular-container />
<!--    <div class="dashboard-container"></div>-->
  </div>
</template>

<script>
  import MySwiper from "@/components/Swiper";
  import GridSwitch from "@/components/GridSwitch";
  import IrregularContainer from "@/components/IrregularContainer";
   // import Recommend from '@/components/Recommend'
  export default {
    components: { MySwiper, GridSwitch,IrregularContainer },
    data () {
      return {
        name: '123'
      }
    },
    name: 'Home',
    computed: {
    }
  }
</script>

<style lang="scss" scoped>
  .dashboard {
    &-container {
      margin: 80px;
    }
    &-text {
      font-size: 30px;
      line-height: 46px;
    }
  }
</style>
