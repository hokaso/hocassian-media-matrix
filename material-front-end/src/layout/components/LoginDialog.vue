<template>
  <el-dialog
    title="登 录"
    :visible.sync="visible"
    width="400px"
    center
    :destroy-on-close="true"
    :close-on-click-modal="false"
    :close-on-press-escape="false">
    <el-form
      ref="form"
      :model="form"
      :rules="rules">
      <el-form-item prop="account">
        <el-input
          placeholder="账号"
          v-model.trim="form.account"
          @keyup.enter.native="login()"
          clearable>
          <i slot="prefix" class="el-input__icon el-icon-user iconSize" />
        </el-input>
      </el-form-item>
      <el-form-item prop="passWord">
        <el-input
          placeholder="密码"
          v-model.trim="form.passWord"
          type="password"
          @keyup.enter.native="login()"
          clearable>
          <i slot="prefix" class="el-input__icon el-icon-lock iconSize" />
        </el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="closeDialog()">取 消</el-button>
      <el-button @click="login()">登 录</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { login, getInfo } from '@/api/login';
import { setToken } from '@/utils/auth';
import { mapMutations, mapGetters } from 'vuex';

export default {
  data() {
    return {
      form: {
        account: '',
        passWord: '',
      },
      rules: {
        account: [
          { required: true, message: '请输入账号', trigger: 'blur' }
        ],
        passWord: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    };
  },
  computed: {
    ...mapGetters(['loginAgain']),
    visible: {
      set(v) {
        this.SET_LOGINAGAIN(v);
      },
      get() {
        return this.loginAgain;
      }
    }
  },
  methods: {
    ...mapMutations([
      'SET_AVATAR',
      'SET_LOGINAGAIN'
    ]),
    closeDialog() {
      this.SET_LOGINAGAIN(false);
      this.$refs.form.resetFields();
    },
    checkForm() {
      let flag = false;
      this.$refs.form.validate((valid) => {
        flag = valid;
      });
      return flag;
    },
    async login() {
      if(!this.checkForm()) return;
      setToken('');
      const res = await login({
        username: this.form.account,
        password: this.form.passWord
      });
      if (res.code === 200) {
        setToken(res.token);
        const { user } = await getInfo();
        const avatar = user.avatar == "" ? "@/assets/images/profile.jpg" : process.env.VUE_APP_BASE_API + user.avatar;
        this.SET_AVATAR(avatar);
        this.$emit('loginSuccess', true);
        this.closeDialog();
        location.href="/newest";
      }
    }
  },
}
</script>

<style>
.iconSize {
  font-size: 20px;
}
</style>