<template>
  <div>
    <m-header></m-header>
    <router-view></router-view>
  </div>
</template>

<script>
import MHeader from '../common/MHeader';

export default {
  name: "Index",
  components: {
    MHeader
  }
}
</script>

<style lang="scss" scoped>

</style>
