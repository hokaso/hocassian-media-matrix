<template>
  <el-footer class="footer__wrap">
    <p>{{ about.aboutCopyright }}</p>
    <a href="http://beian.miit.gov.cn" target="_blank">
      <span>{{ about.aboutRecord }}</span>
    </a>
  </el-footer>
</template>

<script>
  import { mapGetters } from "vuex";
  export default {
    name: "EndPart",
    computed: {
      ...mapGetters(["about"])
    }
  };
</script>

<style lang="scss">
.footer__wrap {
  text-align: center;
  color: #8a8a8a;
  background-color: #373737;
  height: 120px !important;
  display: flex;
  flex-direction: column;
  justify-content: center;
  & > p {
    margin-bottom: 25px;
  }
  @media screen and (max-width: 768px){
    font-size: 12px;
  }
    @media screen and (min-width: 768px){
    font-size: 16px;
  }
}
</style>
