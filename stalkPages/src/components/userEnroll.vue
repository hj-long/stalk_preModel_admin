<script setup>
import { ref } from 'vue'
import axios from '../api/index.js'


const username = ref('');
const password = ref('');
const mailAddress = ref('');

// 接收父组件的函数
const emit = defineEmits(['backPage']);

const backPage = function() {
    username.value = '';
    password.value = '';
    mailAddress.value = '';
    emit('backPage');
}

const toEnroll = function() {
    if(username.value == '' || password.value == '') {
        alert('用户名或密码不能为空!');
        return;
    }
    // 发送请求
    axios.post('user/register/', {
        username: username.value,
        password: password.value,
        mailAddress: mailAddress.value
    }).then(res => {
        if(res.msg == '注册成功') {
            // 注册成功
            console.log('成功：', res);
            alert('注册成功');
            emit('backPage');
        } else {
            console.log('失败：', res);
            alert(res.msg + '，请重新注册!');
        }
    }).catch(err => {
        console.log(err);
    })
}
</script>

<template>
    <div class="usersname">
        <span class="iconfont icon-yonghu">&nbsp;用户名：</span><input type="text" placeholder="请输入用户名" v-model="username">
    </div>
    <div class="password">
        <span class="iconfont icon-ziyuanxhdpi">&nbsp;密&nbsp;&nbsp;&nbsp;&nbsp;码：</span><input type="text" placeholder="请输入密码" v-model="password">
    </div>
    <div class="password">
        <span class="iconfont icon-ziyuanxhdpi">&nbsp;邮&nbsp;&nbsp;&nbsp;&nbsp;箱：</span><input type="text" placeholder="请输入邮箱" v-model="mailAddress">
    </div>
    <div class="btn">
        <el-button type="success" @click="toEnroll">确认注册</el-button>
        <el-button type="info" plain @click="backPage">返回</el-button>
    </div>
</template>

<style scoped>
.usersname,.password {
    width: 100%;
    height: 50px;
    line-height: 50px;
    text-align: center;
}
.usersname input,.password input {
    width: 200px;
    height: 30px;
    border: 1px solid #e6e4e4;
    border-radius: 5px;
    outline: none;
    padding-left: 10px;
}

.usersname span,.password span {
    display: inline-block;
    width: 100px;
    text-align: right;
}
.btn {
    width: 100%;
    height: 50px;
    line-height: 50px;
    margin-top: 20px;
    text-align: center;
}
.el-button {
    width: 100px;
}
</style>