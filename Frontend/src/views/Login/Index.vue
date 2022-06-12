<template>
  <div class="login">
    <div class="box">
      <span id="login-span">登陆页面</span>
      <el-form
          :model="ruleForm"
          status-icon
          :rules="rules"
          ref="ruleForm"
          label-width="100px"
          class="demo-ruleForm">
        <el-form-item label="账号" prop="user">
          <el-input type="text" v-model="ruleForm.user" autocomplete="off" placeholder="请输入账号"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pwd">
          <el-input type="password" v-model="ruleForm.pwd" autocomplete="off" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item class="ppp">
          <el-button type="success" @click="toRegister" style="float: left">注册</el-button>
          <el-button @click="returnHome" style="float: right">取消</el-button>
          <el-button type="primary" @click="submitForm('ruleForm')" style="float: right">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import {setStore} from '@/utils/storage'
import {MessageBox} from 'element-ui'

export default {
  data() {
    let validateUser = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入账号'))
      } else {
        callback()
      }
    }

    let validatePwd = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        callback()
      }
    }

    return {
      ruleForm: {
        user: '',
        pwd: ''
      },

      rules: {
        user: [{validator: validateUser, trigger: 'blur'}],
        pwd: [{validator: validatePwd, trigger: 'blur'}],
      }
    }
  },

  methods: {
    toRegister() {
      this.$router.push({
        name: 'register'
      })
    },

    returnHome() {
      this.$router.push({
        name: 'home'
      })
    },

    submitForm(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          let {user, pwd} = this.ruleForm
          let res = await this.$http.post('http://127.0.0.1:8000/api/login',
              {'username': user, 'password': pwd})
          if (res.data.code === 1) {
            let token = res.data.token
            let username = res.data.user
            let head = res.data.head
            setStore('token', token)
            setStore('user', username)
            setStore('head', head)
            await this.$router.push({
              name: 'home'
            })
          } else {
            await MessageBox.alert('<h2 style="color: red">账号或密码错误</h2>', {
              dangerouslyUseHTMLString: true
            })
          }
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
  }

}
;
</script>

<style lang="scss" scoped>

::v-deep #login-span {
  position: relative;
  left: 38px
}

::v-deep .login .box[data-v-2014ec42] {
  padding: 61px 50px 50px 10px
}

.ppp {
  //margin-right: -138px;
}

.login {
  position: relative;
  overflow: visible;
  background: #ededed;

  .box {
    width: 530px;
    border: 1px solid #dadada;
    border-radius: 10px;
    position: absolute;
    top: 100px;
    left: 45%;
    padding: 50px 50px 50px 10px;
    margin-left: -225px;
    box-shadow: 0 9px 30px -6px rgba(0, 0, 0, 0.2),
    0 18px 20px -10px rgba(0, 0, 0, 0.04),
    0 18px 20px -10px rgba(0, 0, 0, 0.04),
    0 10px 20px -10px rgba(0, 0, 0, 0.04);
    text-align: center;

    form {
      margin-top: 30px;
    }

    span {
      color: #333;
      font-weight: 400;
    }
  }
}
</style>
