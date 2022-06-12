<template>
  <div class="login">
    <div class="box">
      <span id="login-span">注册页面</span>
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

        <el-form-item label="确认密码" prop="repwd">
          <el-input type="password" v-model="ruleForm.repwd" autocomplete="off" placeholder="请再次输入密码"></el-input>
        </el-form-item>

        <el-form-item label="头像" prop="head">
          <el-upload
              class="upload-demo"
              ref="uploadImage"
              action="http://127.0.0.1:8000/api/Upload"
              :on-remove="removeHead"
              :on-change="changeHead"
              :file-list="fileListHead"
              list-type="picture"
              :auto-upload="false"
              name="head" style="float: left">
            <el-button size="small" type="primary">点击上传</el-button>
          </el-upload>
        </el-form-item>

        <el-form-item class="ppp">
          <el-button type="primary" @click="submitForm('ruleForm')">确定</el-button>
          <el-button @click="returnLogin">取消</el-button>
        </el-form-item>

      </el-form>
    </div>
  </div>
</template>

<script>
import {setStore} from '@/utils/storage';
import {MessageBox, Notification} from "element-ui";

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
    let validateRePwd = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else {
        callback()
      }
    }

    return {
      fileListHead: [],
      ruleForm: {
        user: '',
        pwd: '',
        repwd: '',
      },

      rules: {
        user: [{validator: validateUser, trigger: 'blur'}],
        pwd: [{validator: validatePwd, trigger: 'blur'}],
        repwd: [{validator: validateRePwd, trigger: 'blur'}],
      }
    }
  },

  methods: {

    removeHead(file, fileList) {
      this.fileListHead = fileList
    },

    changeHead(file, fileList) {
      this.fileListHead = fileList
    },

    toRegister() {
      this.$router.push({
        name: 'register'
      })
    },

    returnLogin() {
      this.$router.push({
        name: 'login'
      })
    },

    submitForm(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          let formData = new FormData()

          this.fileListHead.forEach(file => {
            formData.append("head", file.raw);
          })

          formData.append("username", this.ruleForm.user)
          formData.append("password", this.ruleForm.pwd)
          formData.append("rePassword", this.ruleForm.repwd)

          let res = await this.$http.post('http://127.0.0.1:8000/api/register', formData, {
            headers: {"Content-Type": "multipart/form-data"},
          })

          if (res.data.code === 200) {
            // 提示注册成功
            Notification({
              title: '注册成功',
              type: 'success',
              duration: 3000,
              offset: 100
            })
            await this.$router.push({
              name: 'login'
            })
          } else if (res.data.code === 300) {
            // 警告 两次密码不同
            await MessageBox.alert('<h2 style="color: red">两次密码不相同</h2>', {
              dangerouslyUseHTMLString: true
            })
          } else if (res.data.code === 400) {
            // 警告账号已存在
            await MessageBox.alert('<h2 style="color: red">账号已存在</h2>', {
              dangerouslyUseHTMLString: true
            })
          } else if (res.data.code === 500) {
            // 警告请上传头像
            await MessageBox.alert('<h2 style="color: red">请上传头像</h2>', {
              dangerouslyUseHTMLString: true
            })
          } else {
            // 警告注册不成功
            await MessageBox.alert('<h2 style="color: red">注册失败</h2>', {
              dangerouslyUseHTMLString: true
            })
          }
        } else {
          console.log('error submit!!');
          return false;
        }
      })
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
  margin-left: 218px;
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
