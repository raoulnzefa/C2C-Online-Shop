import Vue from 'vue'
import Vuex from 'vuex'
import ca from "element-ui/src/locale/lang/ca";
import {setStore} from "../utils/storage";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        cartList: [],
        addList: [],
        showCart: false,
    },
    mutations: {
        SHOWCART(state, {showCart}) {
            state.showCart = showCart
        },
        ADDCART(state, {id, price, name, image, num}) {
            let cart = state.cartList
            let goods = {id, price, name, image, num}
            let flag = true

            if (cart.length) {
                cart.forEach(item => {
                    if (item.id === id && item.num >= 0) {
                        flag = false
                        item.num = num
                    }
                })
            }

            if (!cart.length || flag) {
                goods.id = id
                goods.price = price
                goods.name = name
                goods.image = image
                goods.num = num
                cart.push(goods)
            }
            state.cartList = cart
        },

        CARTLIST(state, {obj_list}) {
            state.cartList = obj_list
        },

        ADDRESSLIST(state, {obj_list}) {
            state.addList = obj_list
        },

        ADDRESSADD(state, {id, name, phone, address}) {
            let addr_list = state.addList
            let add = {id, name, phone, address}
            add.id = id
            add.name = name
            add.phone = phone
            add.address = address
            addr_list.push(add)
            state.addList = addr_list

        },

        ADDRESSEDIT(state, {id, name, phone, address}) {
            let addr_list = state.addList
            addr_list.forEach(item => {
                if (item.id === id) {
                    item.name = name
                    item.phone = phone
                    item.address = address
                }
            })
            state.addList = addr_list

        },
    },
    actions: {},
    modules: {}
})
