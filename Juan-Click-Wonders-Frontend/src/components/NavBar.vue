<template>
    <div>
        <header class="bg-gradient-to-r from-gray-900 to-gray-800 text-white shadow-md">
            <div class="container mx-auto px-4 py-2">
                <!-- Desktop Navbar -->
                <div class="hidden md:flex items-center justify-between">
                    <!-- Logo -->
                    <div class="flex items-center">
                        <router-link to="/" class="flex items-center">
                            <img src="/icon.png" alt="Logo" class="h-12 w-12 object-contain">
                            <span class="ml-2 text-xl font-bold text-yellow-500">Juan Click Wonders</span>
                        </router-link>
                    </div>

                    <!-- Navigation -->
                    <div class="flex space-x-6 font-medium">
                        <router-link to="/"
                            class="py-4 px-2 border-b-2 border-transparent hover:border-yellow-500 hover:text-yellow-500 transition-colors duration-300">HOME</router-link>
                        <router-link to="/product_list"
                            class="py-4 px-2 border-b-2 border-transparent hover:border-yellow-500 hover:text-yellow-500 transition-colors duration-300">SHOP</router-link>
                        <router-link to="/about"
                            class="py-4 px-2 border-b-2 border-transparent hover:border-yellow-500 hover:text-yellow-500 transition-colors duration-300">ABOUT</router-link>
                    </div>

                    <!-- Search Bar -->
                    <div v-if="!isAuthPage" class="flex-1 max-w-md mx-4 relative">
                        <div class="relative">
                            <input type="text" placeholder="Search Products" v-model="searchQuery"
                                @keyup.enter="handleSearch"
                                class="w-full py-2 pl-10 pr-4 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 placeholder-gray-400" />
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <!-- User Actions -->
                    <div class="flex items-center space-x-4">
                        <!-- Cart -->
                        <router-link to="/cart" class="relative p-2 hover:text-yellow-500 transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            <span v-if="cartCount > 0"
                                class="absolute -top-1 -right-1 bg-yellow-500 text-black text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                                {{ cartCount }}
                            </span>
                        </router-link>

                        <!-- User -->
                        <div v-if="!authState" class="flex items-center">
                            <router-link to="/auth/login"
                                class="bg-yellow-500 hover:bg-yellow-600 text-gray-900 !text-gray-900 font-medium py-2 px-4 rounded-lg transition-colors"
                                style="color: #1F2937 !important;">
                                LOGIN
                            </router-link>
                        </div>
                        <div v-else class="relative" @click="toggleUserMenu" ref="userMenuContainer">
                            <button class="flex items-center focus:outline-none">
                                <div
                                    class="h-8 w-8 rounded-full bg-yellow-500 flex items-center justify-center text-gray-900 font-bold">
                                    {{ userInitial }}
                                </div>
                                <span class="ml-2 text-sm hidden lg:inline">{{ userName }}</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>
                            <div v-show="showUserMenu"
                                class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                                <router-link to="/profile"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                    Your Profile
                                </router-link>
                                <router-link to="/orders"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                    Your Orders
                                </router-link>
                                <router-link to="/wishlist"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                    Your Wishlist
                                </router-link>
                                <router-link v-if="isAdmin" to="/admin"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                    Admin Panel
                                </router-link>
                                <div class="border-t border-gray-200"></div>
                                <a href="#" @click.prevent="logout"
                                    class="block px-4 py-2 text-sm text-red-600 hover:bg-gray-100">
                                    Logout
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Mobile Navbar -->
                <div class="md:hidden">
                    <div class="flex items-center justify-between py-2">
                        <!-- Logo and Menu Button -->
                        <div class="flex items-center">
                            <button @click="toggleMobileMenu" class="mr-2 text-white focus:outline-none">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round"
                                        stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                            <router-link to="/" class="flex items-center">
                                <img src="/icon.png" alt="Logo" class="h-10 w-10 object-contain">
                                <span class="ml-2 text-lg font-bold text-yellow-500">Juan Click</span>
                            </router-link>
                        </div>

                        <!-- Cart and User -->
                        <div class="flex items-center space-x-4">
                            <router-link to="/cart" class="relative p-1">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                                </svg>
                                <span v-if="cartCount > 0"
                                    class="absolute -top-1 -right-1 bg-yellow-500 text-black text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                                    {{ cartCount }}
                                </span>
                            </router-link>
                            <router-link v-if="!authState" to="/auth/login"
                                class="py-1 px-3 bg-yellow-500 text-gray-900 !text-gray-900 rounded-lg text-sm font-medium"
                                style="color: #1F2937 !important;">
                                LOGIN
                            </router-link>
                            <div v-else
                                class="h-8 w-8 rounded-full bg-yellow-500 flex items-center justify-center text-gray-900 font-bold"
                                @click="toggleUserMenu">
                                {{ userInitial }}
                            </div>
                        </div>
                    </div>

                    <!-- Mobile Menu -->
                    <div v-show="showMobileMenu" class="pt-2 pb-4 border-t border-gray-700">
                        <!-- Search -->
                        <div v-if="!isAuthPage" class="px-2 mb-3">
                            <div class="relative">
                                <input type="text" placeholder="Search Products" v-model="searchQuery"
                                    @keyup.enter="handleSearch"
                                    class="w-full py-2 pl-10 pr-4 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 placeholder-gray-400" />
                                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none"
                                        viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>
                                </div>
                            </div>
                        </div>

                        <!-- Mobile Navigation -->
                        <div class="space-y-1 px-2">
                            <router-link to="/" @click="showMobileMenu = false"
                                class="block px-3 py-2 rounded-md hover:bg-gray-700 transition-colors">
                                HOME
                            </router-link>
                            <router-link to="/product_list" @click="showMobileMenu = false"
                                class="block px-3 py-2 rounded-md hover:bg-gray-700 transition-colors">
                                SHOP
                            </router-link>
                            <router-link to="/about" @click="showMobileMenu = false"
                                class="block px-3 py-2 rounded-md hover:bg-gray-700 transition-colors">
                                ABOUT
                            </router-link>
                            <router-link v-if="authState" to="/profile" @click="showMobileMenu = false"
                                class="block px-3 py-2 rounded-md hover:bg-gray-700 transition-colors">
                                PROFILE
                            </router-link>
                            <router-link v-if="authState" to="/orders" @click="showMobileMenu = false"
                                class="block px-3 py-2 rounded-md hover:bg-gray-700 transition-colors">
                                YOUR ORDERS
                            </router-link>
                            <router-link v-if="authState" to="/wishlist" @click="showMobileMenu = false"
                                class="block px-3 py-2 rounded-md hover:bg-gray-700 transition-colors">
                                WISHLIST
                            </router-link>
                            <router-link v-if="authState && isAdmin" to="/admin" @click="showMobileMenu = false"
                                class="block px-3 py-2 rounded-md hover:bg-gray-700 transition-colors">
                                ADMIN PANEL
                            </router-link>
                            <a v-if="authState" href="#" @click.prevent="logout"
                                class="block px-3 py-2 rounded-md text-red-400 hover:bg-gray-700 transition-colors">
                                LOGOUT
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    </div>
</template>

