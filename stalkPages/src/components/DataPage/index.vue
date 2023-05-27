<script setup>
import PageTitle from '../PageTitle/index.vue'
import DataType from './DataType.vue';

</script>

<template>
    <PageTitle :msg="'数据管理'">
        <span class="iconfont icon-jurassic_preview " ></span>
    </PageTitle>
    <DataType />
</template>