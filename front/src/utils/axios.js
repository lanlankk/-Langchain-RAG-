/**
 * axios 全局配置
 * 自动在请求头中添加 JWT token
 */

import axios from 'axios';
import { useUserStore } from '../store/user';

// 创建 axios 实例
const instance = axios.create({
  baseURL: '', // 使用相对路径，通过 Vite 代理
  timeout: 30000,
});

// 请求拦截器：自动添加 token
instance.interceptors.request.use(
  (config) => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('jwt_token');
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器：处理 token 过期
instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 如果 token 过期或无效，跳转到登录页
    if (error.response?.status === 401) {
      localStorage.removeItem('jwt_token');
      const userStore = useUserStore();
      userStore.isLogin = false;
      userStore.token = '';
      userStore.userInfo = null;
      
      // 跳转到登录页
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

export default instance;