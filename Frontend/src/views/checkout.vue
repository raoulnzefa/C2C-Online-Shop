<template>
  <div class="checkout">
    <div class="w" style="padding-top: 40px;">
      <!-- 收货地址 -->
      <m-shelf title="请选择收货地址">
        <div slot="content">
          <ul class="address-item-list clearfix">
            <li v-for="(item,i) in addList"
                :key="i"
                class="address pr"
                :class="{checked:addressId === item.id}"
                @click="chooseAddress(item.id, item.name, item.phone, item.address)">

               <span v-if="addressId === item.id" class="pa">
                 <svg viewBox="0 0 1473 1024" width="17.34375" height="12">
                 <path
                     d="M1388.020 57.589c-15.543-15.787-37.146-25.569-61.033-25.569s-45.491 9.782-61.023 25.558l-716.054 723.618-370.578-374.571c-15.551-15.769-37.151-25.537-61.033-25.537s-45.482 9.768-61.024 25.527c-15.661 15.865-25.327 37.661-25.327 61.715 0 24.053 9.667 45.849 25.327 61.715l431.659 436.343c15.523 15.814 37.124 25.615 61.014 25.615s45.491-9.802 61.001-25.602l777.069-785.403c15.624-15.868 25.271-37.66 25.271-61.705s-9.647-45.837-25.282-61.717M1388.020 57.589z"
                     fill="#6A8FE5" p-id="1025">
                   </path>
                 </svg>
               </span>

              <p>收货人: {{ item.name }}</p>
              <p>手机号码: {{ item.phone }}</p>
              <p class="street-name ellipsis">收货地址: {{ item.address }}</p>

              <div class="operation-section">
                <span class="update-btn" style="font-size:12px" @click="update(item)">修改</span>
                <span class="delete-btn" style="font-size:12px" :data-id="item.id" @click="delAddr(item.id)">删除</span>
              </div>

            </li>
            <li class="add-address-item" @click="dialogFormVisible = true">
              <img src="../../public/static/images/jia.svg" alt="">
              <p>添加新地址</p>
            </li>
          </ul>
        </div>
      </m-shelf>
      <!-- 购物清单 -->
      <m-shelf title="订单信息">
        <div slot="content">
          <div class="box-inner ui-cart">
            <div>
              <!--标题-->
              <div class="cart-table-title">
                <span class="subtotal">价格</span>
                <span class="num">数量</span>
                <span class="price">单价</span>
              </div>
              <!--列表-->
              <div class="cart-table" v-for="(item,i) in cartList" :key="i">
                <div class="cart-group divide pr" :data-productid="item.id">
                  <div class="cart-top-items">
                    <div class="cart-items clearfix">
                      <!--图片-->
                      <div class="items-thumb fl">
                        <img :alt="item.name"
                             :src="item.image">
                        <a @click="productDetail(item.id)" :title="item.name" target="_blank"></a>
                      </div>
                      <!--信息-->
                      <div class="name hide-row fl">
                        <div class="name-table">
                          <a @click="productDetail(item.id)" :title="item.name" target="_blank"
                             v-text="item.name"></a>
                        </div>
                      </div>
                      <!--商品数量-->
                      <div>
                        <!--总价格-->
                        <div class="subtotal" style="font-size: 14px">¥ {{ item.price * item.num }}</div>
                        <!--数量-->
                        <div class="item-cols-num">
                          <span v-text="item.num"></span>
                        </div>
                        <!--价格-->
                        <div class="price">¥ {{ item.price }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- 合计 -->
            <div class="cart-bottom-bg fix-bottom">
              <div class="fix-bottom-inner">
                <div class="shipping">
                  <div class="shipping-box" style="padding: 0 40px;">
                    <div class="shipping-total shipping-price"><h4
                        class="highlight">总价格：<em>￥{{ checkPrice }}</em>
                    </h4>
                    </div>
                  </div>
                  <my-button class="big-main-btn"
                             style="margin: 0;width: 130px;height: 50px;line-height: 50px;font-size: 16px"
                             :text="returnToCart" @click.native="returnCart">
                  </my-button>
                  <my-button class="big-main-btn"
                             style="margin: 0;width: 130px;height: 50px;line-height: 50px;font-size: 16px"
                             :text="submitOrder"
                             @click.native="SubmitOrder">
                  </my-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </m-shelf>

      <el-dialog title="添加收货地址" :visible.sync="dialogFormVisible" @close="resetForm('ruleForm')">
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm">

          <el-form-item label="姓名" :label-width="formLabelWidth" prop="name">
            <el-input v-model="ruleForm.name" autocomplete="off"></el-input>
          </el-form-item>

          <el-form-item label="手机号" :label-width="formLabelWidth" prop="phone">
            <el-input v-model="ruleForm.phone" autocomplete="off"></el-input>
          </el-form-item>

          <el-form-item label="地址" :label-width="formLabelWidth" prop="address">
            <el-input v-model="ruleForm.address" autocomplete="off"></el-input>
          </el-form-item>

          <el-form-item class="submit123">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="submitForm('ruleForm')">确 定</el-button>
          </el-form-item>

        </el-form>
      </el-dialog>


      <el-dialog title="修改收货地址" :visible.sync="editFormVisible">
        <el-form :model="editForm" :rules="rules" ref="editForm">

          <el-form-item label="姓名" :label-width="formLabelWidth" prop="name">
            <el-input v-model="editForm.name" autocomplete="off"></el-input>
          </el-form-item>

          <el-form-item label="手机号" :label-width="formLabelWidth" prop="phone">
            <el-input v-model="editForm.phone" autocomplete="off"></el-input>
          </el-form-item>

          <el-form-item label="地址" :label-width="formLabelWidth" prop="address">
            <el-input v-model="editForm.address" autocomplete="off"></el-input>
          </el-form-item>

          <el-form-item class="submit123">
            <el-button @click="editFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="submitEditForm('editForm')">确 定</el-button>
          </el-form-item>

        </el-form>
      </el-dialog>
    </div>
  </div>

</template>

<script>
import MShelf from '@/components/shelf.vue';
import MyButton from '@/components/MyButton'
import {mapMutations, mapState} from "vuex";
import {getStore} from "../utils/storage";
import {Notification} from 'element-ui'


export default {
  name: "checkout",
  components: {
    MShelf,
    MyButton,
  },
  data() {
    let validateName = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入姓名'))
      } else {
        callback()
      }
    }

    let validatePhone = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入手机号'))
      } else {
        callback()
      }
    }

    let validateAddress = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入地址'))
      } else {
        callback()
      }
    }

    return {
      // 提交订单
      addressId: '',
      name: '',
      phone: '',
      address: '',

      submitOrder: '提交订单',
      returnToCart: '返回购物车',
      dialogFormVisible: false,

      // 新建地址
      ruleForm: {
        name: '',
        phone: '',
        address: '',
      },
      formLabelWidth: '120px',

      rules: {
        name: [{validator: validateName, trigger: 'blur'}],
        phone: [{validator: validatePhone, trigger: 'blur'}],
        address: [{validator: validateAddress, trigger: 'blur'}],
      },

      editFormVisible: false,
      // 编辑地址
      editForm: {
        id: '',
        name: '',
        phone: '',
        address: '',
      },

    }
  },

  computed: {
    ...mapState(["cartList", "addList"]),

    checkPrice() {
      let totalPrice = 0;
      this.cartList && this.cartList.forEach(item => {
        totalPrice += (item.num * item.price)
      })
      return totalPrice
    },


  },

  methods: {
    ...mapMutations(["ADDRESSLIST", 'ADDRESSADD', 'ADDRESSEDIT']),

    productDetail(id) {
      this.$router.push({
        path: `goodsDetail?productId=${id}`
      })
    },

    returnCart() {
      this.$router.push({
        path: 'cartList'
      })
    },

    submitForm(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          let {name, phone, address} = this.ruleForm
          let res = await this.$http.post('http://127.0.0.1:8000/api/AddressAdd', {
            'token': getStore('token'),
            'name': name,
            'phone': phone,
            'address': address
          })
          this.dialogFormVisible = false
          let obj = res.data;
          this.ADDRESSADD({
            id: obj.id,
            name: obj.name,
            phone: obj.phone,
            address: obj.address
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },

    resetForm(formName) {
      this.$refs[formName].resetFields();
    },

    async addressList() {
      let res = await this.$http.get('http://127.0.0.1:8000/api/AddressList', {
        params: {
          token: getStore('token')
        }
      })
      this.ADDRESSLIST({
        obj_list: res.data
      })
    },

    update(item) {
      this.editForm.id = item.id
      this.editForm.name = item.name
      this.editForm.phone = item.phone
      this.editForm.address = item.address
      this.editFormVisible = true
    },

    submitEditForm(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          let {id, name, phone, address} = this.editForm
          let res = await this.$http.post('http://127.0.0.1:8000/api/AddressEdit', {
            'token': getStore('token'),
            'id': id,
            'name': name,
            'phone': phone,
            'address': address
          })
          this.editFormVisible = false
          this.ADDRESSEDIT({
            id: res.data.id,
            name: res.data.name,
            phone: res.data.phone,
            address: res.data.address,
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },

    async delAddr(id) {
      let res = await this.$http.post('http://127.0.0.1:8000/api/AddressDelete', {
        'token': getStore('token'),
        'id': id,
      })
      console.log(res.data)
      await this.addressList()
    },

    chooseAddress(id, name, phone, address) {
      this.addressId = id
      this.name = name
      this.phone = phone
      this.address = address
    },

    async SubmitOrder() {
      let res = await this.$http.post('http://127.0.0.1:8000/api/SubmitOrder', {
        token: getStore('token'),
        addrId: this.addressId,
        cartList: this.cartList
      })
      if (res.data === 200) {
        Notification({
          title: '购买成功',
          type: 'success',
          duration: 3000,
          offset: 100
        })
        await this.$router.push({
          path: 'orderList'
        })
      } else {
        Notification.error({
          title: '购买失败',
          duration: 3000,
          offset: 100
        })
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
    this.addressList()
  }
}
</script>

<style lang="scss" rel="stylesheet/scss" scoped>

.submit123 {
  padding-left: 520px;
  margin-bottom: 0;
}

// 收货地址
.address-item-list {
  padding: 30px 13px 0;

  .address {
    padding: 19px 14px 0 19px;

    p {
      line-height: 26px;
    }
  }

  li.checked {
    border-color: #6A8FE5;
    position: relative;
    background: #fff;

    .pa {
      right: 15px;
      top: 18px;
    }

    &:hover {
      background: #fff;
    }
  }

  li {
    position: relative;
    overflow: hidden;
    float: left;
    width: 276px;
    height: 158px;
    margin: 0 0 30px 16px;
    border: 1px solid #E5E5E5;
    border-radius: 3px;
    background: #FAFAFA;
    line-height: 14px;
    text-align: left;
    word-wrap: break-word;
    word-break: normal;
    color: #626262;
    cursor: pointer;
    //-moz-user-select: -moz-none;
    -webkit-user-select: none;
    -o-user-select: none;
    user-select: none;

    &:hover {
      background: #F2F2F2;

      .operation-section {
        visibility: visible;
        transform: translate(0, 0);
      }
    }

    &.add-address-item {
      text-align: center;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;

      p {
        margin-top: 5px;
      }
    }

    .operation-section {
      visibility: hidden;
      position: absolute;
      left: 0;
      bottom: 0;
      width: 100%;
      height: 28px;
      background: #E1E1E1;
      border-top: 1px solid #E1E1E1;
      transition: all .2s ease;
      transform: translate(0, 29px);
      border-top: 1px solid #E1E1E1;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 11;

      span {
        background: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 1;
        height: 100%;

        &:hover {
          background: #F2F2F2;
        }
      }

      span + span {
        border-left: 1px solid #E1E1E1;
      }

    }
  }
}

.s-content {
  .md {
    > div {
      text-align: left;
      margin-bottom: 15px;

      > input {
        width: 100%;
        height: 50px;
        font-size: 18px;
        padding: 10px 20px;
        border: 1px solid #ccc;
        border-radius: 6px;
        box-shadow: 0 3px 5px -4px rgba(0, 0, 0, .4) inset, -1px 0 3px -2px rgba(0, 0, 0, .1) inset;
        line-height: 46px;
      }
    }
  }

  .btn {
    margin: 0;
    width: 100%;
    height: 50px;
    font-size: 14px;
    line-height: 48px
  }
}

.ui-cart {
  img {
    width: 80px;
    height: 80px;
  }

  .cart-table-title {
    position: relative;
    z-index: 1;
    line-height: 38px;
    height: 38px;
    padding: 0 0 0 30px;
    font-size: 12px;
    background: #eee;
    border-bottom: 1px solid #dbdbdb;
    border-bottom-color: rgba(0, 0, 0, .08);

    .name {
      float: left;
      text-align: left;
    }

    span {
      width: 137px;
      float: right;
      text-align: center;
      color: #838383;
    }
  }

  .cart-group.divide {
    .cart-items {
      border-top: 1px dashed #eee;
    }
  }

  .cart-items {
    position: relative;
    height: 140px;
    margin-left: 74px;

    .subtotal {
      font-weight: 700;
    }

    .item-cols-num,
    .price,
    .subtotal {
      overflow: hidden;
      float: right;
      width: 137px;
      text-align: center;
      color: #666;
      line-height: 140px;
    }

    /*数量*/
    .subtotal,
    .item-cols-num {
      padding-top: 50px;
      line-height: 40px;
    }

    .select {
      width: 112px;
      height: 40px;
      padding-top: 4px;
      margin: 0 auto;
      line-height: 40px;

      .down {
        background-position: 0 -60px;
      }

      .down.down-disabled:hover {
        background-position: 0 -300px;
        cursor: not-allowed;
      }

      .num {
        position: relative;
        overflow: hidden;
        display: inline-block;
        width: 36px;
        height: 18px;
        margin: 7px 0 0;
        border: none;
        border-radius: 3px;
        line-height: 18px;
        text-align: center;
        font-size: 14px;
        transition: all .2s ease-out;
      }
    }

  }

  .down.down-disabled {
    background-position: 0 -300px;
    cursor: not-allowed;
  }
}

.cart-group.divide .cart-top-items:first-child .cart-items {
  border-top: none;
}

.items-choose {
  position: absolute;
  left: -74px;
  top: 0;
  width: 74px;
  height: 20px;
  padding: 60px 0 0 31px;
  font-size: 12px;
  color: #999;
}

.items-thumb {
  position: relative;
  margin-top: 30px;
  overflow: hidden;
  width: 80px;
  height: 80px;
}

.cart-items .items-thumb > a, .ui-cart .cart-items .items-thumb > i {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  border: 1px solid #fff;
  border-radius: 3px;
  border: 0 solid rgba(255, 255, 255, .1);
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, .06);
}

.name {
  width: 380px;
  margin-left: 20px;
  color: #323232;
  display: table;

  a {
    color: #333;
    font-size: 16px;
  }
}

.name-table {
  display: table-cell;
  vertical-align: middle;
  height: 140px;
}

.fix-bottom {
  padding: 22px 29px 19px 30px;
  height: 90px;
  width: 100%;
  z-index: 1;
  background-position: center;
  background: #fdfdfd;
  background: -webkit-linear-gradient(#fdfdfd, #f9f9f9);
  background: linear-gradient(#fdfdfd, #f9f9f9);
  border-top: 1px solid #e9e9e9;
  box-shadow: 0 -3px 8px rgba(0, 0, 0, .04);

  .cart-bottom-bg {
    height: 80px;
    border-top: 1px solid #D9D9D9;
    border-radius: 0 0 8px 8px;
  }

  .fix-bottom-inner {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }

  .shipping {
    display: flex;
    align-items: center;
  }

  em {
    display: inline-block;
    position: relative;
    top: 3px;
    margin-top: -4px;
    font-size: 24px;
    color: #d44d44;
    font-weight: 700;
  }
}

.attribute, .name p {
  color: #999;
  font-size: 12px;
  padding-top: 4px;
  line-height: 17px;
}


</style>

