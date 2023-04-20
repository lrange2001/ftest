import { createRouter, createWebHistory } from 'vue-router'
import Serverdetails from "@/components/Serverdetails";
import IndexLayout from "@/server/IndexLayout";
// import NProgress from "nprogress"; // 导入 nprogress模块


// import "nprogress/nprogress.css"; // 导入样式，否则看不到效果

const routes = [ //路由对象
  {
    path: '/',
    name: '仪表盘',
    component: IndexLayout,
    icon: 'Histogram'
  },
    {
      path: '/server', //url
      name: '资产管理', //路由名称
      component: IndexLayout, //引用组件
      icon: 'Operation',
      children: [
        {
          path: '/server/Serverdetails',
          name: '服务器管理',
          component: Serverdetails
        }
      ]
    },
  {
    path: '/app', //url
    name: '应用管理', //路由名称
    component: IndexLayout, //引用组件
    icon: 'Menu',
    children: [
      {
        path: '/app/describe',
        component: ()=> import('../app/AppDescribe'),
        name: '自定义应用'
      },
      {
        path: '/app/describe',
        component: ()=> import('../app/AppDescribe'),
        name: 'GIT应用发布'
      }
    ]
  },
  {
    path: '/knowledge_ase',
    name: '文档管理',
    component: IndexLayout,
    icon: 'Document',
    children: [
      {
        path: '/knowledge_ase/txt',
        component: ()=> import('../docapp/DocApp'),
        name: '共享文档'
      }
    ]
  },
  {
    path: '/login', //url
    name: '登录页', //路由名称
    component: ()=> import('../components/UserLogin') //引用组件
  }

]
//创建路由实例并传递上面定义的路由对象
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), //路由模式
  routes
});


// 添加导航守卫
router.beforeEach((to, from, next) => {
  // 如果用户访问登录页，直接放行
  if(to.path == '/login') {
    return next()
  }
  // 从sessionStorage获取token值
  const token = window.sessionStorage.getItem('token');
  // 如果没有获取到token值，跳转到登录页
  if (!token) {
    return next('/login')
  }
  // 正常跳转
  // NProgress.start();
  next()

});
router.afterEach(() => {
// NProgress.done(); //完成进度条

});
export default router