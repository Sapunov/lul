// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'open-iconic/font/css/open-iconic-bootstrap.css'
import moment from 'moment'
import VueLocalStorage from 'vue-localstorage'
import store from './store'

Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(VueLocalStorage)

Vue.filter('formatDateTime', function (value) {
  if (value) {
    return moment(String(value)).format('DD.MM.YYYY hh:mm')
  }
})

Vue.filter('formatDate', function (value) {
  if (value) {
    return moment(String(value)).format('DD.MM.YYYY')
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
