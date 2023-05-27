<script setup>
import { ref } from 'vue'
import router from '../rounter';
import axios from '../api/index.js'

const isCollapse = ref(false);

// 获取用户名
const username = localStorage.getItem('username') || 'admin';

const makeMenu = function() {
    isCollapse.value = !isCollapse.value;
}
const backLogin = function() {
    // 清除token和username
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    // 成功后返回登录页面
    router.push('/login')
}

// 进入页面时，自动加载main页面的数据

</script>

<template>
  <div class="common-layout">
    <el-container>
        <!-- 右侧标题栏 -->
      <el-aside :width="isCollapse ? '60px' : '240px'">
        <p class="titleBox">
            <span class="iconfont icon-svg-" style="font-size: 20px;"></span>
            <span class="title" :style="isCollapse ? 'font-size: 0px;' : 'font-size: 18px;margin-left:7px;'">秸秆发酵预测分析系统</span>    
        </p>
        <div class="navTitle" :style="isCollapse ? 'justify-content:center;' : ''">
            <router-link to="/main">
                <span class="icon-home iconfont"></span>
                <span :class="isCollapse ? 'petty' : 'big'">首页</span>
            </router-link>
        </div>
        <div class="navTitle" :style="isCollapse ? 'justify-content:center;' : ''">
            <router-link to="/useradmin">
                <span class="icon-shujuxitong iconfont"></span>
                <span :class="isCollapse ? 'petty' : 'big'">用户管理</span>
            </router-link>
        </div>
        <div class="navTitle" :style="isCollapse ? 'justify-content:center;' : ''">
            <router-link to="/data">
                <span class="icon-shujuchakan-05 iconfont"></span>
                <span :class="isCollapse ? 'petty' : 'big'">数据查看</span>
            </router-link>
        </div>
        <div class="navTitle" :style="isCollapse ? 'justify-content:center;' : ''">
            <router-link to="/echart">
                <span class="icon-tongjijisuan iconfont"></span>
                <span :class="isCollapse ? 'petty' : 'big'">数据分析</span>
            </router-link>
        </div>
      </el-aside>
      <el-container>
        <el-header>
            <div @click="makeMenu" class="iconMenu"><span class="iconfont icon-recovery"></span></div>
            <div class="headerBox" @click="backLogin">
                <span class="iconfont icon-zhanghaoquanxianguanli">&nbsp;&nbsp;当前用户：</span><span style="color: #409EFF;">{{ username }}</span>
                <span>&nbsp;&nbsp;&nbsp;&nbsp;</span>
                <span class="iconfont icon-tuichu logout">&nbsp;退出账号</span>
            </div>
        </el-header>
        <el-main>
            <router-view name="main"></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.common-layout {
    width: 100vw;
    height: 100vh;
}
.el-main {
    background-color: #ffffff;
}
.el-container {
    height: 100%;
}
.el-aside {
    background-color: #545c64;
    color: #fff;
    padding: 15px 10px 10px 20px;
}
.titleBox {
    display: flex;
    align-items: center;
    justify-content: center;
}
.title {
    font-weight: bold;
    text-align: center;
    height: 30px;
    line-height: 30px;
}
.el-header {
    background-color: #545c6450;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.iconMenu:hover,.navTitle:hover, .logout:hover {
    cursor: pointer;
    color: #409EFF;
}
.headerBox span {
    margin-left: 5px;
}
.big {
    font-size: 16px;
    margin-left:7px;
}
.petty {
    font-size: 0px;
    text-align: center;
}
.navTitle {
    display: flex;
    align-items: center;
    margin-top: 20px;
}
</style>