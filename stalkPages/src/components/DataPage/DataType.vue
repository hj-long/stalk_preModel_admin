<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from '../../api/index.js'
import TableData from './TableData.vue';
import peopleData from './peopleData.js';
import EchartImg from './EchartImg.vue';

const value = ref('陈维维')
const tableData = ref([])
const datatype = ref('秸秆')
const limit = ref([1, 212])
const value2 = ref('data1')
const childData = ref({})

let options = ref(peopleData.data1.map(item => {
        return {
            value: item.name,
            label: item.name
        }
    }))

let nameMap = ref(peopleData.data1)
const options1 = [
    {label: '数据集1', value: 'data1'},
    {label: '数据集2', value: 'data2'},
    {label: '数据集3', value: 'data3'},
]
watch(() => value2.value, (newVal) => {
    nameMap.value = peopleData[newVal]
    options.value = nameMap.value.map(item => {
        return {
            value: item.name,
            label: item.name
        }
    })
    value.value = options.value[0].value
    console.log(nameMap.value)
})


const getTableData = (pages) => {
    axios.get('/api/tableData', {
        params: {
            tableNum: value2.value || 'data1',
            limit: JSON.stringify(limit.value),
            page: pages ? pages : 1
        }
    }).then(res => {
        console.log('返回：', res)
        tableData.value = res
        childData.value = {
            daySet: res.data.map(item => item.days + '天'),
            ch4: res.data.map(item => item.ch4),
            gas: res.data.map(item => item.gas),
        }
    })
}

watch(() => value.value, (newVal) => {
    // 根据名字，更新类型和范围
    let data = nameMap.value.filter(item => item.name === newVal)
    datatype.value = data[0].datatype
    limit.value = data[0].limit
})

onMounted(() => {
    getTableData()
})

</script>

<template>
    <div class="box">
        <div>
            选择数据集：
            <el-select v-model="value2" placeholder="Select" size="large">
                <el-option
                v-for="item in options1"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                />
            </el-select> 
            负责人：
            <el-select v-model="value" class="m-2" placeholder="Select" size="large">
                <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                />
            </el-select>    
            <el-button type="primary" plain @click="getTableData">搜索</el-button>        
        </div>
        <div>
            <span>数据类型：{{ datatype }}</span>
        </div>  
    </div>
    <TableData  @getTableData="getTableData" :tableData="tableData"/>
    <EchartImg  :childData="childData"/>
</template>

<style scoped>
.box {
    margin: 15px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}



</style>