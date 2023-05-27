<script setup>
import PageTitle from '../PageTitle/index.vue'
import StackBar from './StackBar.vue';

</script>

<template>
    <PageTitle :msg="'数据集分析'">
        <span class="iconfont icon-tongji" ></span>
    </PageTitle>
    <div class="box">
        <StackBar />
    </div>
</template>

<style scoped>
.box {
    margin: 20px 0;
}
</style>