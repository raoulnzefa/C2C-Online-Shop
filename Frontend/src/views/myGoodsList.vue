<template>
    <div>
        <m-shelf title="我的商品">
            <div slot="content">
                <div v-for="(item,i) in myGoodsList" :key="i">
                    <!--          <div class="gray-sub-title cart-title">-->
                    <!--            <div class="first">-->
                    <!--              <div>-->
                    <!--                <span class="order-id" style="display: none"> 订单号：{{ item.id }}</span>-->
                    <!--              </div>-->
                    <!--              <div class="f-bc">-->
                    <!--                <span class="price">单价</span>-->
                    <!--                <span class="subTitle">子标题</span>-->
                    <!--                <span class="img">图片</span>-->
                    <!--                <span class="img">详情图片</span>-->
                    <!--                <span class="img">小图片</span>-->
                    <!--                <span class="img">操作</span>-->
                    <!--              </div>-->
                    <!--            </div>-->
                    <!--          </div>-->

                    <div class="pr">
                        <div class="cart">
                            <div class="cart-l" :class="{bt:1>0}">

                                <div class="car-l-l">
                                    <div class="img-box"><img :src="item.image" alt=""></div>
                                    <div class="ellipsis">{{ item.name }}</div>
                                </div>

                                <div class="cart-l-r">
                                    <div>¥ {{ Number(item.price).toFixed(2) }}</div>
                                    <div>{{ item.sub_title }}</div>
                                    <el-button type="info" plain @click="showImage(item.image)">查看图片</el-button>
                                    <el-button type="info" plain @click="showDetail(item.detail)">查看详情图片</el-button>
                                    <el-button type="info" plain @click="showSmallImage(item.small_image)">查看小图片
                                    </el-button>
                                    <el-button type="info" plain @click="editMyGoods(item.id)">编辑商品</el-button>

                                </div>

                            </div>
                        </div>
                    </div>
                </div>


                <div style="padding: 100px 0;text-align: center" v-if="myGoodsList.length === 0">
                    我的商品为空
                </div>


                <el-dialog title="商品图片" :visible.sync="imageVisible">
                    <img :src="imageURL" alt="" v-if="imageURL" style="width: 100%; height: 100%">
                </el-dialog>

                <el-dialog title="商品详情图片" :visible.sync="detailVisible">
                    <img :src="detailURL" alt="" v-if="detailURL" style="width: 100%; height: 100%">
                </el-dialog>

                <el-dialog title="商品小图片" :visible.sync="smallImageVisible">
                    <div class="gallery-wrapper">
                        <div class="gallery">
                            <div class="thumbnail">
                                <ul>
                                    <li v-for="(item, i) in small" :key="i" :class="{on:item===big}"
                                        @click="handleClick(item)">
                                        <img :src='item' alt="">
                                    </li>
                                </ul>
                            </div>
                            <div class="thumb">
                                <div class="big">
                                    <img :src='big' alt="">
                                </div>
                            </div>
                        </div>
                    </div>
                </el-dialog>

                <el-dialog title="编辑商品" :visible.sync="editVisible">
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
                                <el-button size="small" type="primary">重新上传 (请选择一张图片, 上传覆盖)</el-button>
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
                                <el-button size="small" type="primary">重新上传 (请选择一张图片, 上传覆盖)</el-button>
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
                                <el-button size="small" type="primary">重新上传 (最多选择4张图片, 上传覆盖)</el-button>
                            </el-upload>
                        </el-form-item>

                        <el-form-item class="submit123">
                            <el-button type="primary" @click="submitForm('ruleForm')"
                                       style="float: right; margin-left: 10px">确 定
                            </el-button>
                            <el-button @click="cancelEdit" style="float: right">取 消</el-button>
                        </el-form-item>

                    </el-form>

                </el-dialog>

            </div>
        </m-shelf>

        <div class="w">
            <el-pagination
                style="float: right; margin-bottom: 30px;"
                @current-change="handleCurrentChange"
                :current-page.sync="page"
                layout="total, prev, pager, next"
                :total="total"
                :page-size="4">
            </el-pagination>
        </div>

    </div>
</template>

<script>
import MShelf from '@/components/shelf'
import {getStore} from "../utils/storage";
import {Notification} from "element-ui";

