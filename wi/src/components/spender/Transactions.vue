<template>
  <div class="d-flex">

    <!-- Левое навигационное меню -->
    <nav class="nav-wrapper mr-3">
      <spender-nav></spender-nav>
      <div class="filters-wrapper py-3 mt-3">
        <select-shared-users
          v-on:filterSharedUsers="filterSharedUsers($event)">
        </select-shared-users>
      </div>
    </nav>

    <main class="main-wrapper">
      <div class="wrapper">

        <!-- Поисковое поле + кнопка выбора периода + фильтр транзакций -->
        <div class="container-fluid count-wrapper">
          <div class="row d-flex align-items-center">
            <div class="col d-flex">
              <div class="input-group">

                <!-- Период -->
                <div class="input-group-prepend">
                  <b-dropdown
                    variant="light"
                    class="period-toggle"
                    :text="periods[current_period].title">
                    <b-dropdown-item
                      v-for="period in periods"
                      :key="period.id"
                      @click="current_period = period.name"
                      >
                      {{ period.title }}
                    </b-dropdown-item>
                  </b-dropdown>
                </div>

                <!-- Поле поиска -->
                <input
                  ref="query"
                  type="text"
                  class="form-control"
                  placeholder="Поиск транзакций"
                  v-model="query">

                <!-- Фильтр транзакций -->
                <div class="input-group-append">
                  <b-dropdown
                    variant="light"
                    class="period-toggle-right"
                    :text="category_filter_title">
                    <b-dropdown-item
                      v-for="fiCategory in filterCategories"
                      :key="fiCategory.id"
                      @click="filterCategory = fiCategory.name"
                      >
                      {{ fiCategory.title }}
                    </b-dropdown-item>
                  </b-dropdown>
                </div>

              </div>
            </div>
          </div>
        </div>

        <div class="container-fluid period-wrapper d-flex justify-content-between">

          <!-- Отображение периода -->
          <div>
            <b>Период:</b> {{ humanize_period(params.timestamp_from, params.timestamp_to) }}
          </div>

          <!-- Количество транзакций и кнопка "Обновить" -->
          <div class="text-right">
            <span
              class="oi oi-loop-circular reload-button"
              title="Обновить"
              v-b-tooltip.hover
              v-on:click.prevent="load_transactions"></span>
            <b>{{ count }}</b> транзакций
          </div>

        </div>

        <!-- Агрегации -->
        <div class="container-fluid aggs-wrapper">

          <!-- Агрегация доходов -->
          <transactions-aggs
            v-on:filterCategory="changeCategory($event)"
            :aggs="aggs.income"
            :filteredCategory="filterCategory"
            title="Доходы"></transactions-aggs>

          <!-- Агрегация расходов -->
          <transactions-aggs
            v-on:filterCategory="changeCategory($event)"
            :aggs="aggs.expense"
            :filteredCategory="filterCategory"
            title="Расходы"></transactions-aggs>

        </div>

        <div class="content">
          <div class="list-group list-group-flush">

            <!-- Транзакция -->
            <div class="list-group-item"
              v-for="transaction in transactions"
              :key="transaction.id">
              <div class="row">
                <div class="col-4">
                  <div>

                    <!-- Направление транзакции -->
                    <small class="direction-pointer">
                      <span
                        class="oi oi-account-login text-success"
                        v-if="transaction.direction === 0"
                        v-b-tooltip.hover
                        title="Доход"></span>
                      <span
                        class="oi oi-account-logout text-danger"
                        v-else
                        v-b-tooltip.hover
                        title="Расход"></span>
                    </small>

                    <!-- Сумма транзакции -->
                    <b>{{ formatPrice(transaction.amount) }}</b>

                    <!-- Валюта транзакции -->
                    <small class="text-info">{{ transaction.currency }}</small>

                    <!-- Аппроксимация в валюте по умолчанию -->
                    <template v-if="transaction.default_currency !== null">
                      <small class="text-muted">
                        ≈
                        {{ formatPrice(transaction.default_currency.amount) }}
                        {{ transaction.default_currency.currency }}
                        </small>
                    </template>

                  </div>

                  <!-- Время транзакции -->
                  <div>
                    <small class="text-muted">{{ transaction.timestamp | formatDateTime }}</small>
                  </div>

                  <!-- Бейджик имени пользователя.
                       Если не пользователь owner транзакции -->
                  <div v-if="transaction.owner.username !== username">
                    <span
                      v-b-tooltip.hover
                      class="badge badge-secondary"
                      :title="transaction.owner.first_name + ' ' + transaction.owner.last_name">
                      {{ transaction.owner.first_name }}
                    </span>
                  </div>

                </div>

                <!-- Текст транзакции -->
                <div class="col-3">
                  <text-highlight :queries="query">
                    {{ transaction.record.text }}
                  </text-highlight>
                </div>

                <!-- Выбор категории -->
                <div class="col-5 d-flex justify-content-end">
                  <category-select
                    v-bind:readonly="transaction.owner.username !== username"
                    v-bind:transaction="transaction"></category-select>
                </div>

              </div>
            </div>

          </div>

          <!-- Пагинация снизу страницы -->
          <div class="container-fluid pagination-wrapper">
            <b-pagination
              v-model="currentPage"
              :limit="5"
              :total-rows="count"
              :per-page="limit"
              v-if="count > limit"
            ></b-pagination>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

