import Vue from 'vue'
import Router from 'vue-router'
import Records from '@/components/Records'
import LoginForm from '@/components/LoginForm'
import Transactions from '@/components/spender/Transactions'
import Categories from '@/components/spender/Categories'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/spender/transactions'
    },
    {
      path: '/records',
      name: 'Records',
      component: Records
    },
    {
      path: '/login',
      name: 'LoginForm',
      component: LoginForm
    },
    {
      path: '/spender/transactions',
      name: 'Transactions',
      component: Transactions
    },
    {
      path: '/spender/categories',
      name: 'Categories',
      component: Categories
    }
  ]
})
