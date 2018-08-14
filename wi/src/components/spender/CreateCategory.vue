<template>
<div>
  <b-modal
    id="create-category"
    title="Добавить новую категорию"
    header-bg-variant="dark"
    header-text-variant="light"
    @shown="$refs.name.focus()"
    no-fade
    ref="createForm"
  >
    <form v-on:submit.prevent="create_category">
      <div class="alert alert-danger" role="alert" v-if="error">
        <small>{{ error }}</small>
      </div>
      <div class="form-group">
        <label for="name">Название*</label>
        <input
          type="text"
          class="form-control"
          id="name"
          placeholder="Название категории"
          ref="name"
          v-model="name">
      </div>
      <div class="form-group">
        <div class="custom-control custom-radio custom-control-inline">
          <input
            type="radio"
            id="expense"
            name="direction"
            class="custom-control-input"
            value="expense"
            v-model="picked">
          <label class="custom-control-label" for="expense">Расходы</label>
        </div>
        <div class="custom-control custom-radio custom-control-inline">
          <input
            type="radio"
            id="income"
            name="direction"
            class="custom-control-input"
            value="income"
            v-model="picked">
          <label class="custom-control-label" for="income">Доходы</label>
        </div>
      </div>
      <div class="form-group">
        <label for="desc">Описание</label>
        <textarea
          placeholder="Описание"
          v-model="description"
          class="form-control description"
          id="desc"
          rows="2"
        ></textarea>
      </div>
      <button type="submit" class="d-none">save</button>
    </form>
    <div slot="modal-footer" class="w-100">
      <div class="float-right">
        <b-btn variant="secondary" size="sm" @click="$refs.createForm.hide()">
          Отмена
        </b-btn>
        <b-btn variant="primary" size="sm" v-on:click="create_category()">
          Сохранить
        </b-btn>
      </div>
    </div>
  </b-modal>
</div>
</template>

<script>
import axios from 'axios'
import { ApiUrl } from '@/config'

export default {
  name: 'CreateCategory',
  props: ['direction'],
  data () {
    return {
      name: null,
      description: null,
      error: null,
      picked: 'expense',
      directionMapping: {
        'expense': 1,
        'income': 0
      }
    }
  },
  mounted () {
    this.set_direction(this.direction)
  },
  watch: {
    direction (newDirection, oldDirection) {
      this.set_direction(newDirection)
    }
  },
  methods: {
    show () {
      this.$refs.createForm.show()
    },
    create_category () {
      if (!this.name) {
        this.$refs.name.focus()
      } else {
        let data = {
          name: this.name,
          direction: this.directionMapping[this.picked]
        }
        if (this.description) {
          data.description = this.description
        }
        axios.post(ApiUrl + '/spender/categories', data, {
          headers: { Authorization: `Token ${this.$store.state.token}` }
        })
          .then(response => {
            this.$store.commit('add_category', response.data)
            this.name = null
            this.description = null
            this.error = null
            this.$refs.createForm.hide()
          })
          .catch(e => {
            this.error = e.response.data.error.error_msg
          })
      }
    },
    set_direction (direction) {
      if (direction !== undefined) {
        this.picked = direction
      }
    }
  }
}
</script>

<style scoped>
.description {
  resize: none;
}
</style>

<style>
.modal-header {
  border-top-left-radius: 0 !important;
  border-top-right-radius: 0 !important;
}
</style>
