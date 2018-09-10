<template>
  <div v-if="aggs && aggs.categories.length > 0">
    <div
      class="pb-1 d-flex align-items-center cursor"
      v-b-toggle="collapseId"
      @click="opened = !opened">
      <div class="d-flex">
        <div class="direction-title">
          <b>{{ title }}</b>
        </div>
        <template v-if="aggs.summary.default_currency === null">
          <div>
            <span class="text-muted">=</span>
            <span>{{ formatPrice(aggs.summary.currencies[0].amount) }}</span>
            <small class="text-info">{{ aggs.summary.currencies[0].currency }}</small>
          </div>
        </template>
        <template v-else>
          <div v-b-popover.hover.bottom="popover_content(aggs.summary.currencies)">
            <span class="text-muted">≈</span>
            <span>{{ formatPrice(aggs.summary.default_currency.amount) }}</span>
            <small class="text-info">{{ aggs.summary.default_currency.currency }}</small>
          </div>
        </template>
        <div class="pl-1 text-muted">
          <small>({{ aggs.categories.length }} категорий)</small>
        </div>
      </div>
      <div class="flex-grow-1 text-right">
        <small
          class="oi oi-chevron-bottom text-custom-grey"
          :class="{'oi-chevron-top': opened, 'oi-chevron-bottom': !opened}"
        ></small>
      </div>
    </div>
    <b-collapse :id="collapseId">
      <div class="d-flex justify-content-between category-item mr-3"
        v-for="category in aggs.categories" :key="category.id">
        <div class="d-flex align-items-center">
          <a
            v-bind:class="{ 'italic': filteredCategory === category.id }"
            href="#"
            @click.prevent="sayFilterCategory(category)"
            class="text-dark">{{ category.name }}</a>
          <small
            title="Убрать фильтр"
            class="oi oi-x x-icon"
            v-b-tooltip.hover
            @click="sayFilterCategory(null)"
            v-if="filteredCategory === category.id"></small>
        </div>
        <template v-if="category.default_currency === null">
          <div>
            {{ formatPrice(category.currencies[0].amount) }}
            <small class="text-info">
            {{ category.currencies[0].currency }}
            </small>
          </div>
        </template>
        <template v-else>
          <div
            v-b-popover.hover.bottom="popover_content(category.currencies)">
            <span class="text-muted">≈</span>
            {{ formatPrice(category.default_currency.amount) }}
            <small class="text-info">
              {{ category.default_currency.currency }}
            </small>
          </div>
        </template>
      </div>
    </b-collapse>
  </div>
</template>

<script>
export default {
  name: 'TransactionsAggs',
  data () {
    return {
      opened: false,
      collapseId: 'collapse' + this.title
    }
  },
  props: ['aggs', 'title', 'filteredCategory'],
  methods: {
    popover_content (currencies) {
      var content = '<div class="px-1">'
      for (let i = 0; i < currencies.length; ++i) {
        content += `
        <div class="d-flex justify-content-between align-items-center">
          <b class="pr-3">${this.formatPrice(currencies[i].amount)}</b>
          <small class="text-info">${currencies[i].currency}</small>
        </div>`
      }
      content += '</div>'
      return {
        content: content,
        html: true
      }
    },
    formatPrice (value) {
      let val = (value / 1).toFixed(2).replace('.', ',')
      return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')
    },
    sayFilterCategory (category) {
      this.$emit('filterCategory', category)
    }
  }
}
</script>

<style scoped>
.category-item {
  border-bottom: 1px solid #eff3f6;
}
.category-item:last-child {
  border-bottom: none;
}
.text-custom-grey {
  color: #eee;
}
.cursor {
  cursor: pointer;
}
.direction-title {
  min-width: 80px;
}
.x-icon {
  color: #dae2e9;
  font-size: 0.7rem;
  padding-left: 5px;
  cursor: pointer;
}
.x-icon:hover {
  color: #d0d9e3;
}
.x-icon:active {
  color: #bac8d6;
}
.italic {
  font-style: italic;
}
</style>
