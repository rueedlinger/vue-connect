<template>
  <article class="message is-danger" v-if="message">
    <div class="message-header">
      <p v-if="title">{{ title }}</p>
      <p v-else>Error</p>
    </div>
    <div class="message-body">
      {{ message }}
    </div>
  </article>
</template>

<script>
export default {
  props: ["message", "title"],
  data() {
    return {
      isDisplayed: true,
    };
  },
};
</script>
