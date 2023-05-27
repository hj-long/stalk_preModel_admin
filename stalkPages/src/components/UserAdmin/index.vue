<script setup>
import { ref, watch, onMounted, reactive } from 'vue';
import PageTitle from '../PageTitle/index.vue';
import UserTable from './UserTable.vue';
import axios from '../../api/index.js';
import { ElMessage, ElMessageBox } from 'element-plus';

const input = ref('');
const tableData = ref([]);
const total = ref(0);
const dialogTitle = ref('修改用户信息');
const currentPage = ref(1)


onMounted(() => {
    searchUser();
})

const searchUser = (page) => {
    axios.get('/user/getUser', {
        params: {
            name: input.value,
            page: page || 1,
        }
    }).then(res => {
        console.log(res);
        tableData.value = res.data;
        total.value = res.total;
    })
}

const toClear = function() {
    input.value = '';
    currentPage.value = 1;
    searchUser();
}

// 对话框
const dialogFormVisible = ref(false)
const rulesForm = ref({})

// 表单验证
const form = reactive({
    name: '',
    password: '',
    email: '',
    is_admin: '',
    gender: '',
    phone: ''
})
const rules = reactive({
    name: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 2, max: 8, message: '长度在 2 到 8 个字符', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 3, max: 16, message: '长度在 3 到 16 个字符', trigger: 'blur' }
    ],
    email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
    ],
    is_admin: [
        { required: true, message: '请选择是否为管理员', trigger: 'blur' }
    ],
    gender: [
        { required: true, message: '请选择性别', trigger: 'blur' }
    ],
    phone: [
        { required: true, message: '请输入电话号码', trigger: 'blur' },
        { pattern: /^1[3456789]\d{9}$/, message: '请输入正确的电话号码', trigger: 'blur' }
    ]
})

// 打开对话框
const openDialog = (num, uid) => {
    if(num == 1) {
        dialogTitle.value = '修改用户信息'
    } else {
        dialogTitle.value = '新增用户'
    }
    dialogFormVisible.value = true
    // 从tableData中找到对应的数据
    let data = tableData.value.find(item => item.id == uid)
    console.log('找到：',data)
    if(!data) {
        // 如果没有找到，就是新增用户，清空form
        for(let key in form) {
            form[key] = ''
        }
        return
    }
    // 将数据赋值给form
    for(let key in data) {
        form[key] = data[key]
    }
    console.log('form：',form)
}

const submitForm = async (formEl) => {
    if (!formEl) return alert('请传入表单对象')
    await formEl.validate((valid, fields) => {
        if (valid) {
            console.log('提交!')
            // 判断是新增还是修改
            if(dialogTitle.value == '新增用户') {
                console.log('新增用户')
                // 请求新增用户
                addUser();
            } else {
                console.log('修改用户')
                // 请求修改用户信息
                updateUser();
            }
        } else {
            console.log('错误的提交!', fields)
        }
    })
}

// 请求修改用户信息
const updateUser = () => {
    axios.post('/user/updateUser/', form).then(res => {
        console.log(res)
        if(res.msg == '修改用户信息成功') {
            dialogFormVisible.value = false;
            searchUser(currentPage.value);
            ElMessage({
                message: res.msg,
                type: 'success'
            })
        }
    }).catch(err => {
        console.log(err)
        ElMessage({
                message: '修改失败',
                type: 'success'
        })
    })
}
// 请求新增用户
const addUser = () => {
    axios.post('/user/addUser/', form).then(res => {
        console.log(res)
        if(res.msg == '添加用户成功') {
            dialogFormVisible.value = false;
            searchUser(currentPage.value);
            ElMessage({
                message: res.msg,
                type: 'success'
            })
        }
    }).catch(err => {
        console.log(err)
        ElMessage({
                message: '添加失败',
                type: 'success'
        })
    })
}
// 删除用户
const deleteUser = (uid) => {
    console.log('删除用户', uid)
    // 弹窗确认
    ElMessageBox.confirm('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        // 确定删除
        axios.post('/user/deleteUser/', {id: uid}).then(res => {
        console.log(res)
        if(res.msg == '删除用户成功') {
                searchUser(currentPage.value);
                ElMessage({
                    message: res.msg,
                    type: 'success'
                })
            }
        }).catch(err => {
            console.log(err)
            ElMessage({
                    message: '删除失败',
                    type: 'success'
            })
        })
    }).catch(() => {
        // 取消删除
        ElMessage({
            type: 'info',
            message: '已取消删除'
        });
    });
}


