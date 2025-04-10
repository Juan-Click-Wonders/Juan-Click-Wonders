<template>
    <div class="bg-gray-50 min-h-screen pb-16">
        <!-- Loading State -->
        <div v-if="loading" class="container mx-auto px-4 py-12 h-screen flex items-center justify-center">
            <div class="text-center">
                <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-yellow-500 mx-auto"></div>
                <p class="text-gray-600 mt-6 text-lg">Loading product details...</p>
            </div>
        </div>

        <div v-else-if="!product" class="container mx-auto px-4 py-12 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="text-xl font-bold text-gray-700 mb-2">Product Not Found</h3>
            <p class="text-gray-600 mb-6">The product you're looking for could not be found</p>
            <router-link to="/product_list" class="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold px-6 py-2 rounded-lg transition-colors duration-200">
                Browse Products
            </router-link>
        </div>

        <div v-else>
            <!-- Breadcrumb Navigation -->
            <div class="bg-white border-b border-gray-200">
                <div class="container mx-auto px-4 py-3">
                    <div class="flex items-center text-sm text-gray-600">
                        <router-link to="/" class="hover:text-yellow-600 transition-colors">Home</router-link>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mx-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                        <router-link to="/product_list" class="hover:text-yellow-600 transition-colors">Products</router-link>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mx-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                        <span class="text-gray-800 font-medium truncate max-w-xs">{{ product.name }}</span>
                    </div>
                </div>
            </div>

            <!-- Product Content -->
            <div class="container mx-auto px-4 py-8">
                <div class="bg-white rounded-xl shadow-md overflow-hidden">
                    <div class="flex flex-col lg:flex-row">
                        <!-- Product Image -->
                        <div class="lg:w-1/2 p-8 bg-white">
                            <div class="relative h-96 bg-white rounded-lg flex items-center justify-center p-4 mb-3 mx-auto max-w-xl">
                                <img v-if="product.image_url" :src="getImageUrl(product.image_url)" :alt="product.name" 
                                    class="max-h-full max-w-full object-contain transition-transform duration-500 hover:scale-110">
                                <div v-else class="w-full h-full flex items-center justify-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                
                                <!-- Stock Badge -->
                                <div v-if="product.stock === 0" class="absolute top-3 left-3 bg-red-500 text-white text-xs font-bold uppercase px-3 py-1 rounded-lg">
                                    Out of Stock
                                </div>
                                <div v-else-if="product.stock < 5" class="absolute top-3 left-3 bg-orange-500 text-white text-xs font-bold uppercase px-3 py-1 rounded-lg">
                                    Low Stock: {{ product.stock }} left
                                </div>
                            </div>
                        </div>

                        <!-- Product Details -->
                        <div class="lg:w-1/2 p-8">
                            <div class="flex flex-col h-full">
                                <!-- Category & Brand -->
                                <div class="flex justify-between items-start mb-3">
                                    <span class="bg-yellow-100 text-yellow-600 text-xs font-medium px-2.5 py-0.5 rounded-full">
                                        {{ categoryName }}
                                    </span>
                                    <span class="text-gray-600 text-sm">Brand: <span class="font-medium">{{ product.brand }}</span></span>
                                </div>

                                <!-- Product Name -->
                                <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ product.name }}</h1>

                                <!-- Price -->
                                <div class="flex items-baseline mb-6">
                                    <span class="text-3xl font-bold text-gray-900">₱{{ product.price.toLocaleString() }}</span>
                                    <span class="ml-2 text-sm text-gray-500">{{ product.sold_products }} units sold</span>
                                </div>

                                <!-- Description -->
                                <div class="bg-gray-50 rounded-lg p-4 mb-6">
                                    <h3 class="font-semibold text-gray-800 mb-2">Description</h3>
                                    <p class="text-gray-700">{{ product.description || 'No description available for this product.' }}</p>
                                </div>

                                <!-- Specifications -->
                                <div class="border-t border-gray-200 pt-6 mb-6">
                                    <h3 class="font-semibold text-gray-800 mb-3">Specifications</h3>
                                    <div class="grid grid-cols-2 gap-4">
                                        <div class="flex flex-col">
                                            <span class="text-gray-600 text-sm">Category</span>
                                            <span class="font-medium">{{ categoryName }}</span>
                                        </div>
                                        <div class="flex flex-col">
                                            <span class="text-gray-600 text-sm">Brand</span>
                                            <span class="font-medium">{{ product.brand }}</span>
                                        </div>
                                        <div class="flex flex-col">
                                            <span class="text-gray-600 text-sm">Stock</span>
                                            <span class="font-medium">{{ product.stock }} units</span>
                                        </div>
                                        <div class="flex flex-col">
                                            <span class="text-gray-600 text-sm">Units Sold</span>
                                            <span class="font-medium">{{ product.sold_products }}</span>
                                        </div>
                                    </div>
                                </div>

                                <!-- Add to Cart -->
                                <div class="mt-auto">
                                    <div class="flex flex-col sm:flex-row sm:items-center gap-4">
                                        <div class="flex items-center bg-white border border-gray-300 rounded-lg overflow-hidden">
                                            <button @click="decreaseQuantity" 
                                                class="px-4 py-2 text-gray-600 hover:bg-gray-100 transition-colors disabled:opacity-50"
                                                :disabled="quantity <= 1 || product.stock === 0">
                                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                                                </svg>
                                            </button>
                                            <span class="w-12 text-center font-medium">{{ quantity }}</span>
                                            <button @click="increaseQuantity" 
                                                class="px-4 py-2 text-gray-600 hover:bg-gray-100 transition-colors disabled:opacity-50"
                                                :disabled="quantity >= product.stock || product.stock === 0">
                                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                                                </svg>
                                            </button>
                                        </div>
                                        <button @click="addToCart" 
                                            class="flex-1 bg-black text-white py-3 px-6 rounded-lg font-semibold hover:bg-gray-800 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                                            :disabled="product.stock === 0">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                                            </svg>
                                            <span>{{ product.stock === 0 ? 'Out of Stock' : 'Add to Cart' }}</span>
                                        </button>
                                    </div>
                                    <p v-if="!isLoggedIn" class="text-center text-sm text-gray-600 mt-3">
                                        <router-link to="/auth/login/" class="text-yellow-600 hover:underline">Log in</router-link> to add items to your cart
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    withCredentials: true
});

