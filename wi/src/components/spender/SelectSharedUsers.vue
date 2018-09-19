<template>
  <div class="filter-wrapper">
    <p class="filter-title">Доступные транзакции</p>
    <div class="users-wrapper" v-if="selected_users.length > 0">
      <div
        class="user-badge d-flex"
        v-for="user in selected_users"
        :key="user.id">
        <p class="p-0 m-0 flex-grow-1">
          {{ user.first_name }} {{ user.last_name }}
        </p>
        <p
          class="remove-selection oi oi-x x-icon remove-selection"
          @click="remove_selection(user)"></p>
      </div>
    </div>
    <b-dropdown
      variant="light"
      text="Выберите пользователя"
      :disabled="visible_users.length === 0">
      <b-dropdown-item
        v-for="user in visible_users"
        :key="user.id"
        @click="select_user(user)">
        {{ user.first_name }} {{ user.last_name }}
      </b-dropdown-item>
    </b-dropdown>
  </div>
</template>

<script>
import axios from 'axios'
import { ApiUrl } from '@/config'

export default {
  name: 'SelectSharedUsers',
  data () {
    return {
      shared_users: [],
      selected_users: []
    }
  },
  mounted () {
    this.load_shared_users()
  },
  watch: {
    selected_users (newValue, oldValue) {
      this.$emit('filterSharedUsers', newValue)
    }
  },
  computed: {
    visible_users () {
      return this.shared_users.filter(user => {
        for (var i = 0; i < this.selected_users.length; ++i) {
          if (user.id === this.selected_users[i].id) return false
        }
        return true
      })
    }
  },
  methods: {
    load_shared_users () {
      axios.get(ApiUrl + `/spender/transactions/sharedusers`, {
        headers: { Authorization: `Token ${this.$store.state.token}` }
      })
        .then(response => {
          this.shared_users = response.data.results
        })
        .catch(e => {
          console.log(e)
        })
    },
    select_user (user) {
      this.selected_users.push(user)
    },
    remove_selection (user) {
      for (var i = 0; i < this.selected_users.length; ++i) {
        if (this.selected_users[i].id === user.id) {
          this.selected_users.splice(i, 1)
          break
        }
      }
    }
  }
}
</script>

<style scoped>
.filter-wrapper {
  padding-left: 1rem;
  padding-right: 1rem;
}
.users-wrapper {
  margin-bottom: 10px;
}
.users-wrapper span {
  margin-right: .2rem;
  margin-bottom: .4rem;
}
.users-wrapper span:last-child {
  margin-right: 0 !important;
}
.remove-selection {
  cursor: pointer;
  font-size: 80%;
  padding: 0;
  margin: 0;
  color: #dae2e9;
}
.remove-selection:hover {
  color: #d0d9e3;
}
.remove-selection:active {
  color: #bac8d6;
}
.filter-title {
  color: #6c757d;
  margin-bottom: 10px;
  padding: 0;
}
.user-badge {
  padding: 0.25em 0.4em;
  font-size: 80%;
  font-weight: 700;
  line-height: 1;
  white-space: nowrap;
  vertical-align: baseline;
}
</style>
