<template>
  <div class="box notification is-primary">
    <div class="columns">
      <div class="column is-1">
        <p class="title">
          {{ title }}
        </p>
      </div>
      <div class="column is-8 is-offset-1">
        <input
          v-if="hasSearchText"
          class="input is-primary is-rounded"
          type="text"
          placeholder="Name"
          v-bind:value="value"
          v-on:input="$emit('input', $event.target.value)"
        />
      </div>
      <div class="column is-1 is-offset-1">
        <button
          v-on:click="reloadData()"
          v-bind:class="[isLoading != `` ? `is-loading` : ``]"
          class="button"
        >
          <font-awesome-icon icon="sync-alt"></font-awesome-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["isLoading", "hasSearchText", "title", "reloadData", "value"],
  data() {
    return {};
  },
};
</script>
