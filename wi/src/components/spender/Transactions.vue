<template>
  <div class="d-flex">
    <nav class="nav-wrapper mr-3">
      <spender-nav></spender-nav>
      <div class="filters-wrapper py-2 mt-3" v-if="false">
      </div>
    </nav>
    <main class="main-wrapper">
      <div class="wrapper">
        <div class="container-fluid count-wrapper">
          <div class="row d-flex align-items-center">
            <div class="col d-flex">
              <div class="input-group">
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
                <input
                  ref="query"
                  type="text"
                  class="form-control"
                  placeholder="Поиск транзакций"
                  v-model="query">
              </div>
            </div>
          </div>
        </div>
        <div class="container-fluid period-wrapper d-flex justify-content-between">
          <div>
            <b>Период:</b> {{ humanize_period(params.timestamp_from, params.timestamp_to) }}
          </div>
          <div class="text-right">
            <span
              class="oi oi-loop-circular reload-button"
              title="Обновить"
              v-b-tooltip.hover
              v-on:click.prevent="load_transactions"></span>
            <b>{{ count }}</b> транзакций
          </div>
        </div>
        <div class="container-fluid aggs-wrapper">
          <transactions-aggs
            :aggs="aggs.income"
            title="Доходы"></transactions-aggs>
          <transactions-aggs
            :aggs="aggs.expense"
            title="Расходы"></transactions-aggs>
        </div>
        <div class="content">
          <div class="list-group list-group-flush">
            <div class="list-group-item"
              v-for="transaction in transactions"
              :key="transaction.id"
            >
              <div class="row">
                <div class="col-4">
                  <div>
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
                    <b>{{ formatPrice(transaction.amount) }}</b>
                    <small class="text-info">{{ transaction.currency }}</small>
                    <template v-if="transaction.default_currency !== null">
                      <small class="text-muted">
                        ≈
                        {{ formatPrice(transaction.default_currency.amount) }}
                        {{ transaction.default_currency.currency }}
                        </small>
                    </template>
                  </div>
                  <div>
                    <small class="text-muted">{{ transaction.timestamp | formatDateTime }}</small>
                  </div>
                </div>
                <div class="col-3">
                  <text-highlight :queries="query">
                    {{ transaction.record.text }}
                  </text-highlight>
                </div>
                <div class="col-5 d-flex justify-content-end">
                  <category-select
                    v-bind:transaction="transaction"></category-select>
                </div>
              </div>
            </div>
          </div>
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
      params: {}
    }
  },
  computed: {
    lower_query () {
      return this.query.toLowerCase()
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
    '$route' (to, from) {
      console.log(to)
    },
    current_period (newPeriod, oldPeriod) {
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
      axios.get(ApiUrl + `/spender/transactions?page=${this.currentPage}&q=${encodeURIComponent(this.query)}&period=${this.current_period}`, {
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
    }
  },
  components: {
    SpenderNav,
    CategorySelect,
    TextHighlight,
    vSelect,
    TransactionsAggs
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
