<script setup>
import { ref, onMounted, toRefs, watch } from "vue";
import * as echarts from 'echarts'

const echart_1 = ref()
onMounted(() => {
    let option = getOption({})
    draw(option)
})

const props = defineProps({
    childData: {
        daySet: Array,
        ch4: Array,
        gas: Array,
    }
})

watch(() => props.childData, (newVal) => {
    let option = getOption(newVal)
    draw(option)
})

function getOption(datas) {
    let option = {
            title: {
                text: '预期输出'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['甲烷量', '产气量']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
                feature: {
                saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: datas.daySet || ['1天', '2天', '3天', '4天', '5天', '6天', '7天']
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                name: '甲烷量',
                type: 'line',
                stack: 'Total',
                data: datas.ch4 || [120, 132, 101, 134, 90, 230, 210]
                },
                {
                name: '产气量',
                type: 'line',
                stack: 'Total',
                data: datas.gas || [220, 182, 191, 234, 290, 330, 310]
                }
            ]
        };
    return option
}

function draw(option) {
    var myChart = echarts.init(echart_1.value)
    myChart.setOption(option)
}

</script>

<template>
    <div ref="echart_1" style="height: 260px; width: 100%; border: 1px solid #F5DFDF;"></div>
</template>