<template>
  <div class="align-self-start confirm-group">
    <b-dropdown
      :disabled="is_readonly"
      :no-caret="is_readonly"
      :text="visible_name(transaction.category)"
      variant="light"
      right
      @shown="$refs.query.focus()"
      @hidden="query = ''"
      v-bind:title="transaction.category === null ? '' : transaction.category.name"
    >

      <!-- Поисковое поле -->
      <div class="search-category">
        <div class="form-group">
          <input
            type="text"
            ref="query"
            class="form-control"
            placeholder="Поиск категории"
            v-model="query"
            @keyup.enter="try_set_category(transaction)">
        </div>
      </div>

      <!-- Категория -->
      <b-dropdown-item
        v-for="category in $store.getters.filter_categories(query, transaction.direction).slice(0, limit)"
        :key="category.id"
        v-if="category.direction === transaction.direction"
        @click="set_category(transaction, category)">
          <text-highlight :queries="query">{{ category.name }}</text-highlight>
          <br>

          <!-- Описание категории, появляющееся при поиске -->
          <small
            v-if="category.description !== '' && query && category.description.toLowerCase().includes(query.toLowerCase())"
            class="text-muted">
            <text-highlight :queries="query">{{ category.description }}</text-highlight>
          </small>

      </b-dropdown-item>

      <!-- Кнопка "Показать все" -->
      <template v-if="$store.getters.count_categories(transaction.direction) > 10 && limit !== max_limit && query == ''">
        <div class="dropdown-divider"></div>
        <div class="dropdown-item cursor" @click="limit = max_limit">
          <span class="text-info">Показать все...</span>
        </div>
      </template>

      <div class="dropdown-divider"></div>

      <!-- Кнопка создания новой категории -->
      <b-dropdown-item
        @click="$refs.CreateCategoryModal.show()">
        Создать новую категорию</b-dropdown-item>

    </b-dropdown>

    <!-- Кнопка подтверждения выбранной категории -->
    <span
      class="oi oi-check ckeck-button"
      @click="confirm_category(transaction)"
      :class="{
        'text-success': transaction.category_confirmed,
        'grey-color': !transaction.category_confirmed,
        'cursor': !is_readonly
      }"
      ></span>

    <!-- Компонент для создания новой категории -->
    <create-category ref="CreateCategoryModal" :direction="transaction.direction_human"></create-category>

  </div>
</template>

<script>
import axios from 'axios'

import { ApiUrl } from '@/config'
import CreateCategory from './CreateCategory'
import TextHighlight from 'vue-text-highlight'

export default {
  name: 'CategorySelect',
  data () {
    return {
      query: '',
      max_limit: 1000,
      limit: 10
    }
  },
  props: ['transaction', 'readonly'],
  computed: {
    is_readonly () {
      return this.readonly !== undefined ? this.readonly : false
    }
  },
  methods: {
    visible_name (category) {
      if (category !== null) {
        if (category.name.length <= 15) {
          return category.name
        } else {
          return category.name.slice(0, 15) + '..'
        }
      }
      return null
    },
    set_category (transaction, category) {
      axios.post(ApiUrl + `/spender/transactions/${transaction.id}/category/${category.id}`, {}, {
        headers: { Authorization: `Token ${this.$store.state.token}` }
      })
        .then(response => {
          transaction.category = category
          transaction.category_confirmed = true
          this.$store.commit('increment_references', category.id)
        })
        .catch(e => {

        })
    },
    try_set_category (transaction) {
      let result = this.$store.getters.filter_categories(this.query, transaction.direction)
      if (result.length === 1) {
        this.set_category(transaction, result[0])
      }
    },
    confirm_category (transaction) {
      if (this.is_readonly) {
        return
      }
      if (transaction.category !== null && transaction.category_confirmed === false) {
        axios.post(ApiUrl + `/spender/transactions/${transaction.id}/category/confirm`, {}, {
          headers: { Authorization: `Token ${this.$store.state.token}` }
        })
          .then(response => {
            transaction.category_confirmed = true
          })
          .catch(e => {

          })
        transaction.category_confirmed = true
      }
    }
  },
  components: {
    CreateCategory,
    TextHighlight
  }
}
</script>

<style scoped>
.ckeck-button {
  padding-left: 10px;
}
.cursor {
  cursor: pointer;
}
.ckeck-button:hover {
  color: #ddd;
}
.grey-color {
  color: #eee;
}
.search-category {
  padding-left: 10px;
  padding-right: 10px;
}
.cursor {
  cursor: pointer;
}
</style>
