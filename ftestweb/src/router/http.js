import axios from "axios";
import { ElMessage } from 'element-plus';
import {showLoading,hideLoading} from './loading'

//创建实例
const instance = axios.create({
    // baseURL: 'http://127.0.0.1:8000',
    baseURL: process.env.VUE_APP_BASE_URL,
    timeout: 100000,
});




instance.interceptors.request.use(config=>{
    const token = window.sessionStorage.getItem('token');
     showLoading();
    if(token) {
        config.headers = {
            'Authorization': 'token' + ' '+ token
        };
    }
    return config;
},error =>{
    hideLoading();
    return Promise.reject(error)
});
instance.interceptors.response.use(response => {
    // console.log('响应拦截处理');
    hideLoading();
    if(response.data.code != 200) {
        const a = 123; // 这里应根据后端返回消息显示
    }
    hideLoading();
    return response
}, error => {
    // 处理响应错误（catch）
    ElMessage.error('请求服务端接口错误：' + error.message);
    hideLoading();
    return Promise.reject(error);
});

export default instance //导出 其他地方可以引用