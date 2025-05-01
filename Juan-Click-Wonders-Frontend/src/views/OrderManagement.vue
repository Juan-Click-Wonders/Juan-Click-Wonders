<template>
    <div class="p-6 font-sans max-w-screen-xl mx-auto">
        <h1 class="text-2xl font-bold mb-6">Order Management</h1>

        <div v-if="isLoading" class="flex justify-center items-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-yellow-600"></div>
        </div>

        <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            <p>{{ error }}</p>
            <button @click="fetchOrders" class="mt-2 bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded">
                Try Again
            </button>
        </div>

        <div v-else-if="orders.length === 0" class="bg-white rounded-lg shadow p-8 text-center">
            <p class="text-gray-600 mb-4">You don't have any orders yet.</p>
            <router-link to="/product_list" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-yellow-600 hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                Start Shopping
            </router-link>
        </div>

        <div v-else class="bg-white rounded-lg shadow overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full whitespace-nowrap">
                    <thead>
                        <tr class="bg-gray-100 text-center">
                            <th class="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                Order ID
                            </th>
                            <th class="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                Product
                            </th>
                            <th class="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                Price
                            </th>
                            <th class="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                Quantity
                            </th>
                            <th class="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                Total
                            </th>
                            <th class="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                Status
                            </th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr v-for="order in orders" :key="order.order_id" class="hover:bg-gray-50 transition-colors text-center">
                            <td class="px-6 py-4">#{{ order.order_id }}</td>
                            <td class="px-6 py-4 whitespace-normal break-words max-w-[200px] text-left">
                                {{ order.product.name }}
                            </td>
                            <td class="px-6 py-4">₱{{ formatPrice(order.product.price) }}</td>
                            <td class="px-6 py-4">{{ order.quantity }}</td>
                            <td class="px-6 py-4 font-semibold">₱{{ formatPrice(order.product.price * order.quantity) }}</td>
                            <td class="px-6 py-4">
                                <span :class="getStatusClass(order.status)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full min-w-15 justify-center">
                                    {{ order.status }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    withCredentials: true
});

export default {
    name: 'OrderManagement',
    data() {
        return {
            orders: [],
            isLoading: true,
            isAuthenticated: false,
            error: null
        };
    },
    methods: {
        async checkAuth() {
            try {
                await api.post('/api/auth/authenticate/');
                this.isAuthenticated = true;
                return true;
            } catch (error) {
                this.isAuthenticated = false;
                this.$router.push('/auth/login');
                return false;
            }
        },
        async fetchOrders() {
            this.isLoading = true;
            this.error = null;
            
            try {
                const response = await api.get('/orders/');
                this.orders = response.data;
            } catch (error) {
                if (error.response?.status === 401) {
                    this.$router.push('/auth/login');
                } else {
                    this.error = 'Failed to load orders. Please try again.';
                }
            } finally {
                this.isLoading = false;
            }
        },
        formatPrice(price) {
            return price.toLocaleString('en-PH', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        },
        getStatusClass(status) {
            switch(status) {
                case 'Paid':
                    return 'bg-green-100 text-green-800';
                case 'To Ship':
                    return 'bg-blue-100 text-blue-800';
                case 'To Receive':
                    return 'bg-yellow-100 text-yellow-800';
                case 'Delivered':
                    return 'bg-purple-100 text-purple-800';
                default:
                    return 'bg-gray-100 text-gray-800';
            }
        },
        async fetchCart() {
            if (!this.isAuthenticated) return;
            try {
                this.isLoading = true;
                const cartResponse = await api.get('/cart/');
                if (cartResponse.data && cartResponse.data.length > 0) {
                    this.cart = cartResponse.data[0];
                    this.cartItems = [];
                    this.unavailableItems = [];

                    let totalItems = 0;

                    // Use Promise.all to fetch all products in parallel
                    const productPromises = this.cart.cart_items.map(async (item) => {
                        try {
                            const productResponse = await api.get(`/products/${item.product}`);
                            return {
                                id: item.id,
                                quantity: item.quantity,
                                product: {
                                    ID: item.product,
                                    Name: productResponse.data.name,
                                    Price: productResponse.data.price,
                                    Image: productResponse.data.image_url,
                                    Inventory_Level: productResponse.data.stock
                                }
                            };
                        } catch (error) {
                            console.error(`Error fetching product ${item.product}:`, error);
                            this.unavailableItems.push(item.id);
                            return null;
                        }
                    });

                    const results = await Promise.all(productPromises);
                    this.cartItems = results.filter(item => item !== null);

                    // Count unique items instead of total quantity
                    const uniqueItemCount = this.cartItems.length;

                    // Set cart count to number of unique items
                    localStorage.setItem('cartCount', uniqueItemCount.toString());
                    window.dispatchEvent(new Event('cart-updated'));

                    if (this.unavailableItems.length > 0) {
                        this.message = `${this.unavailableItems.length} item${this.unavailableItems.length > 1 ? 's' : ''} in your cart ${this.unavailableItems.length > 1 ? 'are' : 'is'} no longer available.`;
                        this.messageType = 'error';
                    } else {
                        this.message = null;
                    }
                } else {
                    this.cartItems = [];
                    this.cart = null;
                    this.message = null;
                    localStorage.setItem('cartCount', '0');
                    window.dispatchEvent(new Event('cart-updated'));
                }
                this.isLoading = false;
            } catch (error) {
                console.error('Error fetching cart:', error);
                this.cartItems = [];
                this.cart = null;
                this.message = 'There was an error loading your cart. Please try again.';
                this.messageType = 'error';
                this.isLoading = false;
                if (error.response && error.response.status === 401) {
                    this.isAuthenticated = false;
                    localStorage.removeItem('cartCount');
                    this.$router.push('/auth/login');
                }
            }
        }
    },
    async created() {
        const isAuth = await this.checkAuth();
        if (isAuth) {
            await this.fetchCart();            
            await this.fetchOrders();
        }
    }
};
</script>