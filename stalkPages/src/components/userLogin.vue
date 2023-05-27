<script setup>
import { ref } from 'vue'
import userEnroll from './userEnroll.vue';
import { router } from '../rounter/index.js'
import axios from '../api/index.js'
import { ElMessage } from 'element-plus'

const username = ref('');
const password = ref('');
const showLogin = ref(true);

const register = function() {
    showLogin.value = !showLogin.value;
    password.value = '';
}

const login = function() {
    if(username.value == '' || password.value == '') {
        alert('用户名或密码不能为空');
        return;
    }
    // 发送请求
    axios.post('user/login/', {
        username: username.value,
        password: password.value
    }).then(res => {
        if(res.msg == '登录成功') {
            // 登录成功
            // 保存token
            localStorage.setItem('token', res.data.token);
            localStorage.setItem('username', res.data.username);
            // 跳转到首页
            console.log('成功：', res);
            ElMessage({
                message: '登录成功',
                type: 'success',
            });
            router.push('/');
        } else {
            console.log('失败：', res);
            ElMessage({
                message: res.msg + '，用户名或密码错误',
                type: 'warning',
            });
        }
    }).catch(err => {
        console.log(err);
    })

}


</script>

<template>
    <div class="loginBox">
        <div class="title">秸秆发酵数据预测管理系统</div>
        <div class="userForm" v-show="showLogin">
            <div class="usersname">
                <span class="iconfont icon-yonghu">&nbsp;用户名：</span>
                <input type="text" placeholder="请输入用户名" v-model="username">
            </div>
            <div class="password">
                <span class="iconfont icon-ziyuanxhdpi">&nbsp;密&nbsp;&nbsp;&nbsp;码：</span>
                <input type="password" placeholder="请输入密码" v-model="password">
            </div>
            <div class="btn">
                <el-button type="success" @click="login">登录</el-button>
                <el-button type="info" plain @click="register">注册</el-button>
            </div>
        </div>
        <div class="userForm" v-show="!showLogin">
            <userEnroll @backPage="register"></userEnroll>
        </div>
    </div>
</template>

<style scoped>
.loginBox {
    width: 500px;
    height: 300px;
    background-color: #fff;
    border-radius: 8px;
    border: 1px solid #63c3e9;
    /* 居中 */
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}
.title {
    width: 100%;
    height: 50px;
    line-height: 50px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    border-bottom: 1px solid #52d0f0;
} 
.usersname,.password {
    width: 100%;
    height: 50px;
    line-height: 50px;
    margin-top: 20px;
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

