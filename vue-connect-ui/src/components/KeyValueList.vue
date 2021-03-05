<template>
  <ul v-if="keys.length > 0">
    <li v-for="(key, index) in keys" :key="key">
      <b>{{ key }}:</b> {{ values[index] }}
    </li>
  </ul>
</template>

<script>
export default {
  props: ["keys", "values"],
  data() {
    return {};
  },
};
</script>
