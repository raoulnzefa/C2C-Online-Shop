import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '../views/Index'
import Login from '../views/Login/Index'
import Home from '../views/Home'
import Goods from '../views/Goods'
import Sale from '../views/Sale'
import goodsDetail from '../views/goodsDetail'
import orderList from '../views/orderList'
import cartList from '../views/CartList'
import myGoodsList from '../views/myGoodsList'
import mySale from '../views/mySale'
import checkout from '../views/checkout'
import register from '../views/register'


Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: '/home',
        name: 'home',
        component: Index,
        children: [
            {
                path: 'home',
                component: Home,
            },
            {
                path: 'goods',
                component: Goods,
            },
            {
                path: 'goodsDetail',
                name: 'goodsDetail',
                component: goodsDetail,
            },
            {
                path: '/cartList',
                name: 'cartList',
                component: cartList,
            },
            {
                path: '/orderList',
                name: 'orderList',
                component: orderList,
            },
            {
                path: '/myGoodsList',
                component: myGoodsList,
            },
            {
                path: '/mySale',
                component: mySale,
            },
            {
                path: '/checkout',
                name: 'checkout',
                component: checkout,
            },

        ]
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/register',
        name: 'register',
        component: register,
    },

    {
        path: '/sale',
        component: Sale,
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
