import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes =[
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Homepage.vue'),
    },
    {
      path: '/auth/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/auth/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/auth/forgot-password',
      name: 'forgot-password',
      component: () => import('../views/ForgotPassword.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfilePage.vue'),
    },
    {
      path: '/profile/edit',
      name: 'profile-edit',
      component: () => import('../views/EditProfile.vue'),
    },
    {
      path: '/profile/update-password',
      name: 'update-password',
      component: () => import('../views/UpdatePassword.vue'),
    },
    {
      path: '/product_list',
      name: 'product_list',
      component: () => import('../views/ProductList.vue'),
    },
    {
      path: '/product/:id',
      name: 'product',
      component: () => import('../views/ProductDetail.vue'),
      props: true,
    },
    
  ];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router
