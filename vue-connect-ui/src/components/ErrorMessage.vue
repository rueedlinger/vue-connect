<template>
  <article class="message is-danger" v-if="error">
    <div class="message-header">
      <p v-if="error.title">{{ error.title }}</p>
      <p v-else>Error</p>
    </div>
    <div class="message-body">
      {{ error.message }}
    </div>
  </article>
</template>

<script>
export default {
  props: ["error"],
  data() {
    return {};
  },
};
</script>
