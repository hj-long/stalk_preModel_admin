<script setup>
import { ref } from 'vue'
import router from './rounter';

// 如果发生跳转，把背景图片元素隐藏
const showBg = ref(true);

// 监听路由变化
router.beforeEach((to, from, next) => {
  // console.log(to, from);
  if(to.path == '/login') {
    showBg.value = true;
  } else {
    showBg.value = false;
  }
  next();
})


</script>

<template>
  <div id="app">
    <div class="bg" v-show="showBg"></div>
    <!-- 路由出口 -->
    <!-- 路由匹配到的组件将渲染在这里 -->
    <router-view></router-view>
  </div>
</template>

<style scoped>
#app {
  width: 100vw;
  height: 100vh;
}
.bg {
  width: 100%;
  height: 100%;
  background: url('./assets/bg.jpg');
  background-size: cover;
  filter: blur(5px);
}
</style>