import { ApiUrl } from '@/config'
import SpenderNav from './SpenderNav'
import CategorySelect from './CategorySelect'
import TransactionsAggs from './TransactionsAggs'
import SelectSharedUsers from './SelectSharedUsers'
import TextHighlight from 'vue-text-highlight'
import vSelect from 'vue-select'
import moment from 'moment'

export default {
  name: 'Transactions',
  data () {
    return {
      transactions: [],
      count: 0,
      currentPage: 1,
      categories: [],
      query: '',
      aggs: {},
      limit: 10,
      current_period: 'month',
      predefined_periods: {
        'today': {id: 1, name: 'today', title: 'Сегодня'},
        'yesterday': {id: 2, name: 'yesterday', title: 'Вчера'},
        'week': {id: 3, name: 'week', title: 'За неделю'},
        'month': {id: 4, name: 'month', title: 'С начала месяца'},
        'year': {id: 5, name: 'year', title: 'С начала года'},
        'whole': {id: 6, name: 'whole', title: 'За все время'}
      },
      params: {},
      filterCategories: {
        '_with': {id: 1, name: '_with', title: 'С категорией'},
        '_null': {id: 2, name: '_null', title: 'Без категории'}
      },
      filterCategory: '_with',
      other_owners: []
    }
  },
  computed: {
    username () {
      return this.$store.state.username
    },
    lower_query () {
      return this.query.toLowerCase()
    },
    category_filter_title () {
      if (this.filterCategory !== '_null') {
        return this.filterCategories['_with'].title
      } else {
        return this.filterCategories['_null'].title
      }
    },
    other_owners_list () {
      return this.other_owners.join(',')
    },
    periods () {
      let months = [
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь'
      ]

      let now = moment()
      var result = this.predefined_periods

      result['month-one'] = {id: 7, name: 'month-one', title: months[now.month() - 1]}
      result['month-two'] = {id: 8, name: 'month-two', title: months[now.month() - 2]}

      return result
    }
  },
  watch: {
    currentPage (newPage, oldPage) {
      this.load_transactions()
    },
    query (newQuery, oldQuery) {
      this.currentPage = 1
      this.load_transactions()
    },
    other_owners (newOwners, oldOwners) {
      this.currentPage = 1
      this.load_transactions()
    },
    '$route' (to, from) {
      console.log(to)
    },
    current_period (newPeriod, oldPeriod) {
      this.currentPage = 1
      this.load_transactions()
    },
    filterCategory (newFilterCategory, oldFilterCategory) {
      this.currentPage = 1
      this.load_transactions()
    }
  },
  mounted () {
    this.load_transactions()
    if (this.$store.state.spender.categories_loaded === false) {
      this.$store.dispatch('load_categories')
    }
    this.$refs.query.focus()
  },
  methods: {
    load_transactions () {
      axios.get(ApiUrl + `/spender/transactions?page=${this.currentPage}` +
        `&q=${encodeURIComponent(this.query)}&period=${this.current_period}` +
        `&category=${this.filterCategory}&other_owners=${this.other_owners_list}`, {
        headers: { Authorization: `Token ${this.$store.state.token}` }
      })
        .then(response => {
          // Должны отображаться результаты запроса, который введен сейчас
          if (response.data.params.q === this.query) {
            this.transactions = response.data.results
            this.count = response.data.count
            this.aggs = response.data.aggs
            this.params = response.data.params
          }
        })
        .catch(e => {
          console.log(e)
        })
    },
    formatPrice (value) {
      let val = (value / 1).toFixed(2).replace('.', ',')
      return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')
    },
    humanize_period (from, to) {
      if (!(from && to)) {
        return ''
      }

      let months = [
        'января',
        'февраля',
        'марта',
        'апреля',
        'мая',
        'июня',
        'июля',
        'августа',
        'сентября',
        'октября',
        'ноября',
        'декабря'
      ]

      let dtA = moment(String(from))
      let dtB = moment(String(to))

      if (this.date_string(from) === this.date_string(to)) {
        // one day
        return `${dtA.date()} ${months[dtA.month()]}`
      } else {
        // period
        var fromString = `с ${dtA.date()} ${months[dtA.month()]}`
        var toString = `по ${dtB.date()} ${months[dtB.month()]}`
        if (dtA.year() !== dtB.year()) {
          fromString += ` ${dtA.year()}`
          toString += ` ${dtB.year()}`
        }
        return fromString + ' ' + toString
      }
    },
    date_string (value) {
      if (value) {
        return moment(String(value)).format('DD.MM.YYYY')
      }
    },
    changeCategory (category) {
      if (category === null) {
        this.filterCategory = '_with'
      } else {
        this.filterCategory = category.id
      }
    },
    filterSharedUsers (filteredUsers) {
      this.other_owners = filteredUsers.map(({id}) => id)
    }
  },
  components: {
    SpenderNav,
    CategorySelect,
    TextHighlight,
    vSelect,
    TransactionsAggs,
    SelectSharedUsers
  }
}
</script>