<script>
import { useRoute } from "vue-router";
import { computed, ref, onMounted, onUnmounted, watch } from "vue";

export default {
    setup() {
        const route = useRoute();
        const isAuthPage = computed(() => {
            return route.path.includes('/auth/');
        });
        const cartCount = ref(0);
        const showUserMenu = ref(false);
        const showMobileMenu = ref(false);
        const userMenuContainer = ref(null);
        const authState = ref(localStorage.getItem('isAuthenticated') === 'true');
        const userName = ref(localStorage.getItem('userName') || 'User');
        const isAdmin = ref(false);

        const updateCartCount = () => {
            if (localStorage.getItem('isAuthenticated')) {
                const count = localStorage.getItem('cartCount');
                cartCount.value = count ? parseInt(count) : 0;
            } else {
                cartCount.value = 0;
                localStorage.removeItem('cartCount');
            }
        };

        const handleClickOutside = (event) => {
            if (userMenuContainer.value && !userMenuContainer.value.contains(event.target)) {
                showUserMenu.value = false;
            }
        };

        const updateAuthState = () => {
            authState.value = localStorage.getItem('isAuthenticated') === 'true';
            // Update userName when auth state changes
            userName.value = localStorage.getItem('userName') || 'User';
            console.log('Auth state updated:', authState.value, 'User name:', userName.value);

            // Check if user is admin
            if (authState.value) {
                checkAdminStatus();
            } else {
                isAdmin.value = false;
            }
        };

        const checkAdminStatus = async () => {
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
                    isAdmin.value = data.is_admin;

                    // Log admin status details
                    console.log('Admin status check:', {
                        is_admin: data.is_admin,
                        is_staff: data.is_staff,
                        is_superuser: data.is_superuser
                    });
                } else {
                    isAdmin.value = false;
                    console.log('Admin status check failed:', response.status);
                }
            } catch (error) {
                console.error('Error checking admin status:', error);
                isAdmin.value = false;
            }
        };

        onMounted(() => {
            updateCartCount();
            updateAuthState();

            // Listen for storage events from other tabs/windows
            window.addEventListener('storage', updateCartCount);
            window.addEventListener('storage', updateAuthState);
            // Listen for custom events from the same window
            window.addEventListener('cart-updated', updateCartCount);
            // Listen for auth state changes
            window.addEventListener('auth-state-changed', updateAuthState);
            window.addEventListener('auth-state-changed', updateCartCount);
            // Listen for clicks outside user menu
            document.addEventListener('click', handleClickOutside);
        });

        onUnmounted(() => {
            window.removeEventListener('storage', updateCartCount);
            window.removeEventListener('storage', updateAuthState);
            window.removeEventListener('cart-updated', updateCartCount);
            window.removeEventListener('auth-state-changed', updateCartCount);
            window.removeEventListener('auth-state-changed', updateAuthState);
            document.removeEventListener('click', handleClickOutside);
        });

        return {
            isAuthPage,
            cartCount,
            showUserMenu,
            showMobileMenu,
            userMenuContainer,
            authState,
            userName,
            isAdmin
        };
    },
    computed: {
        userInitial() {
            // Get the user's name from the reactive reference
            return this.userName.charAt(0).toUpperCase();
        }
    },
    data() {
        return {
            searchQuery: '',
        }
    },
    watch: {
        // Watch for auth state changes from external sources
        '$route': {
            handler() {
                // This route watcher no longer needs to update authState manually
                // as we now have proper event handling
            },
            immediate: true
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
            // Close mobile menu after search
            this.showMobileMenu = false;
        },
        toggleUserMenu() {
            this.showUserMenu = !this.showUserMenu;
        },
        toggleMobileMenu() {
            this.showMobileMenu = !this.showMobileMenu;
        },
        logout() {
            // Clear authentication state
            localStorage.removeItem('isAuthenticated');
            localStorage.removeItem('cartCount');
            localStorage.removeItem('userName');

            // Close menus
            this.showUserMenu = false;
            this.showMobileMenu = false;

            // Dispatch event for components listening to auth state
            window.dispatchEvent(new Event('auth-state-changed'));

            // Redirect to login
            this.$router.push('/auth/login');
        }
    }
};
</script>

<style scoped>
.router-link-active {
    color: #F59E0B;
    /* yellow-500 */
    border-color: #F59E0B;
}

@media (min-width: 768px) {
    .router-link-active {
        border-bottom-width: 2px;
    }
}
</style>
