<template>
    <div class="layout-container">
        <m-header>
            <div slot="nav"></div>
        </m-header>
        <div class="w">
            <div class="content">
                <div class="form-title">请输入商品信息</div>
                <el-form :model="ruleForm" :rules="rules" ref="ruleForm" class="form">

                    <el-form-item label="商品名称" :label-width="formLabelWidth" prop="name">
                        <el-input v-model="ruleForm.name" autocomplete="off"></el-input>
                    </el-form-item>

                    <el-form-item label="价格" :label-width="formLabelWidth" prop="price">
                        <el-input v-model="ruleForm.price" autocomplete="off"></el-input>
                    </el-form-item>

                    <el-form-item label="子标题" :label-width="formLabelWidth" prop="subTitle">
                        <el-input v-model="ruleForm.subTitle" autocomplete="off"></el-input>
                    </el-form-item>

                    <el-form-item label="图片" :label-width="formLabelWidth" prop="image">
                        <el-upload
                            class="upload-demo"
                            ref="uploadImage"
                            action="http://127.0.0.1:8000/api/Upload"
                            :on-remove="removeImage"
                            :on-change="changeImage"
                            :file-list="fileListImage"
                            list-type="picture"
                            :auto-upload="false"
                            name="image">
                            <el-button size="small" type="primary">点击上传 (请选择一张图片)</el-button>
                        </el-upload>
                    </el-form-item>

                    <el-form-item label="详情图片" :label-width="formLabelWidth" prop="detail">
                        <el-upload
                            class="upload-demo"
                            ref="uploadDetail"
                            action="http://127.0.0.1:8000/api/Upload"
                            :on-remove="removeDetail"
                            :on-change="changeDetail"
                            :file-list="fileListDetail"
                            list-type="picture"
                            :auto-upload="false"
                            name="detail">
                            <el-button size="small" type="primary">点击上传 (请选择一张图片)</el-button>
                        </el-upload>
                    </el-form-item>

                    <el-form-item label="小图片" :label-width="formLabelWidth" prop="smallImage">
                        <el-upload
                            class="upload-demo"
                            ref="uploadSmallImage"
                            action="http://127.0.0.1:8000/api/Upload"
                            :on-remove="removeSmallImage"
                            :on-change="changeSmallImage"
                            :file-list="fileListSmallImage"
                            list-type="picture"
                            :auto-upload="false"
                            name="smallImage"
                            multiple>
                            <el-button size="small" type="primary">点击上传 (最多选择4张图片)</el-button>
                        </el-upload>
                    </el-form-item>

                    <el-form-item class="submit123">
                        <el-button @click="cancelrelace">取 消</el-button>
                        <el-button type="primary" @click="submitForm('ruleForm')">确 定</el-button>
                    </el-form-item>

                </el-form>
            </div>
        </div>


    </div>
</template>

<script>
import {getStore} from '@/utils/storage'
import MHeader from '@/common/MHeader'
import {Notification} from 'element-ui'


export default {
    name: "Sale",

    components: {
        MHeader,
    },

    data() {
        let validateName = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入商品名称'))
            } else {
                callback()
            }
        }

        let validatePrice = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入商品价格'))
            } else {
                callback()
            }
        }

        let validateSubTitle = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入商品子标题'))
            } else {
                callback()
            }
        }

        return {
            // 新建商品
            ruleForm: {
                name: '',
                price: '',
                subTitle: '',
            },
            formLabelWidth: '120px',

            rules: {
                name: [{validator: validateName, trigger: 'blur'}],
                price: [{validator: validatePrice, trigger: 'blur'}],
                subTitle: [{validator: validateSubTitle, trigger: 'blur'}],
            },

            fileListImage: [],
            fileListDetail: [],
            fileListSmallImage: [],
        }
    },

    methods: {
        removeImage(file, fileList) {
            this.fileListImage = fileList
        },

        changeImage(file, fileList) {
            this.fileListImage = fileList
        },

        removeDetail(file, fileList) {
            this.fileListDetail = fileList
        },

        changeDetail(file, fileList) {
            this.fileListDetail = fileList
        },

        removeSmallImage(file, fileList) {
            this.fileListSmallImage = fileList
        },

        changeSmallImage(file, fileList) {
            this.fileListSmallImage = fileList
            console.log(this.fileListSmallImage)
        },

        // 表单提交
        submitForm(formName) {
            this.$refs[formName].validate(async (valid) => {
                if (valid) {
                    let formData = new FormData()

                    this.fileListImage.forEach(file => {
                        formData.append("image", file.raw);
                    })

                    this.fileListDetail.forEach(file => {
                        formData.append("detail", file.raw);
                    })

                    this.fileListSmallImage.forEach(file => {
                        formData.append("smallImage", file.raw);
                    })

                    formData.append("name", this.ruleForm.name)
                    formData.append("price", this.ruleForm.price)
                    formData.append("subTitle", this.ruleForm.subTitle)

                    const res = await this.$http.post("http://127.0.0.1:8000/api/RelaseGoods", formData, {
                        headers: {"Content-Type": "multipart/form-data"},
                        params: {
                            token: getStore('token')
                        }
                    })
                    if (res.data === 200) {
                        Notification({
                            title: '发布商品成功',
                            type: 'success',
                            duration: 3000,
                            offset: 100
                        })
                    } else {
                        Notification.error({
                            title: '发布商品失败',
                            duration: 3000,
                            offset: 100
                        })
                    }


                    this.$refs.uploadImage.submit()
                    this.$refs.uploadDetail.submit()
                    this.$refs.uploadSmallImage.submit()
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },

        cancelrelace() {
            this.$router.push('/')
        },

        async getSale() {
            try {
                const token = getStore('token')
                if (token) {
                    const res = await this.$http.get("http://127.0.0.1:8000/api/user", {
                        params: {
                            token: token
                        }
                    })
                    this.content = res.data
                } else {
                    await this.$router.push({
                        name: 'login'
                    })
                }
            } catch (e) {
                console.log(e)
            }
        },

        isLogin() {
            let token = getStore("token")
            if (!token) {
                this.$router.push({
                    path: 'login'
                })
            }
        }
    },

    created() {
        this.isLogin()
        this.getSale()
    },
}
</script>

<style scoped>
.submit123 {
    padding-left: 730px;
    margin-bottom: 0;
}

.form {
    padding: 20px 200px 50px 132px;
}

.form-title {
    text-align: center;
    margin: 25px auto 0;
    font-size: 25px;
}

.avatar {
    width: 178px;
    height: 178px;
    display: block;
}
</style>
