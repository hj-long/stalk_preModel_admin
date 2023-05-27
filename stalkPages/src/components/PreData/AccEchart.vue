<script setup>
import { ref, onMounted, toRefs, watch } from "vue";
import * as echarts from 'echarts'

const echart_1 = ref()

onMounted(() => {
    let option = getOption(props.preData)
    draw(option)
})

const props = defineProps({
    preData: {
        type: Object,
        default: () => import('./BP_data3_1.json')
    }
})

watch(() => props.preData, (newVal) => {
    let option = getOption(newVal)
    draw(option)
})

function getOption(datas) {
    let option = {
        legend: {
            data: ['测试集', '训练集']
        },
        xAxis: {
            name: '训练次数',
            type: 'category',
            data:  datas.epochs || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
            name: '准确率',
            type: 'value',
            axisLabel: {
                formatter: '{value}'
            }
        },
        tooltip: {
            trigger: 'axis',
        },
        series: [
            {   
                name: '测试集',
                showSymbol: false,
                data: datas.acc || [150, 230, 224, 218, 135, 147, 260],
                type: 'line'
            },
            {
                name: '训练集',
                
                data: datas.val_acc || [320, 332, 301, 334, 390, 330, 320],
                type: 'scatter',
                symbolSize: 6,
                itemStyle: {
                    color: '#ff7f50'
                }
            }
        ]
    }
    return option
}

function draw(option) {
    var myChart = echarts.init(echart_1.value)
    myChart.setOption(option)
}

</script>

<template>
    <div ref="echart_1" style="height: 350px; width: 100%; border: 1px solid #F5DFDF;"></div>
</template>