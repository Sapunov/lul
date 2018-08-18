<template>
  <div class="records-wrapper">
    <div>
      <p>
        <b>Количество записей: </b>
        <span>{{ count }}</span>
        <span class="text-info">(<a href="#" v-on:click.prevent="load_records">обновить</a>)</span>
      </p>
    </div>
    <b-table
      bordered
      hover
      striped
      :items="records"
      :fields="fields">
      <template slot="label" slot-scope="data">
        <labels-predicted :record="data.item"></labels-predicted>
      </template>
      <template slot="timestamp" slot-scope="data">
        {{ data.item.timestamp | formatDateTime }}
      </template>
    </b-table>
    <b-pagination
      v-model="currentPage"
      :limit="5"
      :total-rows="count"
      :per-page="limit"
      :hide-ellipsis="true"
      :prev-text="'Сюда'"
      :next-text="'Туда'"
      :hide-goto-end-buttons="true"
      v-if="count > 0"
    ></b-pagination>
  </div>
</template>

<script>
import axios from 'axios'

import { ApiUrl } from '@/config'

import LabelsPredicted from './LabelsPredicted'

export default {
  name: 'Records',
  data () {
    return {
      records: [],
      count: 0,
      currentPage: 1,
      limit: 20,
      fields: [
        { key: 'id', label: 'ID' },
        { key: 'text', label: 'Текст' },
        { key: 'timestamp', label: 'Время' },
        { key: 'label', label: 'Класс' }
      ]
    }
  },
  watch: {
    currentPage (newPage, oldPage) {
      this.load_records()
    }
  },
  created () {
    this.load_records()
  },
  methods: {
    load_records () {
      axios.get(ApiUrl + `/records?page=${this.currentPage}`, {
        headers: { Authorization: `Token ${this.$store.state.token}` }
      })
        .then(response => {
          this.records = response.data.results
          this.count = response.data.count
        })
        .catch(e => {
          console.log(e)
        })
    }
  },
  components: {
    LabelsPredicted
  }
}
</script>

<style scoped>
</style>