export default {
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
            ruleForm: {
                name: '',
                price: '',
                subTitle: '',
            },

            rules: {
                name: [{validator: validateName, trigger: 'blur'}],
                price: [{validator: validatePrice, trigger: 'blur'}],
                subTitle: [{validator: validateSubTitle, trigger: 'blur'}],
            },

            fileListImage: [],
            fileListDetail: [],
            fileListSmallImage: [],

            formLabelWidth: '120px',
            myGoodsList: [],
            imageVisible: false,
            detailVisible: false,
            smallImageVisible: false,
            editVisible: false,
            imageURL: '',
            detailURL: '',
            small: [],
            big: '',
            page: 1,
            size: 4,
            total: 0,
            curEditGoodsId: -1,
        }
    },

    methods: {
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
                    formData.append("id", this.curEditGoodsId)

                    const res = await this.$http.post("http://127.0.0.1:8000/api/MyGoodsEdit", formData, {
                        headers: {"Content-Type": "multipart/form-data"},
                        params: {
                            token: getStore('token')
                        }
                    })

                    if (res.data === 200) {
                        Notification({
                            title: '商品修改成功',
                            type: 'success',
                            duration: 3000,
                            offset: 100
                        })
                        this.fileListImage = []
                        this.fileListDetail = []
                        this.fileListSmallImage = []
                        this.editVisible = false
                        await this.getMyGoods()
                    } else {
                        Notification.error({
                            title: '修改商品失败',
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

        async editMyGoods(id) {
            this.curEditGoodsId = id
            let res = await this.$http.get('http://127.0.0.1:8000/api/goodsDetail', {
                params: {
                    productId: id
                }
            })
            let obj = res.data
            this.ruleForm.name = obj.name
            this.ruleForm.price = obj.price
            this.ruleForm.subTitle = obj.sub_title
            this.editVisible = true
        },

        cancelEdit() {
            this.editVisible = false
        },

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

        showImage(imageURL) {
            this.imageURL = imageURL
            this.imageVisible = true
        },
        showDetail(detailURL) {
            this.detailURL = detailURL
            this.detailVisible = true
        },
        showSmallImage(small_image) {
            this.small = small_image
            this.big = this.small[0]
            this.smallImageVisible = true
        },

        handleClick(src) {
            this.big = src
        },

        async getMyGoods() {
            let res = await this.$http.get('http://127.0.0.1:8000/api/MyGoodsList', {
                params: {
                    token: getStore('token'),
                    page: this.page,
                    size: this.size,
                }
            })
            this.myGoodsList = res.data.results
            this.total = res.data.count
        },

        handleCurrentChange(val) {
            this.page = val
            this.getMyGoods()
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
        this.getMyGoods()
    },
    components: {
        MShelf,
    },
}
</script>

<style lang="scss" scoped>
@import "../assets/style/mixin";

.submit123 {
    padding-left: 200px;
}

::v-deep .gray-box[data-v-3b1bf56c] {
    width: 1220px;
    margin: 40px auto 30px;
}

.gray-sub-title {
    height: 38px;
    padding: 0 24px;
    background: #EEE;
    border-top: 1px solid #DBDBDB;
    border-bottom: 1px solid #DBDBDB;
    line-height: 38px;
    font-size: 12px;
    color: #666;
    display: flex;

    span {
        display: inline-block;
        height: 100%;
    }

    .first {
        display: flex;
        justify-content: space-between;
        flex: 1;

        .f-bc {
            > span {
                width: 123px;
                text-align: center;
            }
        }
    }

    .last {
        width: 230px;
        text-align: center;
        display: flex;
        border-left: 1px solid #ccc;

        span {
            flex: 1;
        }
    }
}

.bt {
    border-top: 1px solid #EFEFEF;
}

.date {
    padding-left: 0;
}


.cart {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0 0 24px;

    &:hover {
        .del-order {
            display: block;
        }
    }

    .del-order {
        display: none;
    }

    .cart-l {
        display: flex;
        align-items: center;
        flex: 1;
        padding: 15px 0;
        justify-content: space-between;
        position: relative;

        &:before {
            position: absolute;
            content: ' ';
            right: -1px;
            top: 0;
            width: 1px;
            background-color: #EFEFEF;
            height: 100%;
        }

        .ellipsis {
            margin-left: 20px;
            width: 220px;
        }

        .img-box {
            border: 1px solid #EBEBEB;
        }

        img {
            display: block;
            @include wh(80px);
        }

        .cart-l-r {
            display: flex;
            margin-right: 24px;
            line-height: 40px;

            > div {
                text-align: center;
                width: 134px;
            }
        }

        .car-l-l {
            display: flex;
            align-items: center;
        }
    }

    .cart-r {
        width: 230px;
        display: flex;

        span {
            text-align: center;
            flex: 1;
        }
    }
}

.prod-operation {
    height: 110px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 254px;

    div {
        width: 100%;
        text-align: center;
    }

    div:last-child {
        padding-right: 24px;
    }
}


.gallery-wrapper {
    .gallery {
        display: flex;
        width: 540px;

        .thumbnail {
            li:first-child {
                margin-top: 0;
            }

            li {
                @include wh(80px);
                margin-top: 10px;
                padding: 12px;
                border: 1px solid #f0f0f0;
                border: 1px solid rgba(0, 0, 0, 0.06);
                border-radius: 5px;
                cursor: pointer;

                &.on {
                    padding: 10px;
                    border: 3px solid #ccc;
                    border: 3px solid rgba(0, 0, 0, 0.2);
                }

                img {
                    display: block;
                    @include wh(100%);
                }
            }
        }

        .thumb {
            .big {
                margin-left: 20px;
            }

            img {
                display: block;
                @include wh(440px);
            }
        }
    }
}
</style>

