<template>
  <div class="login-form-wrapper">
    <h1 class="text-center login-logo">LOGULIFE</h1>
    <p class="text-center"><small>Вход в систему LOGULIFE</small></p>
    <div class="row justify-content-center">
      <form class="login-form" v-on:submit.prevent="login">
        <div class="alert alert-danger text-center" role="alert" v-if="error">
          <small>{{ error }}</small>
        </div>
        <div class="form-group">
          <label for="username">Логин</label>
          <input
            type="text"
            class="form-control"
            id="username"
            ref="username"
            placeholder="Логин"
            autofocus
            v-model="username">
        </div>
        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            type="password"
            class="form-control"
            id="password"
            ref="password"
            placeholder="Пароль"
            v-model="password">
        </div>
        <button type="submit" class="btn btn-primary btn-block">Войти</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import { ApiUrl } from '../config'

export default {
  name: 'LoginForm',
  data () {
    return {
      username: null,
      password: null,
      error: null
    }
  },
  created () {
    if (this.$localStorage.get('token') !== null) {
      this.$router.push('/')
      this.$router.go()
    }
  },
  methods: {
    login () {
      if (!(this.username && this.password)) {
        if (!this.username) {
          this.$refs.username.focus()
        } else {
          this.$refs.password.focus()
        }
      } else {
        axios.post(ApiUrl + '/tokens', {
          username: this.username,
          password: this.password
        })
          .then(response => {
            this.$localStorage.set('token', response.data.token)
            this.$store.dispatch('set_token', response.data.token)
            this.$localStorage.set('username', this.username)
            this.$store.dispatch('set_username', this.username)

            this.$router.push('/')
            this.$router.go()
          })
          .catch(e => {
            this.error = 'Неверные логин/пароль'
            this.password = null
            this.$refs.username.focus()
          })
      }
    }
  }
}
</script>

<style scoped>
.login-form {
  background-color: #fff;
  border: 1px solid #d8dee2;
  border-radius: 5px;
  padding: 30px 20px;
  width: 330px;
}
.login-logo {
  margin-bottom: 20px;
}
</style>
