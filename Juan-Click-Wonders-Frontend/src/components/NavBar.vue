<template>
    <div>
        <header class="bg-gray-900 text-white">
            <div class="w-full px-4">
                <div class="flex items-center justify-between">
                    <div class="!h-full !py-2 !mx-25">
                        <a href="/">
                            <img src="/icon.png" alt="Logo" class="!h-16 !w-16 object-contain">
                        </a>
                    </div>
                    <!-- Search Bar -->
                    <div v-if="!isAuthPage" class="flex-1 max-w-7xl mx-4 relative flex items-center">
                        <div class="w-full relative">
                            <input type="text" placeholder="Search Products"
                                v-model="searchQuery"
                                @keyup.enter="handleSearch"
                                class="w-full !py-3 !pl-5 !pr-12 bg-white rounded-full text-gray-800 focus:outline-none" />
                            <button 
                                @click="handleSearch"
                                class="absolute right-0 top-0 h-full !px-4 flex items-center hover:text-gray-600 cursor-pointer">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                </svg>
                            </button>
                        </div>
                        <div class="!ml-4">
                            <!-- Cart Icon -->
                            <div v-if="isLoggedIn">
                                <router-link to="/cart" class="flex items-center relative">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                                        stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                                    </svg>
                                    <span v-if="cartCount > 0" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                                        {{ cartCount }}
                                    </span>
                                </router-link>
                            </div>
                            <div v-else>
                                <router-link to="/auth/login" class="flex items-center relative">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                                        stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                                    </svg>
                                </router-link>
                            </div>
                        </div>
                    </div>
                    <div>
                        <a v-if="!isLoggedIn" href="/auth/login/" class="font-medium hover:text-gray-300 !mx-25">LOGIN</a>
                        <a v-else  href="/profile/" class="font-medium hover:text-gray-300 !mx-25">PROFILE</a>
                    </div>
                </div>
                <nav class="flex justify-end !py-2 !mx-25">
                    <div class="flex !space-x-8 font-medium">
                        <a href="/" class="hover:text-gray-300">HOME</a>
                        <a href="/product_list/" class="hover:text-gray-300">SHOP</a>
                        <a href="/about/" class="hover:text-gray-300">ABOUT</a>
                    </div>
                </nav>
            </div>
        </header>
    </div>
</template>

<script>
import { useRoute } from "vue-router";
import { computed, ref, onMounted, onUnmounted } from "vue";

export default {
  setup() {
      const route = useRoute();
      const isAuthPage = computed(() => ["login", "register", "forgot-password"].includes(route.name));
      const cartCount = ref(0);

      const updateCartCount = () => {
          if (localStorage.getItem('isAuthenticated')) {
              const count = localStorage.getItem('cartCount');
              cartCount.value = count ? parseInt(count) : 0;
          } else {
              cartCount.value = 0;
              localStorage.removeItem('cartCount');
          }
      };

      onMounted(() => {
          updateCartCount();
          // Listen for storage events from other tabs/windows
          window.addEventListener('storage', updateCartCount);
          // Listen for custom events from the same window
          window.addEventListener('cart-updated', updateCartCount);
          // Listen for auth state changes
          window.addEventListener('auth-state-changed', updateCartCount);
      });

      onUnmounted(() => {
          window.removeEventListener('storage', updateCartCount);
          window.removeEventListener('cart-updated', updateCartCount);
          window.removeEventListener('auth-state-changed', updateCartCount);
      });

      return { isAuthPage, cartCount };
  },
  computed: {
    isLoggedIn() {
        return localStorage.getItem('isAuthenticated') === 'true';
    }
  },
  data() {
        return {
            searchQuery: '',
        }
  },
  methods: {
      handleSearch() {
          // If search is empty or only whitespace, remove search parameter
          if (!this.searchQuery || !this.searchQuery.trim()) {
              this.$router.push({
                  path: '/product_list'
              });
          } else {
              this.$router.push({
                  path: '/product_list',
                  query: { search: this.searchQuery.trim() }
              });
          }
      },
      updateCartCount() {
          if (localStorage.getItem('isAuthenticated')) {
              const count = localStorage.getItem('cartCount');
              this.cartCount = count ? parseInt(count) : 0;
          } else {
              this.cartCount = 0;
              localStorage.removeItem('cartCount');
          }
      }
  },
};
</script>

