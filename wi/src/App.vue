<template>
  <div id="app">
    <nav class="navbar navbar-expand-sm flex-md-nowrap py-1 navbar-dark bg-dark" v-if="loggedIn()">
      <router-link
        to="/"
        :class="'navbar-brand'"
      >LOGULIFE</router-link>
      <ul class="navbar-nav mr-auto">
        <li class="nav-item" :class="{'active': $route.path == '/records'}">
          <router-link
            to="/records"
            class="nav-link"
          >Records</router-link>
        </li>
        <li class="nav-item"
          :class="{'active': $route.path.match(/^\/spender\//)}">
          <router-link
            to="/spender/transactions"
            class="nav-link"
          >Spender</router-link>
        </li>
      </ul>
      <div class="navbar-nav my-2 my-lg-0">
        <b-dropdown class="m-md-0" right size="sm">
          <template slot="button-content">
            {{ username }}
          </template>
          <!-- <b-dropdown-item>First Action</b-dropdown-item> -->
          <!-- <b-dropdown-divider></b-dropdown-divider> -->
          <b-dropdown-item v-on:click="logout">Выйти</b-dropdown-item>
        </b-dropdown>
      </div>
    </nav>
    <div class="container main">
      <router-view/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
    }
  },
  computed: {
    username () {
      return this.$store.state.username
    }
  },
  methods: {
    loggedIn () {
      return this.$localStorage.get('token') !== null
    },
    logout () {
      this.$localStorage.remove('token')
      this.$localStorage.remove('username')
      this.$router.go()
    }
  },
  created () {
    if (this.loggedIn()) {
      this.$store.dispatch('set_token', this.$localStorage.get('token'))
      this.$store.dispatch('set_username', this.$localStorage.get('username'))
    } else if (this.$route.path !== '/login') {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.top-navbar {
  padding-top: 10px;
  padding-bottom: 10px;
}

.main {
  padding-top: 15px;
  padding-bottom: 15px;
  min-width: 800px !important;
}
</style>

<style>
body {
  background-color: #edeef0;
}
.dropdown-item, .dropdown-toggle {
  outline: none;
}
</style>