<style scoped>
.nav-wrapper {
  width: 250px;
}
.main-wrapper {
  width: 800px;
}
.wrapper {
  box-shadow: 0 1px 0 0 #d7d8db, 0 0 0 1px #e3e4e8;
  background-color: #fff;
  border-radius: 2px;
}
.count-wrapper {
  background-color: #fafbfc;
  border-bottom: 1px solid #e7e8ec;
  padding-top: 10px;
  padding-bottom: 10px;
}
.pagination-wrapper {
  padding-top: 20px;
  padding-bottom: 20px;
  background-color: #fafbfc;
}
.pagination-wrapper ul {
  margin: 0;
}
.reload-button {
  font-size: .9em;
  cursor: pointer;
  color: #007bff;
}
.reload-button:hover {
  color: #006bdd;
}
.reload-button:active {
  color: #000;
}
.direction-pointer {
  padding-right: 5px;
}
.filters-wrapper {
  box-shadow: 0 1px 0 0 #d7d8db, 0 0 0 1px #e3e4e8;
  background-color: #fff;
  border-radius: 2px;
}
.period-toggle {
  border: 1px solid #ced4da;
  border-radius: 0.25rem 0 0 0.25rem;
}
.period-toggle-right {
  border: 1px solid #ced4da;
  border-radius: 0 0.25rem 0.25rem 0;
}
.period-wrapper {
  background-color: #fafbfc;
  border-bottom: 1px solid #e7e8ec;
  padding-top: 5px;
  padding-bottom: 5px;
}
.aggs-wrapper {
  background-color: #fafbfc;
  border-bottom: 1px solid #e7e8ec;
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>
