<template>
  <div class="shopping-cart">
    <div class="store-content page-cart">
      <div class="gray-box">
        <div class="title"><h2>购物车</h2></div>
        <!--内容-->
        <div v-if="cartList.length">
          <div class="ui-cart">
            <div>
              <!--标题-->
              <div class="cart-table-title">
                <span class="operation">删除</span>
                <span class="subtotal">价格</span>
                <span class="num">数量</span>
                <span class="price1">单价</span>
              </div>
              <!--列表-->
              <div class="cart-table" v-for="(item,i) in cartList" :key="i">
                <div class="cart-group divide pr" :data-productid="item.id">
                  <div class="cart-top-items">
                    <div class="cart-items clearfix">
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
                      <!--删除按钮-->
                      <div class="operation">
                        <a class="items-delete-btn" @click="CartDelete(item.id)"></a>
                      </div>
                      <!--商品数量-->
                      <div>
                        <!--总价格-->
                        <div class="subtotal" style="font-size: 14px">¥ {{ item.price * item.num }}</div>
                        <!--数量选择-->
                        <div class="item-cols-num clearfix"
                             style="height: 140px; display: flex; align-items: center; justify-content: center;">
                          <el-input-number v-model="item.num" @change="((val)=>{handleChange(val, item.id)})" :min="1"
                                           :max="10" label="描述文字"></el-input-number>
                        </div>
                        <!--价格-->
                        <div class="price1">¥ {{ item.price }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="cart-bottom-bg fix-bottom">
            <div class="fix-bottom-inner">
              <div class="shipping">
                <div class="shipping-box">
                  <div class="shipping-total shipping-num">
                  </div>
                  <div class="shipping-total shipping-price">
                    <h4 class="highlight">总价格：<span>￥</span><i v-text="checkPrice"></i></h4>
                  </div>
                </div>
                <my-button class="big-main-btn"
                           style="margin: 0;width: 130px;height: 50px;line-height: 50px;font-size: 16px"
                           :text="checkoutNow"
                           @click.native="checkout"></my-button>
              </div>
            </div>
          </div>
        </div>

        <div v-else style="padding:50px">
          <p style="text-align: center;padding: 20px;color: #8d8d8d">购物车为空</p>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import MHeader from '@/common/MHeader.vue';
import MyButton from '@/components/MyButton'
import {mapMutations, mapState} from "vuex";
import {getStore} from "../utils/storage";

export default {
  name: "CartList",
  data() {
    return {
      checkoutNow: '购买',
    }
  },
  components: {
    MHeader,
    MyButton,
  },

  computed: {
    ...mapState(["cartList"]),

    checkPrice() {
      var totalPrice = 0
      this.cartList && this.cartList.forEach(item => {
        totalPrice += (item.num * item.price)
      })
      return totalPrice
    },
  },

  methods: {

    productDetail(id) {
      this.$router.push({
        path: `goodsDetail?productId=${id}`
      })
    },

    async handleChange(value, goods_id) {
      let res = await this.$http.post("http://127.0.0.1:8000/api/CartEdit", {
        goods_id: goods_id,
        token: getStore('token'),
        product_num: value,
      })
    },

    ...mapMutations(["CARTLIST"]),
    async CartList() {
      const res = await this.$http.get("http://127.0.0.1:8000/api/CartList", {
        params: {
          token: getStore("token")
        }
      });
      this.CARTLIST({
        obj_list: res.data
      })
    },

    async CartDelete(id) {
      const res = await this.$http.post("http://127.0.0.1:8000/api/CartDelete", {
        token: getStore("token"),
        id: id
      });
      console.log(res.data)
      await this.CartList()
    },

    checkout() {
      this.$router.push({
        path: 'checkout'
      })
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
  },

  mounted() {

  }
}
</script>

<style lang="scss" rel="stylesheet/scss" scoped>

.item-cols-num {
  display: inline-block;
}

.store-content {
  clear: both;
  width: 1220px;
  min-height: 600px;
  padding: 0 0 25px;
  margin: 0 auto;

  .gray-box {
    position: relative;
    margin-bottom: 30px;
    overflow: hidden;
    background: #fff;
    border-radius: 8px;
    border: 1px solid #dcdcdc;
    border-color: rgba(0, 0, 0, .14);
    box-shadow: 0 3px 8px -6px rgba(0, 0, 0, .1);

    .title {
      padding-left: 30px;
      position: relative;
      z-index: 10;
      height: 60px;
      padding: 0 10px 0 24px;
      border-bottom: 1px solid #d4d4d4;
      border-radius: 8px 8px 0 0;
      box-shadow: rgba(0, 0, 0, .06) 0 1px 7px;
      background: #f3f3f3;
      background: -webkit-linear-gradient(#fbfbfb, #ececec);
      background: linear-gradient(#fbfbfb, #ececec);
      line-height: 60px;
      font-size: 18px;
      color: #333;
    }
  }

  .ui-cart {
    padding-bottom: 91px;

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
      /*删除*/
      .operation {
        padding: 58px 0 0;
        font-size: 12px;
        line-height: 24px;

        .items-delete-btn {
          background-image: url(../../public/static/images/delete-btn-icon_a35bf2437e@2x.jpg);

          &:hover {
            background-position: 0 -36px;
          }
        }

        .items-delete-btn {
          display: block;
          width: 24px;
          height: 24px;
          margin: 0 auto;
          color: #C2C2C2;
          background: url(../../public/static/images/delete-btn-icon_a35bf2437e@2x.jpg);
          -webkit-background-size: 100% auto;
          background-size: 100% auto;
          -moz-transition: none;
          -webkit-transition: none;
          -o-transition: none;
          transition: none;
        }
      }

      .subtotal {
        font-weight: 700;
      }

      .item-cols-num,
      .operation,
      .price1,
      .subtotal {
        overflow: hidden;
        float: right;
        width: 137px;
        text-align: center;
        color: #666;
        line-height: 140px;
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

    img {
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

    .attribute, .name p {
      color: #999;
      font-size: 12px;
      padding-top: 4px;
      line-height: 17px;
    }

  }

}

.page-cart {
  padding-top: 40px;

  .fix-bottom {
    height: 90px;
    width: 100%;
    position: absolute;
    bottom: 0;
    z-index: 1;
    background-position: center;
    background: #fdfdfd;
    background: -webkit-linear-gradient(#fdfdfd, #f9f9f9);
    background: linear-gradient(#fdfdfd, #f9f9f9);
    border-top: 1px solid #e9e9e9;
    box-shadow: 0 -3px 8px rgba(0, 0, 0, .04);

    .cart-bottom-bg {
      height: 80px;
      /*background: url(../img/store/library/cart-wrapper-bg_4c8003c76e.jpg) repeat-x;*/
      border-top: 1px solid #D9D9D9;
      border-radius: 0 0 8px 8px;
    }
  }

  .cart-bar-operation {
    float: left;
    padding: 35px 26px;
    font-size: 12px;
  }

  .blue-checkbox-new {
    float: left;
    margin-right: 9px;
  }

  .choose-all, .delete-choose-goods, .selected-count {
    float: left;
    height: 20px;
    line-height: 20px;
    cursor: pointer;
    position: relative;
  }

  .blue-checkbox-new, .blue-checkbox-new.checkbox-disable, .blue-checkbox-new.checkbox-on {
    display: inline-block;
    position: relative;
    width: 20px;
    height: 20px;
    background: url(../../public/static/images/checkbox-new_631a56a4f6.png) no-repeat 0 -20px;
    cursor: pointer;
    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    user-select: none;
    vertical-align: middle;
  }

  .blue-checkbox-new.checkbox-on, .choose-checkbox-on .blue-checkbox-new {
    background: url(../../public/static/images/checkbox-new_631a56a4f6.png) no-repeat 0 0;
  }

  .delete-choose-goods {
    position: relative;
    margin-left: 21px;
    color: #bbb;
  }

  .shipping {
    float: right;
    padding: 20px 30px;
  }

  .shipping-box {
    display: inline-block;
    padding-top: 1px;
    margin-right: 10px;
  }

  .shipping-total {
    display: inline-block;
    border-left: 1px solid #e1e1e1;
    padding: 12px 20px;

    .shipping-price {
      width: 155px;
      padding-right: 0;
    }

    &.shipping-num i {
      width: 28px;
      display: inline-block;
      text-align: center;
    }

    h4 {
      color: #323232;

      > i {
        font-size: 18px;
        font-weight: 700;
      }

      i, span {
        color: #d44d44;
      }

    }

    h5 {
      color: #959595;

      > i {
        font-size: 16px;
        font-weight: 700;
      }
    }

  }

  .shipping-total.shipping-num {
    text-align: right;
  }

  .shipping-total:first-child {
    border: none;
  }

  .big-main-btn {
    float: right;
    height: 48px;
  }
}


</style>

