import Vue from 'vue'
import Vuex from 'vuex'

import Spender from './modules/spender'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    token: null,
    username: null
  },
  mutations: {
    set (state, { type, item }) {
      state[type] = item
    }
  },
  actions: {
    set_token ({ commit }, token) {
      commit('set', { type: 'token', item: token })
    },
    set_username ({ commit }, username) {
      commit('set', { type: 'username', item: username })
    }
  },
  modules: {
    spender: Spender
  }
})

export default store
