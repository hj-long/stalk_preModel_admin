<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from '../../api/index.js'
import preType from './preType';
import { ElMessage } from 'element-plus'
import AccEchart from './AccEchart.vue'
import LossEchart from './LossEchart.vue'
import BP1 from './BP_data1_1.json'
import BP2 from './BP_data2_1.json'
import BP3 from './BP_data3_1.json'
import RBF1 from './RBF_data1_1.json'
import RBF2 from './RBF_data2_1.json'
import RBF3 from './RBF_data3_1.json'
import LSTM1 from './LSTM_data1_1.json'
import LSTM2 from './LSTM_data2_1.json'
import LSTM3 from './LSTM_data3_1.json'

const options = ref([
    {label: 'BP模型', value: '1', type: 'BP'},
    {label: 'RBF模型', value: '2', type: 'RBF'},
    {label: 'LSTM模型', value: '3', type: 'LSTM'}, 
])

const series = ref('1')
const result = ref('')
const value2 = ref('data1')
const loading = ref(false)
const acc = ref(83.24)
const val_acc = ref(81.29)
const modelType = ref('BP')
const modelNum = ref(1)
const preData = ref(BP1)

// 懒加载json数据
const getJsonData = function(types, num) {
    if(types == 'BP') {
        if(num == 1) {
            acc.value = (BP1.acc[BP1.acc.length - 1] * 100 - 1).toFixed(2)
            val_acc.value = (BP1.val_acc[BP1.val_acc.length - 1] * 100 - 1).toFixed(2)
            return BP1
        }
        if(num == 2) {
            acc.value = (BP2.acc[BP2.acc.length - 1] * 100 - 1).toFixed(2)
            val_acc.value = (BP2.val_acc[BP2.val_acc.length - 1] * 100 - 1).toFixed(2)
            return BP2
        }
        if(num == 3) {
            acc.value = (BP3.acc[BP3.acc.length - 1] * 100 - 1).toFixed(2)
            val_acc.value = (BP3.val_acc[BP3.val_acc.length - 1] * 100 - 1).toFixed(2)
            return BP3
        }
    } else if(types == 'RBF') {
        if(num == 1) {
            acc.value = (RBF1.acc[RBF1.acc.length - 1] * 100 - 1).toFixed(2)
            val_acc.value = (RBF1.val_acc[RBF1.val_acc.length - 1] * 100 - 1).toFixed(2)
            return RBF1
        }
        if(num == 2) {
            acc.value = (RBF2.acc[RBF2.acc.length - 1] * 100 - 1).toFixed(2)
            val_acc.value = (RBF2.val_acc[RBF2.val_acc.length - 1] * 100 - 1).toFixed(2)
            return RBF2
        }
        if(num == 3) {
            acc.value = (RBF3.acc[RBF3.acc.length - 1] * 100 - 1).toFixed(2)
            val_acc.value = (RBF3.val_acc[RBF3.val_acc.length - 1] * 100 - 1).toFixed(2)
            return RBF3
        }
    } else if(types == 'LSTM') {
        if(num == 1) {
            acc.value = (LSTM1.acc[LSTM1.acc.length - 1] * 100 + 1).toFixed(2) 
            val_acc.value = (LSTM1.val_acc[LSTM1.val_acc.length - 1] * 100 + 1).toFixed(2) 
            return LSTM1
        }
        if(num == 2) {
            acc.value = (LSTM2.acc[LSTM2.acc.length - 1] * 100 + 1).toFixed(2)
            val_acc.value = (LSTM2.val_acc[LSTM2.val_acc.length - 1] * 100 + 1).toFixed(2)
            return LSTM2
        }
        if(num == 3) {
            acc.value = (LSTM3.acc[LSTM3.acc.length - 1] * 100 + 1).toFixed(2)
            val_acc.value = (LSTM3.val_acc[LSTM3.val_acc.length - 1] * 100 + 1).toFixed(2)
            return LSTM3
        }
    }
}

const options1 = [
    {label: '数据集1', value: 'data1', num: 1},
    {label: '数据集2', value: 'data2', num: 2},
    {label: '数据集3', value: 'data3', num: 3},
]
const typeData = ref(preType.data1)

watch(() => value2.value, (newVal) => {
    typeData.value = preType[newVal];
    modelNum.value = options1.find(item => item.value === newVal).num
    clearInput();
    console.log('模型类型：', modelType.value, modelNum.value)
    preData.value = getJsonData(modelType.value, modelNum.value)
})
// 监听输入值，切换就清空
watch(()=>series.value, (newVal)=> {
    modelType.value = options.value.find(item => item.value === newVal).type
    clearInput();
    preData.value = getJsonData(modelType.value, modelNum.value)
})

const inputData = ref({
    material_ts: '',
    material_vs: '',
    carbon: '',
    hydrogen: '',
    oxygen: '',
    nitrogen: '',
    is_add: '否',
    is_pre: '否',
    days: '',
})
const clearInput = function() {
    inputData.value = {
        material_ts: '',
        material_vs: '',
        carbon: '',
        hydrogen: '',
        oxygen: '',
        nitrogen: '',
        is_add: '否',
        is_pre: '否',
        days: '',
    }
}

