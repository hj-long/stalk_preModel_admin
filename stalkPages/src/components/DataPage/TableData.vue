<script setup>
import { ref, watch } from 'vue'


const props = defineProps({
    tableData: {
        total: Number,
        data: Array,
    }
})

const emit = defineEmits(['getTableData'])

const tableData = ref(props.tableData.data)
const total = ref(props.tableData.total)
const currentPage = ref(1)

watch(() => props.tableData, (newVal) => {
    tableData.value = newVal.data
    total.value = newVal.total
})


const handleCurrentChange = (val) => {
    currentPage.value = val
    emit('getTableData', val)
}

</script>

<template>
    <div class="table1">
        <el-table :data="tableData" style="width: 100%" fit empty-text="暂无数据...请点击搜索" >
            <el-table-column prop="id" label="id"  width="80"/>
            <el-table-column prop="material_ts" label="原料TS"  />
            <el-table-column prop="material_vs" label="原料VS"  />
            <el-table-column prop="carbon" label="碳（%）"  width="100"/>
            <el-table-column prop="hydrogen" label="氢（%）"  width="100"/>
            <el-table-column prop="oxygen" label="氧（%）"  width="100"/>
            <el-table-column prop="nitrogen" label="氮（%）"  width="100"/>
            <el-table-column prop="is_add" label="是否添加剂"  width="120"/>
            <el-table-column prop="is_pre" label="是否预处理"  width="120"/>
            <el-table-column prop="days" label="时间（天）"  width="100"/>
            <el-table-column prop="ch4" label="累计产甲烷量（ml/gvs）"  />
            <el-table-column prop="gas" label="累计产气量（ml/gvs）"  />
        </el-table>    
    </div>
    <div class="pageDiv">
          <el-pagination
              v-model="currentPage"
              background
              layout="prev, pager, next, total"
              :total="total"
              @current-change="handleCurrentChange"
          />
    </div>
</template>

<style scoped>
.pageDiv {
    display: flex;
    justify-content: end;
    margin: 8px 20px;
    background-color: #fff;
}
.table1 {
    background-color: #fff;
    border: 1px solid lightcyan;
}
</style>