const handleClose = () => {
    dialogFormVisible.value = false;
}

const resetForm = (formEl) => {
    formEl.resetFields()
    dialogFormVisible.value = false;
}

const handleCurrentChange = (val) => {
    currentPage.value = val
    console.log('当前页', val)
    searchUser(val)
}

</script>

<template>
    <PageTitle :msg="'用户管理'">
        <span class="iconfont icon-yonghu" ></span>
    </PageTitle>
    <div class="box flexBox">
        <div>
            <span>用户名：</span>
            <el-input v-model="input" placeholder="请输入用户名" />&nbsp;&nbsp;
            <el-button type="success" @click="searchUser"><el-icon><Search /></el-icon> &nbsp;查询</el-button>
            <el-button type="primary" plain  @click="toClear"><el-icon><Refresh /></el-icon> &nbsp;重置</el-button>
        </div>
        <div>
            <el-button type="success" @click="openDialog(0)"><el-icon><Plus /></el-icon>新增用户</el-button>
        </div>
    </div>
    <div class="box">
        <UserTable  :tableData="tableData" :total="total" @openDialog="openDialog" @searchUser="searchUser" @deleteUser="deleteUser"/>
        <div class="pageDiv">
          <el-pagination
              v-model="currentPage"
              background
              layout="prev, pager, next, total"
              :current-page="currentPage"
              :page-size="5"
              :total="total"
              @current-change="handleCurrentChange"
        />
    </div>
    </div>
    <!-- 对话框 -->
    <el-dialog v-model="dialogFormVisible" :title="dialogTitle" :before-close="handleClose">
        <el-form :model="form" label-width="100px" :rules="rules" ref="rulesForm">
            <el-form-item label="用户名" prop="name">
                <el-input v-model="form.name" />
            </el-form-item>
            <el-form-item label="密码" prop="password" v-if="dialogTitle == '新增用户'">
                <el-input v-model="form.password" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
                <el-input v-model="form.email" />
            </el-form-item>
            <el-form-item label="管理员" prop="is_admin">
                <el-select v-model="form.is_admin" placeholder="未设置">
                    <el-option label="是" value="是" />
                    <el-option label="否" value="否" />
                </el-select>
            </el-form-item>
            <el-form-item label="性别" prop="gender">
                <el-select v-model="form.gender" placeholder="未设置">
                    <el-option label="男" value="男" />
                    <el-option label="女" value="女" />
                </el-select>
            </el-form-item>
            <el-form-item label="手机" prop="phone">
                <el-input v-model="form.phone" />
            </el-form-item>
        </el-form>
        <template #footer>
        <span class="dialog-footer">
            <el-button @click="resetForm(rulesForm)" >取消</el-button>
            <el-button type="primary" @click="submitForm(rulesForm)">确认</el-button>
        </span>
        </template>
    </el-dialog>
</template>

<style scoped>
.box {
    background-color: #fff;
    border-radius: 5px;
    border: 1px solid #DFDEDE;
    line-height: 50px;
    margin: 10px 0;
    padding: 5px 10px;
}
.flexBox {
    display: flex;
    justify-content: space-between;
    height: 50px;
}
.el-input {
    width: 200px;
}
.pageDiv {
    display: flex;
    justify-content: end;
    margin: 8px 20px;
    background-color: #fff;
}
</style>