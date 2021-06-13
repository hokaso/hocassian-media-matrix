<template>
  <el-input
    :placeholder="placeholder"
    v-model="syncValue"
    :clearable="true"
    @keyup.enter.native="$emit('search')"
    class="input__search"
  >
    <template #append>
      <span @click="$emit('search')">{{ placeholderSearch}}</span>
    </template>
  </el-input>
</template>

<script>
export default {
  props: {
    value: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: '搜索视频素材'
    },
    placeholderSearch: {
      type: String,
      default: '搜索视频'
    },
  },
  computed: {
    syncValue: {
      set(v) {
        this.$emit('update:value', v);
      },
      get() {
        return this.value;
      }
    }
  },
  methods: {

  },
}
</script>

<style lang="scss">
.el-input-group__append {
  border: 1px solid #e64b3b;
  border-left: 0;
  background: #e64b3b;
  color: #fff;
  font-size: 16px;
  width: 140px;
  text-align: center;
  font-weight: bold;
  cursor: pointer;
}
</style>