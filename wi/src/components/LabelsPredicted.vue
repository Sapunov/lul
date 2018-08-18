<template>
  <b-dropdown :text="record_label">
    <b-dropdown-item
      v-for="label in (record.labels_predicted.length > 0 ? record.labels_predicted : labels_exist)"
      :key="label.label"
      @click="set_label(record.id, label.label)"
    >
    {{ label.label }}
    </b-dropdown-item>
  </b-dropdown>
</template>

<script>
import axios from 'axios'

import { ApiUrl } from '@/config'

export default {
  name: 'LabelsPredicted',
  data () {
    return {
      record_label: '',
      labels_exist: [
        {'label': 'expense'},
        {'label': 'income'},
        {'label': 'time'},
        {'label': 'other'}
      ]
    }
  },
  props: ['record'],
  methods: {
    set_label (recordId, label) {
      axios.post(ApiUrl + `/records/${recordId}/label`, {
        label: label,
        force: true
      }, {
        headers: { Authorization: `Token ${this.$store.state.token}` }
      })
        .then(response => {
          this.record_label = label
        })
        .catch(e => {
          console.log(e)
        })
    },
    process_label () {
      if (this.record.label_confirmed) {
        this.record_label = this.record.label
      } else {
        this.record_label = 'Выберите класс'
      }
    }
  },
  updated () {
    this.process_label()
  },
  mounted () {
    this.process_label()
  }
}
</script>
