<template>
  <div class="spender-nav py-2">
    <ul class="nav flex-column">
      <li class="nav-item">
        <router-link
          class="nav-link"
          to="/spender/transactions"
          :class="{active: $route.path == '/spender/transactions'}"
        >
          Транзакции
        </router-link>
      </li>
      <li class="nav-item">
        <router-link
          class="nav-link"
          to="/spender/categories"
          :class="{active: $route.path == '/spender/categories'}"
        >
          Категории
        </router-link>
      </li>
      <!-- <li class="nav-item">
        <router-link
          class="nav-link"
          to="/spender/budget"
          :class="{active: $route.path == '/spender/budget'}"
        >
          Бюджет
        </router-link>
      </li> -->
    </ul>
  </div>
</template>

<script>
export default {
  name: 'SpenderNav',
  data () {
    return {

    }
  }
}
</script>

<style scoped>
.spender-nav {
  box-shadow: 0 1px 0 0 #d7d8db, 0 0 0 1px #e3e4e8;
  background-color: #fff;
  border-radius: 2px;
}
.spender-nav a {
  padding-top: 10px;
  padding-bottom: 10px;
}
.spender-nav a:not(.active):hover {
  background-color: #f0f2f5;
  color: #007bff;
}
.active {
  border-right: 5px solid #343a40;
  background-color: #f0f2f5;
  color: #6c757d;
}
</style>
