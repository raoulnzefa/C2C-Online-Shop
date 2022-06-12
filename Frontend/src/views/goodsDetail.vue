<template>
  <div class="w store-content">
    <div class="gray-box">

      <div class="gallery-wrapper">
        <div class="gallery">
          <div class="thumbnail">
            <ul>
              <li v-for="(item, i) in small" :key="i" :class="{on:item===big}" @click="handleClick(item)">
                <img :src='item'>
              </li>
            </ul>
          </div>
          <div class="thumb">
            <div class="big">
              <img :src='big'>
            </div>
          </div>
        </div>
      </div>
      <!--右边-->
      <div class="banner">
        <div class="sku-custom-title">
          <h4>{{ product.name }}</h4>
          <h3>{{ product.sub_title }}</h3>
          <h6>
            <span>Seller: {{ product.seller }}</span>
            <span class="price">
              <em>¥</em>
              <i>{{ Number(product.price).toFixed(2) * product_num }}</i>
            </span>
          </h6>
        </div>
        <div class="num">
          <span class="params-name">数量</span>
          <BuyNum @handleValue="productNum"></BuyNum>
        </div>
        <div class="buy">
          <el-button @click="addCart(product.id)" type="primary">加入购物车</el-button>
          <el-button type="danger">购买</el-button>
        </div>
      </div>
    </div>
    <!--产品信息-->
    <div class="item-info">
      <Shelf title="商品详情">
        <div slot="content">
          <div id="detail-img">
            <img :src="product.detail">
          </div>
        </div>
      </Shelf>
    </div>
  </div>
</template>

<script>
import BuyNum from '@/components/BuyNum.vue';
import Shelf from '@/components/shelf.vue';
import {getStore} from "../utils/storage";
import {mapMutations} from "vuex";

export default {
  name: "goodsDetail",
  components: {
    BuyNum,
    Shelf
  },
  data() {
    return {
      product: {},
      small: [],
      big: '',
      product_num: 1
    }
  },

  methods: {
    async getGoodsDetail() {
      try {
        const res = await this.$http.get("http://127.0.0.1:8000/api/goodsDetail", {
          params: {
            productId: this.$route.query.productId
          }
        })
        this.product = res.data
        this.small = this.product['small_image']
        this.big = this.small[0]
      } catch (e) {
        console.log(e)
      }
    },

    handleClick(src) {
      this.big = src
    },

    productNum(num) {
      this.product_num = num
    },

    ...mapMutations(["ADDCART"]),

    async addCart(id) {
      const token = getStore('token')
      if (token) {
        let res = await this.$http.post("http://127.0.0.1:8000/api/CartAdd", {
          good_id: id,
          token: token,
          product_num: this.product_num,
        })
        let obj = res.data;
        console.log(obj)

        this.ADDCART({
          id: id,
          price: obj.price,
          name: obj.name,
          image: obj.image,
          num: obj.num,
        })

      } else {
        await this.$router.push({
          name: 'login'
        })
      }
    },
  },

  created() {
    this.getGoodsDetail()
    this.handleClick()
  }
}
</script>

<style lang="scss" scoped>
@import "../assets/style/mixin";

::v-deep #detail-img {
  text-align: center;
}

.store-content {
  clear: both;
  width: 1220px;
  min-height: 600px;
  padding: 0 0 25px;
  margin: 0 auto;
}

.gray-box {
  display: flex;
  padding: 60px;
  margin: 20px 0;

  .gallery-wrapper {
    .gallery {
      display: flex;
      width: 540px;

      .thumbnail {
        li:first-child {
          margin-top: 0px;
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

  // 右边
  .banner {
    width: 450px;
    margin-left: 10px;

    h4 {
      font-size: 24px;
      line-height: 1.25;
      color: #000;
      margin-bottom: 13px;
    }

    h6 {
      font-size: 14px;
      line-height: 1.5;
      color: #bdbdbd;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .sku-custom-title {
      overflow: hidden;
      padding: 8px 8px 18px 10px;
      position: relative;
    }

    .params-name {
      padding-right: 20px;
      font-size: 14px;
      color: #8d8d8d;
      line-height: 36px;
    }

    .num {
      padding: 29px 0 8px 10px;
      border-top: 1px solid #ebebeb;
      display: flex;
      align-items: center;
    }

    .buy {
      position: relative;
      border-top: 1px solid #ebebeb;
      padding: 30px 0 0 10px;
    }
  }
}

.item-info {
  .gray-box {
    padding: 0;
    display: block;
  }

  .img-item {
    width: 1220px;
    // padding: 1vw;
    text-align: center;

    img {
      width: 100%;
      height: auto;
      display: block;
    }
  }
}

.no-info {
  padding: 200px 0;
  text-align: center;
  font-size: 30px;
}

.price {
  display: block;
  color: #d44d44;
  font-weight: 700;
  font-size: 16px;
  line-height: 20px;
  text-align: right;

  i {
    padding-left: 2px;
    font-size: 24px;
  }
}
</style>
