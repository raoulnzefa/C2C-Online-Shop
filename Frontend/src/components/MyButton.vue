<template>
  <input :type="inputType"
         :class="classStyle"
         :value="text">
</template>
<script>
export default {
  props: {
    text: {},
    inputType: {
      default: 'button'
    },
    classStyle: {
      default: 'default-btn'
    }
  },
}
</script>
<style lang="scss" rel="stylesheet/scss" scoped>
@import "../assets/style/theme";

%style {
  width: 100px;
  height: 30px;
  line-height: 28px;
  vertical-align: middle;
}

@mixin color($a,$b,$c) {
  border: 1px solid $a;
  border-radius: 4px;
  font-size: 12px;
  color: $b;
  background-color: $c;
}

input {
  display: inline-block;
  cursor: pointer;
  text-align: center;
}

.default-btn {
  @include color(#e1e1e1, #646464, #f9f9f9);
  @extend %style;
  background-image: -webkit-linear-gradient(top, $cf, #f9f9f9);
  background-image: linear-gradient(180deg, $cf, #f9f9f9);

  &:hover {
    background-color: #eee;
    background-image: -webkit-linear-gradient(top, #f5f5f5, #eee);
    background-image: linear-gradient(180deg, #f5f5f5, #eee);
  }
}
</style>
