<template>
  <div>
    <article
      v-for="error in errors"
      :key="error.message"
      class="message is-danger"
    >
      <div class="message-header">
        <p v-if="error.title">{{ error.title }}</p>
        <p v-else>Error</p>
      </div>
      <div class="message-body">
        {{ error.message }}
      </div>
    </article>
  </div>
</template>

<script>
export default {
  props: ["errors"],
  data() {
    return {};
  },
};
</script>
