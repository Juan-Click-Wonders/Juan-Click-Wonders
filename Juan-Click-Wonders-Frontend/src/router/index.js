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
    {
      path: '/orders',
      name: 'orders',
      component: () => import('../views/OrderManagement.vue'),
    },
    {
      path: '/wishlist',
      name: 'wishlist',
      component: () => import('../views/WishlistView.vue'),
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminPanel.vue'),
    },
    // 404 catch-all route - must be the last route
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFound.vue'),
    },
  ];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const restrictedForAdminRoutes = [
  'product_list',
  'product',
  'cart',
  'wishlist'
];

// Global navigation guard
router.beforeEach(async (to, from, next) => {
  // Check if user is authenticated
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  
  if (isAuthenticated) {
    // Check if the user is an admin
    try {
      const response = await fetch('http://127.0.0.1:8000/admins/check/', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        const isAdmin = data.is_admin;
        
        // If user is admin and trying to access a restricted route, redirect to 404
        if (isAdmin && restrictedForAdminRoutes.includes(to.name)) {
          next({ name: 'not-found' });
          return;
        }
      }
    } catch (error) {
      console.error('Error checking admin status:', error);
    }
  }
  
  // Continue navigation as normal for non-admin users
  next();
});

export default router
