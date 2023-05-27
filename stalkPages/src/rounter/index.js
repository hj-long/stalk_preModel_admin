import { createRouter, createWebHashHistory } from "vue-router";
import { ElMessage, componentSizeMap } from 'element-plus'

const routes = [
    {
        path: "/hello",
        name: "HelloWorld",
        component: () => import("../components/HelloWorld.vue"),
    },
    {
        path: "/login",
        name: "userLogin",
        component: () => import("../components/userLogin.vue"),
    },
    {
        path: "/",
        name: "admin_page",
        component: () => import("../components/AdminPage.vue"),
        // 路由守卫
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem("token")) {
                next();
            } else {
                ElMessage.error('请先登录')
                next("/login");
            }
        },
        // 默认加载的子路由
        redirect: "/main",
        // 子路由
        children: [
            {
                path: "main",
                name: "main",
                // 渲染位置指定
                components: {main: () => import("../components/MainPage/index.vue")},
            },
            {
                path: 'data',
                name: 'data',
                components: {main: () => import("../components/DataPage/index.vue")},
            },
            {
                path: 'echart',
                name: 'echart',
                components: {main: () => import("../components/EchartPage/index.vue")},
            },
            {
                path: 'useradmin',
                name: 'useradmin',
                components: {main: () => import("../components/UserAdmin/index.vue")},
            },
        ],
    },
];

export const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;