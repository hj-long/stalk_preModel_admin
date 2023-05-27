<script setup>
import { ref, watch, onMounted } from 'vue'

const table_data = ref([])
const props = defineProps({
    tableData: {
        type: Array,
        default: () => []
    },
})


watch (props.tableData, (newVal) => {
    table_data.value = newVal
})

// 接收事件
const emit = defineEmits(['openDialog', 'searchUser', 'deleteUser'])
const toChange = (uid) => {
    emit('openDialog', 1, uid)
}
const deleteUser = (uid) => {
    emit('deleteUser', uid)
}
</script>

<template>
    <div class="table1">
        <el-table :data="tableData" style="width: 100%" fit empty-text="暂无数据...请点击搜索" >
            <el-table-column prop="id" label="id"  width="80"/>
            <el-table-column prop="name" label="用户名"  />
            <el-table-column prop="email" label="邮箱"  />
            <el-table-column prop="is_admin" label="管理员"  />
            <el-table-column prop="gender" label="性别"  />
            <el-table-column prop="phone" label="电话"  />
            <el-table-column label="操作"  >
                <template #default="scoped">
                    <el-button type="success" @click="toChange(scoped.row.id)">修改</el-button>
                    <el-button type="danger"  @click="deleteUser(scoped.row.id)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>    
    </div>

</template>

<style scoped>
.table1 {
    background-color: #fff;
    border-top: 1px solid lightcyan;
    border-bottom: 1px solid lightcyan;
    width: 100%;
}
</style>