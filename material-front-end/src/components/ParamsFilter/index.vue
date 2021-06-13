<template>
  <div class="params-filter__wrap">
    <div
      v-for="(param, key) in params"
      :key="key"
      class="params-filter__block"
      @mouseover="$set(params[key], 'showChoose', true)"
      @mouseleave="params[key].showChoose = false">
      <span class="title">{{ selectTitle(key, param) }}</span>
      <i class="el-icon-caret-bottom icon-arrow" />
      <div
        :class="{ 'show': params[key].showChoose }"
        class="params-filter__choose">
        <p
          v-for="item in param"
          :key="item.value"
          :class="{ 'active': queryParams[key] === item.value.toString()}"
          class="choose-content"
          @click="$emit('search', key, item.value)">
          {{ item.label }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    params: {
      type: Object,
      default: {}
    },
    queryParams: {
      type: Object,
      default: {}
    },
    translation: {
      type: Object,
      default: {}
    },
  },
  data() {
    return {
      showChoose: false
    }
  },
  methods: {
    selectTitle(key, param) {
      const _this = this;
      const [{ label, value }] = param.filter(item => item.value.toString() === _this.queryParams[key]);
      return value === '' ? this.translation[key] : label;
    },
  },
}
</script>

<style lang="scss">
.params-filter__wrap {
  .params-filter__block {
    position: relative;
    font-size: 16px;
    cursor: pointer;
    display: inline-block;
    margin-right: 60px;
    .title {
      font-weight: bold;
    }
    .icon-arrow {
      margin-left: 5px;
    }
  }
  .params-filter__choose {
    position: absolute;
    top: 25px;
    background: #fff;
    width: 100px;
    box-shadow: 0 0 8px 0 rgba(0,0,0,0.1);
    z-index: 999;
    opacity: 0;
    visibility: hidden;
    transition: 0.3s all ease;
    &.show {
      opacity: 1;
      visibility: visible;
    }
    .choose-content {
      font-size: 14px;
      padding: 5px 10px;
      cursor: pointer;
      &.active {
        font-weight: bold;
      }
      &:hover {
        background: #f0f0f0;
      }
    }
  }
}

</style>
