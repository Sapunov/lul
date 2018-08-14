<template>
  <b-dropdown :text="record_label">
    <b-dropdown-item
      v-for="label in (data.label_confirmed ? labels_exist : data.labels_predicted)"
      :key="label.label"
      @click="set_label(data.id, label.label)"
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
  props: ['data'],
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
    }
  },
  mounted () {
    if (this.data.label_confirmed) {
      this.record_label = this.data.label
    } else {
      this.record_label = 'Выберите класс'
    }
  }
}
</script>
