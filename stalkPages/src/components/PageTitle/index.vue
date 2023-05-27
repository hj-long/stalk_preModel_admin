<script setup>
import { ref } from 'vue'

// 接收父组件传递的数据
const props = defineProps({
    msg: {
        type: String,
        default: '预测数据'
    }
})

const msg = ref(props.msg);


</script>

<template>
    <div class="pageTitle">
        <!-- 图标插槽 --> 
        <h1><slot></slot>&nbsp;{{ msg }}</h1>
    </div>
</template>

<style scoped>
.pageTitle {
    width: 100%;
    height: 32px;
    border-bottom: 1px solid #52d0f0;

}
</style>