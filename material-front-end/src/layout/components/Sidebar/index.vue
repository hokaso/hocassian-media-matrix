<template>
  <div class='container'>

    <el-menu
      :default-active="activeIndex"
      :background-color="variables.menuBg"
      :text-color="variables.menuText"
      :active-text-color="variables.menuActiveText"
      mode="horizontal"
    >
      <img
        class="logo"
        :src="'/prod-api/profile/video_matrix/' + about.aboutIcon"
        alt=""
      />
      <head-nav v-for="route in permission_routes" :key="route.path" :item="route" :base-path="route.path"/>
    </el-menu>
    <div class="container__login">
      <div class="login--tutorial">
        <a href="https://hocassian.feishu.cn/docs/doccnMQlI9vgr275f7ivTuj9BWb#" target="_blank">使用手册</a>
      </div>
      <div
        v-if="!loginSuccess"
        @click="openLogin()">
        登录
      </div>
      <div
        v-if="loginSuccess"
        slot="reference"
        :style="{'background-image': `url(${avatar})`}"
        class="login--image"
        @click="poverVisible = !poverVisible">
        <Popver
          v-show="poverVisible"
          class="popver">
          <el-button
            type="text"
            slot="container"
            @click.stop="logout()">
            登出
          </el-button>
        </Popver>
      </div>
    </div>
    <LoginDialog
      ref="LoginDialog"
      @loginSuccess="loginSuccess = $event"/>
  </div>
</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'
  import HeadNav from './HeadNav'
  import variables from '@/assets/styles/variables.scss'
  import LoginDialog from '../LoginDialog.vue'
  import Popver from './Popver.vue'
  import { getToken, setToken } from '@/utils/auth'
  import { getInfo } from '@/api/login'

  export default {
    components: { HeadNav, LoginDialog, Popver },
    computed: {
      ...mapGetters([
        'permission_routes',
        'avatar',
        'token',
        'loginAgain',
        'about'
      ]),
      activeIndex() {
        const route = this.$route
        const { meta, path } = route
        // if set path, the sidebar will highlight the path you set
        if (meta.activeMenu) {
          return meta.activeMenu
        }
        return path
      },
      variables() {
        return variables
      }
    },
    async created() {
      const token = getToken()
      if (token !== '' && token !== undefined) {
        const { user } = await getInfo()
        const avatar = user.avatar == '' ? '@/assets/images/profile.jpg' : process.env.VUE_APP_BASE_API + user.avatar
        this.SET_AVATAR(avatar)
        this.loginSuccess = true
      }
    },
    data() {
      return {
        loginSuccess: false,
        poverVisible: false
      }
    },
    methods: {
      ...mapMutations([
        'SET_LOGINAGAIN',
        'SET_AVATAR'
      ]),
      openLogin() {
        this.SET_LOGINAGAIN(true)
      },
      logout() {
        setToken('')
        this.SET_AVATAR('')
        this.loginSuccess = false
        this.poverVisible = false
        location.href = '/newest'
      }
    }
  }
</script>
<style lang="scss" scoped>
  .container {
    display: flex;
    position: relative;
  }

  .el-menu {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .container__login {
    height: 56px;
    font-size: 14px;
    color: #949494;
    position: absolute;
    display: flex;
    align-items: center;
    right: 30px;

    & > div {
      height: 20px;
      cursor: pointer;
    }

    & > div:hover {
      color: #fffafa;
    }

    .login--image {
      border-radius: 50%;
      width: 40px;
      height: 40px;
      background-size: 100% 100%;
    }

    .login--tutorial {
      padding-right: 30px;
    }

    .popver {
      width: 120px;
      top: 56px;
      right: -20px;
      z-index: 999;
    }
  }

  .logout {
    text-align: center;
    cursor: pointer;
  }
</style>

