import axios from 'axios'
import { ApiUrl } from '@/config'

const Spender = {
  state: {
    categories: [],
    categories_loaded: false
  },
  mutations: {
    update_categories (state, categoriesList) {
      state.categories = categoriesList
      state.categories_loaded = true
    },
    add_category (state, category) {
      state.categories.push(category)
    },
    delete_category (state, categoryId) {
      for (let i = 0; i < state.categories.length; ++i) {
        if (state.categories[i].id === categoryId) {
          state.categories.splice(i, 1)
          break
        }
      }
    },
    increment_references (state, categoryId) {
      for (let i = 0; i < state.categories.length; ++i) {
        if (state.categories[i].id === categoryId) {
          state.categories[i].references++
          break
        }
      }
    }
  },
  actions: {
    load_categories (context) {
      axios.get(ApiUrl + '/spender/categories?limit=1000', {
        headers: { Authorization: `Token ${context.rootState.token}` }
      })
        .then(response => {
          context.commit('update_categories', response.data.results)
        })
        .catch(e => {
          //
        })
    }
  },
  getters: {
    filter_categories: state => (query, direction) => {
      if (query) {
        query = query.toLowerCase()
        return state.categories
          .filter(category => (category.name.toLowerCase().includes(query) ||
            category.description.toLowerCase().includes(query)) &&
            category.direction === direction)
      } else {
        return state.categories.filter(category => category.direction === direction)
      }
    },
    count_categories: (state, getters) => (direction) => {
      return getters.filter_categories(null, direction).length
    },
    categories_names (state) {
      return state.categories.map(category => category.name)
    }
  }
}

export default Spender
