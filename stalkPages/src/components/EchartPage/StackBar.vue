<script setup>
import { ref, watch, onMounted } from 'vue'
import * as echarts from 'echarts'

const echart_1 = ref()
function draw(option) {
    var myChart = echarts.init(echart_1.value)
    myChart.setOption(option)
}

onMounted(() => {
    let option = getOptions()
    draw(option)
})

function getOptions() {
    let option = {
            title: {
                text: '输入特征分析'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                // Use axis to trigger tooltip
                type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
                }
            },
            legend: {},
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value'
            },
            yAxis: {
                type: 'category',
                data: ['数据集1', '数据集2', '数据集3']
            },
            series: [
                {
                name: '原料TS',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [3258, 1173, 2122]
                },
                {
                name: '原料VS',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [3258, 1173, 2122]
                },
                {
                name: '碳含量',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [3258, 0, 2122]
                },
                {
                name: '氢含量',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [3258, 0, 1912]
                },
                {
                name: '氧含量',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [3258, 0, 452]
                },
                {
                name: '添加剂',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [3258, 714, 135]
                },
                {
                name: '预处理',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true
                },
                emphasis: {
                    focus: 'series'
                },
                data: [2862, 0, 1620]
                }
            ]
            };
    return option
}


</script>

<template>
    <div ref="echart_1" style="height: 260px; width: 100%; border: 1px solid #F5DFDF;"></div>
</template>

<style scoped>

</style>