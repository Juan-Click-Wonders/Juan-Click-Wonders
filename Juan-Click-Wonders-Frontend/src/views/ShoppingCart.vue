<template>
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-8">Shopping Cart</h1>

        <!-- Message Display -->
        <div v-if="message" :class="[
            'mb-6 p-4 rounded-lg',
            messageType === 'error' ? 'bg-red-100 text-red-700' :
            messageType === 'success' ? 'bg-green-100 text-green-700' :
            'bg-blue-100 text-blue-700'
        ]">
            {{ message }}
        </div>

        <div v-if="cartItems.length === 0" class="text-center py-8">
            <p class="text-gray-600">Your cart is empty</p>
            <router-link to="/product_list" class="text-blue-600 hover:text-blue-800 mt-4 inline-block">
                Continue Shopping
            </router-link>
        </div>

        <div v-else class="flex flex-col lg:flex-row gap-8">
            <!-- Cart Items List -->
            <div class="lg:w-2/3">
                <div v-for="item in cartItems" :key="item.id" class="flex items-center border-b py-4">
                    <img :src="item.product.Image" :alt="item.product.Name" class="w-24 h-24 object-cover rounded">

                    <div class="flex-grow ml-4">
                        <h3 class="text-lg font-semibold">{{ item.product.Name }}</h3>
                        <p class="text-gray-600">₱{{ item.product.Price.toLocaleString('en-US', {
            minimumFractionDigits: 2, maximumFractionDigits: 2
        }) }}</p>

                        <div class="flex items-center mt-2">
                            <button @click="updateQuantity(item.id, item.quantity - 1)"
                                class="px-2 py-1 border rounded-l" 
                                :disabled="unavailableItems.includes(item.id)">
                                -
                            </button>
                            <span class="px-4 py-1 border-t border-b">{{ item.quantity }}</span>
                            <button @click="updateQuantity(item.id, item.quantity + 1)"
                                class="px-2 py-1 border rounded-r"
                                :disabled="item.quantity >= item.product.Inventory_Level || unavailableItems.includes(item.id)">
                                +
                            </button>
                        </div>
                        <p v-if="unavailableItems.includes(item.id)" class="text-red-600 mt-2">
                            This item is no longer available
                        </p>
                    </div>

                    <div class="text-right ml-4">
                        <p class="font-semibold">₱{{ (item.product.Price * item.quantity).toLocaleString('en-US', {
            minimumFractionDigits: 2, maximumFractionDigits: 2
        }) }}</p>
                        <button @click="removeFromCart(item.id)" class="text-red-600 hover:text-red-800 mt-2">
                            Remove
                        </button>
                    </div>
                </div>
            </div>

            <!-- Right Column -->
            <div class="lg:w-1/3">
                <!-- Location Section -->
                <div class="bg-gray-50 p-6 rounded-lg mb-1">
                    <h2 class="text-xl font-semibold mb-4">Location</h2>
                    <div class="flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                        </svg>
                        <span class="text-gray-600">{{ userAddress }}</span>
                    </div>
                </div>

                <hr class="my-1 border-gray-200">

                <!-- Cart Summary Content -->
                <div class="bg-gray-50 p-6 rounded-lg mt-1">
                    <h2 class="text-xl font-semibold mb-4">Cart Summary</h2>
                    <div class="flex justify-between mb-2">
                        <span>Subtotal</span>
                        <span>₱{{ subtotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</span>
                    </div>
                    <div class="flex justify-between mb-4">
                        <span>Shipping Fee</span>
                        <span>₱{{ shippingFee.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</span>
                    </div>
                    <div class="border-t pt-4">
                        <div class="flex justify-between font-semibold text-lg">
                            <span>Total</span>
                            <span>₱{{ total.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</span>
                        </div>
                    </div>
                    <button class="w-full bg-blue-600 text-white py-2 rounded mt-6 hover:bg-blue-700">
                        Proceed to Checkout
                    </button>
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
    name: 'ShoppingCart',
    data() {
        return {
            cartItems: [],
            cart: null,
            message: null,
            messageType: 'info',
            unavailableItems: [],
            userAddress: 'Loading...',
            isAuthenticated: false
        };
    },
    computed: {
        subtotal() {
            return this.cartItems.reduce((sum, item) => {
                return sum + (item.product.Price * item.quantity);
            }, 0);
        },
        shippingFee() {
            return 1000; // Fixed shipping fee of 1000 pesos
        },
        total() {
            return this.subtotal + this.shippingFee;
        }
    },
    methods: {
        async checkAuth() {
            try {
                await api.post('/api/auth/authenticate/');
                this.isAuthenticated = true;
                return true;
            } catch (error) {
                this.isAuthenticated = false;
                localStorage.removeItem('cartCount'); // Clear cart count if not authenticated
                this.$router.push('/auth/login');
                return false;
            }
        },
        async fetchUserProfile() {
            if (!this.isAuthenticated) return;
            try {
                const response = await api.get('/api/profile/');
                this.userAddress = response.data.address;
            } catch (error) {
                console.error('Error fetching user profile:', error);
                this.userAddress = 'Address not available';
                if (error.response && error.response.status === 401) {
                    this.isAuthenticated = false;
                    localStorage.removeItem('cartCount');
                    this.$router.push('/auth/login');
                }
            }
        },
        async fetchCart() {
            if (!this.isAuthenticated) return;
            try {
                const cartResponse = await api.get('/cart/');
                if (cartResponse.data && cartResponse.data.length > 0) {
                    this.cart = cartResponse.data[0];
                    this.cartItems = [];
                    this.unavailableItems = [];

                    let totalItems = 0;

                    for (const item of this.cart.cart_items) {
                        try {
                            const productResponse = await api.get(`/products/${item.product}`);
                            this.cartItems.push({
                                id: item.id,
                                quantity: item.quantity,
                                product: {
                                    Name: productResponse.data.name,
                                    Price: productResponse.data.price,
                                    Image: productResponse.data.image_url,
                                    Inventory_Level: productResponse.data.stock
                                }
                            });
                            totalItems += item.quantity;
                        } catch (error) {
                            console.error(`Error fetching product ${item.product}:`, error);
                            this.unavailableItems.push(item.id);
                        }
                    }

                    localStorage.setItem('cartCount', totalItems);
                    window.dispatchEvent(new Event('cart-updated'));

                    if (this.unavailableItems.length > 0) {
                        this.message = `${this.unavailableItems.length} item${this.unavailableItems.length > 1 ? 's' : ''} in your cart ${this.unavailableItems.length > 1 ? 'are' : 'is'} no longer available. Please remove them to proceed with checkout.`;
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
            } catch (error) {
                console.error('Error fetching cart:', error);
                this.cartItems = [];
                this.cart = null;
                this.message = 'There was an error loading your cart. Please try again.';
                this.messageType = 'error';
                if (error.response && error.response.status === 401) {
                    this.isAuthenticated = false;
                    localStorage.removeItem('cartCount');
                    this.$router.push('/auth/login');
                }
            }
        },
        async updateQuantity(itemId, newQuantity) {
            try {
                const itemToUpdate = this.cartItems.find(item => item.id === itemId);
                if (!itemToUpdate) return;

                // If quantity becomes 0, remove the item
                if (newQuantity === 0) {
                    await this.removeFromCart(itemId);
                    return;
                }

                const quantityDifference = newQuantity - itemToUpdate.quantity;

                await api.patch(`/cart/${this.cart.cart_id}/items/${itemId}/`, {
                    quantity: newQuantity
                });

                // Update cart count in localStorage
                const currentCount = parseInt(localStorage.getItem('cartCount') || '0');
                localStorage.setItem('cartCount', Math.max(0, currentCount + quantityDifference));
                
                // Emit cart-updated event to update the navbar
                window.dispatchEvent(new Event('cart-updated'));

                await this.fetchCart(); // Refresh cart data
            } catch (error) {
                console.error('Error updating quantity:', error);
            }
        },
        async removeFromCart(itemId) {
            try {
                // Find the item quantity before removing it
                const itemToRemove = this.cartItems.find(item => item.id === itemId);
                if (!itemToRemove) return;

                await api.delete(`/cart/${this.cart.cart_id}/items/${itemId}/`);
                
                // Update cart count in localStorage
                const currentCount = parseInt(localStorage.getItem('cartCount') || '0');
                localStorage.setItem('cartCount', Math.max(0, currentCount - itemToRemove.quantity));
                
                // Emit cart-updated event to update the navbar
                window.dispatchEvent(new Event('cart-updated'));
                
                await this.fetchCart(); // Refresh cart data
            } catch (error) {
                console.error('Error removing item:', error);
            }
        }
    },
    async created() {
        const isAuth = await this.checkAuth();
        if (isAuth) {
            await this.fetchCart();
            await this.fetchUserProfile();
        }
    },
    beforeUnmount() {
        // Clean up if component is unmounted while not authenticated
        if (!this.isAuthenticated) {
            localStorage.removeItem('cartCount');
        }
    }
};
</script>