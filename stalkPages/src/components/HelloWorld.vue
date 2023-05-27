<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <div>
    hello world!!
    <p>{{ count }}</p>
    <button @click="count++">加1</button>
  </div>
</template>

<style scoped>

</style>
