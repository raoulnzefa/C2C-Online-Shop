<template>
  <div>
    <m-shelf title="我的订单">
      <div slot="content">
        <div v-for="(item,i) in orderList" :key="i">
          <div class="gray-sub-title cart-title">
            <div class="first">
              <div>
                <span class="order-id"> 订单号：{{ item.id }}</span>
              </div>
              <div class="f-bc">
                <span class="price">单价</span>
                <span class="num">数量</span>
                <span class="operation">卖家</span>
              </div>
            </div>
          </div>

          <div class="pr">
            <div class="cart">
              <div class="cart-l" :class="{bt:1>0}">
                <div class="car-l-l">
                  <div class="img-box"><img :src="item.image" alt=""></div>
                  <div class="ellipsis">{{ item.goods.name }}</div>
                </div>
                <div class="cart-l-r">
                  <div>¥ {{ Number(item.goods.price).toFixed(2) }}</div>
                  <div class="num">{{ item.num }}</div>
                  <div class="type">
                    {{ item.seller }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>


        <div style="padding: 100px 0;text-align: center" v-if="orderList.length === 0">
          订单为空
        </div>

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

export default {
  name: "orderList",

  data() {
    return {
      orderList: [],
      page: 1,
      size: 4,
      total: 0,
    }
  },

  methods: {
    handleCurrentChange(val) {
      this.page = val
      this.getOrder()
    },

    async getOrder() {
      let res = await this.$http.get('http://127.0.0.1:8000/api/OrderList', {
        params: {
          token: getStore('token'),
          page: this.page,
          size: this.size,
        }
      })
      this.orderList = res.data.results
      this.total = res.data.count
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
    this.getOrder()
  },
  components: {
    MShelf,
  },
}
</script>

<style lang="scss" scoped>
@import "../assets/style/mixin";

::v-deep .gray-box[data-v-3b1bf56c] {
  width: 1220px;
  margin: 40px auto 80px;
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
        width: 112px;
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

      > div {
        text-align: center;
        width: 112px;
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
</style>
