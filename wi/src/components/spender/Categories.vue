<template>
  <div class="d-flex">
    <nav class="nav-wrapper mr-3">
      <spender-nav></spender-nav>
    </nav>
    <main class="main-wrapper">
      <div class="wrapper">
        <div class="container-fluid button-wrapper clearfix">
          <div class="float-right">
            <b-button
              size="secondary"
              variant="sm"
              @click="$refs.CreateCategoryModal.show()">
              Добавить категорию
            </b-button>
          </div>
          <div class="float-left">
            <ul class="nav nav-pills">
              <li class="nav-item">
                <a
                  class="nav-link"
                  :class="{'active': activeTab === 'expense'}"
                  href="#"
                  @click.stop.prevent="activeTab = 'expense'"
                  >Расходы</a>
              </li>
              <li class="nav-item">
                <a
                  class="nav-link"
                  :class="{'active': activeTab === 'income'}"
                  href="#"
                  @click.stop.prevent="activeTab = 'income'"
                  >Доходы</a>
              </li>
            </ul>
          </div>
        </div>
        <div class="list-group list-group-flush">
          <div
            class="list-group-item category-item align-items-center"
            v-for="category in $store.state.spender.categories" :key="category.id"
            v-if="category.direction_human === activeTab"
          >
            <div class="row">
              <div class="col">
                <p>{{ category.name }}</p>
                <p>
                  <small class="text-muted">{{ category.description }}</small>
                </p>
              </div>
              <div class="col-2 text-right">
                <span
                  v-if="category.owner !== null"
                  @click="delete_category(category.id)"
                  class="oi oi-x delete-button align-middle"
                  title="Удалить категорию"
                  v-b-tooltip.hover
                ></span>
              </div>
            </div>
          </div>
        </div>
        <create-category
          ref="CreateCategoryModal"
          :direction="activeTab"
        ></create-category>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import { ApiUrl } from '@/config'
import SpenderNav from './SpenderNav'
import CreateCategory from './CreateCategory'

export default {
  name: 'Categories',
  data () {
    return {
      activeTab: 'expense'
    }
  },
  mounted () {
    if (this.$store.state.spender.categories_loaded === false) {
      this.$store.dispatch('load_categories')
    }
  },
  methods: {
    delete_category (categoryId) {
      axios.delete(ApiUrl + `/spender/categories/${categoryId}`, {
        headers: {Authorization: `Token ${this.$store.state.token}`}
      })
        .then(response => {
          this.$store.commit('delete_category', categoryId)
        })
        .catch(e => {
          //
        })
    }
  },
  components: {
    SpenderNav,
    CreateCategory
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
.button-wrapper {
  background-color: #fafbfc;
  border-bottom: 1px solid #e7e8ec;
  padding-top: 10px;
  padding-bottom: 10px;
}
.category-item p {
  padding: 0;
  margin: 0;
}
.delete-button {
  color: #eee;
  font-size: .8em;
  cursor: pointer;
}
.delete-button:hover {
  color: #ddd;
}
.delete-button:active {
  color: #ccc;
}
a.nav-link {
  padding-top: 4px;
  padding-bottom: 4px;
}
</style>