export default {
    data() {
        return {
            product: null,
            categories: [],
            ratings: [],
            quantity: 1,
            cart: null,
            loading: true
        };
    },
    computed: {
        categoryName() {
            if (!this.product) return 'Loading...';
            return this.product.category_name || 'Unknown Category';
        },
        isLoggedIn() {
            return localStorage.getItem('isAuthenticated') === 'true';
        }
    },
    methods: {
        getImageUrl(imagePath) {
            if (!imagePath) return null;
            return imagePath;
        },
        formatDate(dateString) {
            return new Date(dateString).toLocaleDateString();
        },
        async fetchCategories() {
            try {
                const response = await api.get("/category");
                this.categories = response.data;
            } catch (error) {
                console.error("Error fetching categories:", error);
            }
        },
        async fetchProduct() {
            try {
                this.loading = true;
                const productId = this.$route.params.id;
                const response = await api.get(`/products/${productId}`);
                this.product = response.data;
                this.loading = false;
            } catch (error) {
                console.error("Error fetching product:", error);
                this.loading = false;
            }
        },
        increaseQuantity() {
            if (this.quantity < this.product.stock) this.quantity++;
        },
        decreaseQuantity() {
            if (this.quantity > 1) this.quantity--;
        },
        async addToCart() {
            if (!this.isLoggedIn) {
                this.$router.push('/auth/login/');
                return;
            }

            try {
                const cartResponse = await api.get('/cart/');
                const cart = cartResponse.data[0]; 

                const existingItem = cart.cart_items.find(item => item.product === this.product.product_id);
                
                // Calculate the quantity difference for the cart count
                let quantityToAdd = this.quantity;
                
                // If item exists, we're only adding the difference in quantity
                if (existingItem) {
                    quantityToAdd = this.quantity - existingItem.quantity;
                    if (quantityToAdd < 0) quantityToAdd = 0; // Prevent negative values
                }
                
                await api.post(`/cart/${cart.cart_id}/items/`, {
                    product: this.product.product_id,
                    quantity: this.quantity
                });

                // Update total item count
                const currentCount = parseInt(localStorage.getItem('cartCount') || '0');
                localStorage.setItem('cartCount', (currentCount + quantityToAdd).toString());
                window.dispatchEvent(new Event('cart-updated'));

                // Redirect to cart page
                this.$router.push('/cart');
            } catch (error) {
                console.error('Error adding to cart:', error);
                if (error.response && error.response.status === 401) {
                    this.$router.push('/auth/login/');
                }
            }
        }
    },
    created() {
        this.fetchCategories();
        this.fetchProduct();
    },
    watch: {
        // Reset and refetch when the route changes (for navigating between products)
        '$route.params.id'() {
            this.quantity = 1;
            this.product = null;
            this.fetchProduct();
        }
    }
};
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css");

/* Add animation for placeholder loading */
@keyframes pulse {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.8;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
