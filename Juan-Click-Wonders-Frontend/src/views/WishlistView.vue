<template>
    <div class="bg-gray-50 min-h-screen pb-16">
        <!-- Header and Breadcrumbs -->
        <div class="bg-white border-b border-gray-200">
            <div class="container mx-auto px-4 py-6">
                <h1 class="text-3xl font-bold mb-2">Your Wishlist</h1>
                <div class="flex items-center text-sm text-gray-600">
                    <router-link to="/" class="hover:text-yellow-600 transition-colors">Home</router-link>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mx-2" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                    <span class="text-gray-800 font-medium">Wishlist</span>
                </div>
            </div>
        </div>

        <div class="container mx-auto px-4 py-8">
            <!-- Loading State -->
            <div v-if="isLoading" class="text-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-4 border-yellow-500 mx-auto"></div>
                <p class="text-gray-600 mt-4">Loading your wishlist...</p>
            </div>

            <!-- Message Display -->
            <div v-if="message" :class="[
                'mb-6 p-4 rounded-lg flex items-center',
                messageType === 'error' ? 'bg-red-100 text-red-700' :
                    messageType === 'success' ? 'bg-green-100 text-green-700' :
                        'bg-blue-100 text-blue-700'
            ]">
                <svg v-if="messageType === 'error'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <svg v-else-if="messageType === 'success'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ message }}</span>
            </div>

            <!-- Empty Wishlist State -->
            <div v-if="!isLoading && wishlistItems.length === 0"
                class="bg-white rounded-xl shadow-md overflow-hidden p-8 text-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                <h3 class="text-xl font-bold text-gray-700 mb-2">Your Wishlist is Empty</h3>
                <p class="text-gray-600 mb-6">Looks like you haven't added any products to your wishlist yet.</p>
                <router-link to="/product_list"
                    class="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold px-6 py-2 rounded-lg transition-colors duration-200 inline-flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    Explore Products
                </router-link>
            </div>

            <!-- Wishlist Content -->
            <div v-else-if="!isLoading" class="flex flex-col gap-8">
                <!-- Wishlist Items Grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    <div v-for="item in wishlistItems" :key="item.id"
                        class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                        <!-- Product Image -->
                        <div class="relative h-48 bg-white flex items-center justify-center p-6 overflow-hidden">
                            <router-link :to="`/product/${item.product.ID}`" @click="scrollToTop" class="flex items-center justify-center w-full h-full">
                                <img v-if="item.product.Image" :src="item.product.Image" :alt="item.product.Name"
                                    class="max-h-36 max-w-[80%] object-contain transition-transform duration-500 hover:scale-110">
                                <div v-else class="w-32 h-32 flex items-center justify-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-300" fill="none"
                                        viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                            </router-link>
                        </div>

                        <!-- Product Details -->
                        <div class="p-4">
                            <router-link :to="`/product/${item.product.ID}`" @click="scrollToTop"
                                class="text-lg font-semibold hover:text-yellow-600 transition-colors line-clamp-2 h-14">
                                {{ item.product.Name }}
                            </router-link>
                            <p class="text-yellow-600 font-medium mt-2">₱{{
                                item.product.Price.toLocaleString('en-US', {
                                    minimumFractionDigits: 2, maximumFractionDigits: 2
                                }) }}</p>
                            <div class="flex mt-4 space-x-2">
                                <button @click="addToCart(item.product.ID)"
                                    class="flex-1 bg-black text-white py-2 px-3 rounded-lg font-medium hover:bg-gray-800 transition-colors text-sm flex items-center justify-center"
                                    :disabled="isItemLoading(item.id) || item.product.Inventory_Level === 0 || isAddingToCart[item.product.ID]">
                                    <span v-if="!isAddingToCart[item.product.ID]">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 inline" fill="none"
                                            viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                                        </svg>
                                        Add to Cart
                                    </span>
                                    <span v-else class="inline-flex items-center">
                                        <div class="animate-spin h-4 w-4 border-b-2 border-white rounded-full mr-2">
                                        </div>
                                        Adding...
                                    </span>
                                </button>
                                <button @click="removeFromWishlist(item.id)"
                                    class="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors text-red-600"
                                    :disabled="isItemLoading(item.id)">
                                    <span v-if="!isRemoving[item.id]">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor"
                                            viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </span>
                                    <span v-else>
                                        <div class="animate-spin h-5 w-5 border-b-2 border-red-600 rounded-full">
                                        </div>
                                    </span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
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
    name: 'WishlistView',
    data() {
        return {
            wishlistItems: [],
            message: null,
            messageType: 'info',
            isLoading: true,
            isAuthenticated: false,
            isRemoving: {},
            isAddingToCart: {}
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
        async fetchWishlist() {
            if (!this.isAuthenticated) return;
            
            try {
                this.isLoading = true;
                const response = await api.get('/wishlist/');
                
                if (response.data && response.data.length > 0) {
                    // Process wishlist items - response.data now contains objects with id and product
                    const productPromises = response.data.map(async (item) => {
                        try {
                            const productId = item.product;
                            const productResponse = await api.get(`/products/${productId}`);
                            return {
                                id: item.id, // Use the wishlist item ID from the response
                                product: {
                                    ID: productId,
                                    Name: productResponse.data.name,
                                    Price: productResponse.data.price,
                                    Image: productResponse.data.image_url,
                                    Inventory_Level: productResponse.data.stock
                                }
                            };
                        } catch (error) {
                            console.error(`Error fetching product ${item.product}:`, error);
                            return null;
                        }
                    });

                    const results = await Promise.all(productPromises);
                    this.wishlistItems = results.filter(item => item !== null);
                    
                } else {
                    this.wishlistItems = [];
                }
                
                this.isLoading = false;
            } catch (error) {
                console.error('Error fetching wishlist:', error);
                this.wishlistItems = [];
                this.message = 'There was an error loading your wishlist. Please try again.';
                this.messageType = 'error';
                this.isLoading = false;
                
                if (error.response && error.response.status === 401) {
                    this.isAuthenticated = false;
                    this.$router.push('/auth/login');
                }
            }
        },
        isItemLoading(itemId) {
            return this.isRemoving[itemId] === true;
        },
        async removeFromWishlist(itemId) {
            // Set removing state for this item
            this.isRemoving = { ...this.isRemoving, [itemId]: true };
            
            try {
                // Extract the product ID from the wishlist item id
                const item = this.wishlistItems.find(item => item.id === itemId);
                if (!item) return;
                
                const productId = item.product.ID;
                
                // Use the toggle endpoint to remove the item
                await api.post('/wishlist/toggle/', {
                    product: productId
                });
                
                // Remove item from array
                this.wishlistItems = this.wishlistItems.filter(item => item.id !== itemId);
                
                // Show success message
                this.message = 'Item removed from wishlist';
                this.messageType = 'success';
                
                // Clear message after 3 seconds
                setTimeout(() => {
                    this.message = null;
                }, 3000);
            } catch (error) {
                console.error('Error removing from wishlist:', error);
                this.message = 'Failed to remove item from wishlist';
                this.messageType = 'error';
            } finally {
                // Clear removing state
                this.isRemoving = { ...this.isRemoving, [itemId]: false };
            }
        },
        async addToCart(productId) {
            // Set adding state for this item
            this.isAddingToCart = { ...this.isAddingToCart, [productId]: true };
            
            try {
                // Fetch the user's cart
                const cartResponse = await api.get('/cart/');
                
                if (!cartResponse.data || cartResponse.data.length === 0) {
                    throw new Error('No cart found');
                }
                
                const cart = cartResponse.data[0];
                
                // Check if the item already exists in the cart
                let existingItem = null;
                if (cart.cart_items && cart.cart_items.length > 0) {
                    existingItem = cart.cart_items.find(item => item.product === productId);
                }
                
                // Add the item to the cart
                await api.post(`/cart/${cart.cart_id}/items/`, {
                    product: productId,
                    quantity: 1
                });
                
                // Update cart count for unique items
                if (!existingItem) {
                    // Update cart count for a new unique item
                    const currentCount = parseInt(localStorage.getItem('cartCount') || '0');
                    localStorage.setItem('cartCount', (currentCount + 1).toString());
                    window.dispatchEvent(new Event('cart-updated'));
                }
                
                // Find and remove the item from wishlist
                const wishlistItem = this.wishlistItems.find(item => item.product.ID === productId);
                if (wishlistItem) {
                    // Use the toggle endpoint to remove the item from wishlist
                    await api.post('/wishlist/toggle/', {
                        product: productId
                    });
                    
                    // Remove item from wishlist array
                    this.wishlistItems = this.wishlistItems.filter(item => item.product.ID !== productId);
                }
                
                // Show success message
                this.message = 'Item added to cart';
                this.messageType = 'success';
                
                // Clear message after 3 seconds
                setTimeout(() => {
                    this.message = null;
                }, 3000);
            } catch (error) {
                console.error('Error adding to cart:', error);
                this.message = 'Failed to add item to cart';
                this.messageType = 'error';
                
                if (error.response && error.response.status === 401) {
                    this.isAuthenticated = false;
                    this.$router.push('/auth/login');
                }
            } finally {
                // Clear adding state
                this.isAddingToCart = { ...this.isAddingToCart, [productId]: false };
            }
        },
        scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
    },
    async created() {
        const isAuth = await this.checkAuth();
        if (isAuth) {
            await this.fetchWishlist();
        }
    }
};
</script>

<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

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

button:disabled {
    cursor: not-allowed;
    opacity: 0.5;
}
</style> 