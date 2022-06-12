<template>
  <el-row class="good-item">
    <el-col>
      <el-card :body-style="{padding: 0}">
        <div class="good-img">
          <a>
            <img :src="goods.image" alt>
          </a>
        </div>
        <h6 class="good-title">{{ goods.name }}</h6>
        <h3 class="sub-title ellipsis">{{ goods.sub_title }}</h3>
        <div class="good-price pr">
          <div class="ds pa">
            <a href>
              <el-button type="default" size="medium" @click="productDetail(goods.id)">查看详情</el-button>
            </a>
            <el-button type="primary" size="medium" @click="addCart(goods.id)">加入购物车</el-button>
          </div>
          <p>
            <span style="font-size:14px">¥</span>
            {{ Number(goods.price).toFixed(2) }}
          </p>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import {mapMutations, mapState} from "vuex";
import {getStore} from "@/utils/storage";

export default {
  name: "MallGoods",
  props: ['goods'],

  data() {
    return {}
  },

  methods: {
    ...mapMutations(["ADDCART"]),

    productDetail(id) {
      this.$router.push({
        path: `goodsDetail?productId=${id}`
      })
    },

    async addCart(id) {
      const token = getStore('token')
      if (token) {
        let res = await this.$http.post("http://127.0.0.1:8000/api/CartAdd", {
          good_id: id,
          token: token,
          product_num: 1,
        })
        let obj = res.data;

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

  }
}
</script>

<style lang="scss" scoped>
.good-img {
  display: flex;
  justify-content: center;

  a {
    display: block;

    img {
      margin: 50px auto 10px;
      width: 206px;
      height: 206px;
      display: block;
    }
  }
}

.good-price {
  margin: 15px 0;
  height: 30px;
  text-align: center;
  line-height: 30px;
  color: #d44d44;
  font-family: Arial;
  font-size: 18px;
  font-weight: 700;
  display: flex;
  justify-content: space-around;
  padding-bottom: 60px;

  a {
    margin-right: 5px;
  }

  .ds {
    display: none;
  }
}

.good-price:hover .ds {
  display: block;
}

.good-title {
  line-height: 1.2;
  font-size: 16px;
  color: #424242;
  margin: 0 auto;
  padding: 0 14px;
  text-align: center;
  overflow: hidden;
}

h3 {
  text-align: center;
  line-height: 1.2;
  font-size: 12px;
  color: #d0d0d0;
  padding: 10px;
}

.good-item {
  background: #fff;
  width: 25%;
  transition: all 0.5s;
  height: 410px;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 1px 1px 20px #999;

    .good-price p {
      display: none;
    }

    .ds {
      display: flex;
    }
  }
}

.el-card {
  border: none;
}
</style>
