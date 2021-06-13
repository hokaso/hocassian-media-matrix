<template>
  <el-footer style="height:120px;" class="footer">
    <div class="cpr">
      <div style="padding-top: 30px;">
        <span>{{ about.aboutCopyright }}</span>
      </div>
      <a class="icp" href="http://beian.miit.gov.cn" target="_blank">
        <span>{{ about.aboutRecord }}</span>
      </a>
    </div>
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
.cpr {
  display: block;
  text-align: center;
  color: #8a8a8a;
  line-height: 30px;
}
.el-footer {
  background-color: #373737;
  color: #333;
  text-align: center;
  line-height: 60px;
}
.footer {
  @media screen and (max-width: 768px) {
    font-size: 12px;
  }
  @media screen and (min-width: 768px) {
    font-size: 16px;
  }
}
</style>