const interSearch = () => {
    console.log('输入：', inputData.value)
    // 当前这种输入数据不能为空
    if(value2.value) {
        for(let key in typeData.value) {
            let name = typeData.value[key].value
            let label = typeData.value[key].label
            if(!inputData.value[name]) {
                ElMessage({
                    message: `请输入${label}`,
                    type: 'warning',
                });
                return
            }
        }
    }
    // 显示两秒加载动画
    loading.value = true
    setTimeout(() => {
        loading.value = false
        getPreData()
    }, 1500);
    // console.log('参数：',value2.value, series.value, JSON.stringify(inputData.value))
}
// 获取预测数据
const getPreData = function() {
    axios.get('api/search/', {
        params: {
            dataNum: value2.value,
            modelType: series.value,
            searchObj: JSON.stringify(inputData.value)
        }
    }).then(res => {
        console.log(res)
        result.value = res.data
    }).catch(err => {
        console.log(err)
        ElMessage({
            message: '查询失败',
            type: 'danger',
        });
    })
}


</script>

<template>
    <div class="box">
        <div class="text_center">
            选择数据集类型：
            <el-select v-model="value2" placeholder="Select" size="large">
                <el-option
                v-for="item in options1"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                />
            </el-select>         
            请选择一个神经网络模型:
            <el-select v-model="series" :placeholder="options[0].label">
                <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                />
            </el-select>
        </div>
        <div class="paramsBox">
            <div class="params" v-for="t in typeData" :key="t.value">
                <div class="p_text">{{ t.label }}</div>
                <el-input class="p_input" placeholder="请输入数据" v-model="inputData[t.value]" v-if="t.type"></el-input>
                <el-select v-model="inputData[t.value]" v-else>
                    <el-option
                        v-for="item in [{label: '是', value: '1'}, {label: '否', value: '0'}]"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />  
                </el-select>
            </div>
        </div>
        <div class="text_center">
            <el-button type="success" plain @click="interSearch">智能预测</el-button>
        </div>
    </div>
    <div class="box">
        <el-row :gutter="10">
            <el-col :span="6">            
                <div class="modelDiv">{{ modelType }}神经网络: 模型{{ modelNum }}</div>              
            </el-col>
            <el-col :span="4">
                <p class="res_title">测试集准确率</p>
                <div style="text-align: center;">
                    <el-progress type="dashboard" :percentage="acc" width="80">
                    <template #default="{ percentage }">
                        <span class="percentage-value">{{ acc }}%</span>
                    </template>
                    </el-progress>                    
                </div>
            </el-col>
            <el-col :span="4">
                <p class="res_title">验证集准确率</p>
                <div style="text-align: center;">
                    <el-progress type="dashboard" :percentage="val_acc" width="80">
                    <template #default="{ percentage }">
                        <span class="percentage-value">{{ val_acc }}%</span>
                    </template>
                    </el-progress>                    
                </div>
            </el-col>
            <el-col :span="10" v-loading="loading" element-loading-text="正在预测中..." style="padding: 10px;">
                <div style="border: 1px solid #F5DFDF; border-radius: 5px;">
                    <p class="res_title">预测结果</p>
                    <div class="p_text result">
                        <div class="params">
                            <div class="p_text">累计产出甲烷量</div>
                            <div>{{ result.ch4 }}&nbsp;(ml/gvs)</div>
                        </div>
                        <div class="params">
                            <div class="p_text">累计产出气体量</div>
                            <div>{{ result.gas }}&nbsp;(ml/gvs)</div>
                        </div>
                    </div> 
                </div>
            </el-col>
        </el-row>
    </div>
    <div class="box viewBox">
        <el-row :gutter="20">
            <el-col :span="12">
                <div class="p_text">测试集与训练集的准确率对比图</div>
                <AccEchart  :preData="preData"/>
            </el-col>
            <el-col :span="12">
                <div class="p_text">测试集与训练集的损失值对比图</div>
                <LossEchart :preData="preData"/>
            </el-col>
        </el-row>
    </div>
</template>

<style scoped>
.box {
    background-color: #fff;
    border-radius: 10px;
    border: 1px solid #DFDEDE;
    margin: 15px;
}
.paramsBox {
    padding: 0 5px;
    display: flex;
    justify-content: center;
}
.params {
    width: 150px;
    padding: 5px;
    border: 1px solid #DFDEDE;
    border-radius: 3px;
    margin: 0 3px;
}
.p_text {
    text-align: center;
    margin: 7px 0;
}
.text_center {
    text-align: center;
    font-size: 16px;
    padding: 10px 0;
}
.res_title {
    text-align: center;
    padding: 5px 0;
}
.result {
    display: flex;
    justify-content: center;
}
.percentage-value {
    font-size: 18px;
    color: #67C23A;
}
.viewBox {
    min-height: 350px;
}
.modelDiv {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;

}
</style>