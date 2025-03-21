import { createRouter, createWebHistory } from 'vue-router'

const routes =[
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
      path: '/reset-password/:uidb64/:token',
      name: 'reset-password',
      component: () => import('../views/ResetPassword.vue'),
      props: true
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
      path: '/profile/password',
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
    {
      path: '/cart',
      name: 'cart',
      component: () => import('../views/ShoppingCart.vue'),
    },
  ];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router
