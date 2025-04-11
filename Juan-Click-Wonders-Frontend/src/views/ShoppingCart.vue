<template>
    <div class="bg-gray-50 min-h-screen pb-16">
        <!-- Header and Breadcrumbs -->
        <div class="bg-white border-b border-gray-200">
            <div class="container mx-auto px-4 py-6">
                <h1 class="text-3xl font-bold mb-2">Your Shopping Cart</h1>
                <div class="flex items-center text-sm text-gray-600">
                    <router-link to="/" class="hover:text-yellow-600 transition-colors">Home</router-link>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mx-2" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                    <span class="text-gray-800 font-medium">Cart</span>
                </div>
            </div>
        </div>

        <div class="container mx-auto px-4 py-8">
            <!-- Loading State -->
            <div v-if="isLoading" class="text-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-4 border-yellow-500 mx-auto"></div>
                <p class="text-gray-600 mt-4">Loading your cart...</p>
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

            <!-- Empty Cart State -->
            <div v-if="!isLoading && cartItems.length === 0"
                class="bg-white rounded-xl shadow-md overflow-hidden p-8 text-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <h3 class="text-xl font-bold text-gray-700 mb-2">Your Cart is Empty</h3>
                <p class="text-gray-600 mb-6">Looks like you haven't added any products to your cart yet.</p>
                <router-link to="/product_list"
                    class="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold px-6 py-2 rounded-lg transition-colors duration-200 inline-flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    Continue Shopping
                </router-link>
            </div>

            <!-- Cart Content -->
            <div v-else-if="!isLoading" class="flex flex-col lg:flex-row gap-8">
                <!-- Cart Items List -->
                <div class="lg:w-2/3">
                    <div class="bg-white rounded-xl shadow-md overflow-hidden">
                        <div class="p-6 border-b border-gray-200">
                            <div class="flex justify-between items-center">
                                <h2 class="text-xl font-semibold">Cart Items ({{ cartItems.length }})</h2>
                                <button @click="clearCart"
                                    class="text-gray-600 hover:text-red-600 text-sm flex items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none"
                                        viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                    Clear Cart
                                </button>
                            </div>
                        </div>

                        <div v-for="item in cartItems" :key="item.id"
                            class="p-6 border-b border-gray-100 hover:bg-gray-50 transition-colors">
                            <div class="flex items-center">
                                <router-link :to="`/product/${item.product.ID}`"
                                    class="w-24 h-24 rounded-lg flex items-center justify-center overflow-hidden bg-transparent border border-gray-100 hover:border-yellow-500 transition-colors">
                                    <img v-if="item.product.Image" :src="item.product.Image" :alt="item.product.Name"
                                        class="w-full h-full object-contain p-1">
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-300"
                                        fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </router-link>

                                <div class="flex-grow ml-6">
                                    <router-link :to="`/product/${item.product.ID}`"
                                        class="text-lg font-semibold hover:text-yellow-600 transition-colors">{{
                                        item.product.Name }}</router-link>
                                    <p class="text-yellow-600 font-medium">₱{{
                                        item.product.Price.toLocaleString('en-US', {
                                            minimumFractionDigits: 2, maximumFractionDigits: 2
                                        }) }}</p>

                                    <div v-if="item.product.Inventory_Level < 5 && item.product.Inventory_Level > 0"
                                        class="text-orange-600 text-sm mt-1">
                                        Only {{ item.product.Inventory_Level }} left in stock
                                    </div>
                                </div>

                                <div class="flex flex-col items-end space-y-3">
                                    <div class="text-right">
                                        <p class="font-semibold">₱{{ (item.product.Price *
                                            item.quantity).toLocaleString('en-US', {
                                                minimumFractionDigits: 2, maximumFractionDigits: 2
                                            }) }}</p>
                                    </div>

                                    <div class="flex items-center">
                                        <button @click="updateQuantity(item.id, item.quantity - 1)"
                                            class="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center text-gray-700"
                                            :disabled="unavailableItems.includes(item.id) || itemsLoading.includes(item.id)">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M20 12H4" />
                                            </svg>
                                        </button>

                                        <div class="w-10 text-center font-medium mx-2 relative">
                                            <span v-if="!itemsLoading.includes(item.id)">{{ item.quantity }}</span>
                                            <div v-else class="absolute inset-0 flex items-center justify-center">
                                                <div
                                                    class="animate-spin h-4 w-4 border-b-2 border-yellow-500 rounded-full">
                                                </div>
                                            </div>
                                        </div>

                                        <button @click="updateQuantity(item.id, item.quantity + 1)"
                                            class="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center text-gray-700"
                                            :disabled="item.quantity >= item.product.Inventory_Level || unavailableItems.includes(item.id) || itemsLoading.includes(item.id)">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M12 4v16m8-8H4" />
                                            </svg>
                                        </button>
                                    </div>

                                    <button @click="removeFromCart(item.id)"
                                        class="text-red-600 hover:text-red-800 text-sm"
                                        :disabled="itemsLoading.includes(item.id)">
                                        <span v-if="!itemsRemoving.includes(item.id)">Remove</span>
                                        <span v-else class="inline-flex items-center">
                                            <div
                                                class="animate-spin h-3 w-3 border-b-2 border-red-600 rounded-full mr-1">
                                            </div>
                                            Removing
                                        </span>
                                    </button>
                                </div>
                            </div>

                            <div v-if="unavailableItems.includes(item.id)"
                                class="mt-3 bg-red-50 p-3 rounded-lg text-red-600 text-sm flex items-start">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 flex-shrink-0" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <span>
                                    This product is no longer available. Please remove it from your cart to continue
                                    checkout.
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right Column -->
                <div class="lg:w-1/3">
                    <!-- Location Section -->
                    <div class="bg-white rounded-xl shadow-md overflow-hidden mb-6">
                        <div class="p-6">
                            <h2 class="text-xl font-semibold mb-4">Delivery Address</h2>
                            <div v-if="isAddressLoading" class="animate-pulse flex space-x-4">
                                <div class="flex-1 space-y-2 py-1">
                                    <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                                    <div class="h-4 bg-gray-200 rounded"></div>
                                </div>
                            </div>
                            <div v-else class="flex items-start">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 mr-2 mt-0.5"
                                    viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd"
                                        d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                                        clip-rule="evenodd" />
                                </svg>
                                <div>
                                    <p class="text-gray-700">{{ userAddress }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Cart Summary Content -->
                    <div class="bg-white rounded-xl shadow-md overflow-hidden">
                        <div class="p-6">
                            <h2 class="text-xl font-semibold mb-4">Order Summary</h2>
                            <div class="space-y-3">
                                <div class="flex justify-between text-gray-600">
                                    <span>Subtotal ({{ cartItems.length }} items)</span>
                                    <span class="font-medium">₱{{ subtotal.toLocaleString('en-US', {
                                        minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</span>
                                </div>
                                <div class="flex justify-between text-gray-600">
                                    <span>Shipping Fee</span>
                                    <span class="font-medium">₱{{ shippingFee.toLocaleString('en-US', {
                                        minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</span>
                                </div>
                            </div>

                            <div class="border-t pt-4 mt-4">
                                <div class="flex justify-between font-semibold text-lg">
                                    <span>Total</span>
                                    <span class="text-xl">₱{{ total.toLocaleString('en-US', {
                                        minimumFractionDigits: 2,
                                        maximumFractionDigits: 2 }) }}</span>
                                </div>
                            </div>

                            <div class="mt-6 mb-4">
                                <p class="text-gray-800 font-medium mb-3">Payment Method</p>
                                <div class="grid grid-cols-2 gap-4">
                                    <label
                                        class="border border-gray-200 rounded-lg p-3 cursor-pointer transition-all duration-200"
                                        :class="selectedPayment === 'GCS' ? 'border-yellow-500 bg-yellow-50' : 'hover:border-yellow-500 hover:bg-yellow-50'">
                                        <div class="flex items-center gap-2">
                                            <input v-model="selectedPayment" type="radio" name="payment" value="GCS"
                                                @change="paymentError = ''"
                                                class="cursor-pointer h-4 w-4 text-yellow-500 focus:ring-yellow-500" />
                                            <span class="flex-1 font-medium">GCash</span>
                                        </div>
                                    </label>
                                    <label
                                        class="border border-gray-200 rounded-lg p-3 cursor-pointer transition-all duration-200"
                                        :class="selectedPayment === 'MYA' ? 'border-yellow-500 bg-yellow-50' : 'hover:border-yellow-500 hover:bg-yellow-50'">
                                        <div class="flex items-center gap-2">
                                            <input v-model="selectedPayment" type="radio" name="payment" value="MYA"
                                                @change="paymentError = ''"
                                                class="cursor-pointer h-4 w-4 text-yellow-500 focus:ring-yellow-500" />
                                            <span class="flex-1 font-medium">Maya</span>
                                        </div>
                                    </label>
                                </div>
                            </div>

                            <div v-if="paymentError"
                                class="mt-4 p-3 bg-red-50 border border-red-200 text-red-600 rounded-lg text-sm flex items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 flex-shrink-0" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                {{ paymentError }}
                            </div>

                            <button @click="handleCheckout"
                                class="w-full bg-black text-white py-3 rounded-lg mt-6 hover:bg-gray-800 font-semibold flex items-center justify-center"
                                :disabled="unavailableItems.length > 0 || cartItems.length === 0 || isCheckingOut || !selectedPayment">
                                <span v-if="!isCheckingOut">Proceed to Checkout</span>
                                <span v-else class="inline-flex items-center">
                                    <div class="animate-spin h-4 w-4 border-b-2 border-white rounded-full mr-2"></div>
                                    Processing
                                </span>
                            </button>

                            <router-link to="/product_list"
                                class="w-full block text-center text-gray-600 hover:text-gray-800 mt-4 text-sm">
                                Continue Shopping
                            </router-link>
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
    name: 'ShoppingCart',
    data() {
        return {
            cartItems: [],
            cart: null,
            message: null,
            messageType: 'info',
            unavailableItems: [],
            itemsLoading: [], // Track items being updated
            itemsRemoving: [], // Track items being removed
            userAddress: 'No address on file',
            isAuthenticated: false,
            isLoading: true,
            isAddressLoading: true,
            isCheckingOut: false,
            selectedPayment: "",
            paymentError: ""
        };
    },
    computed: {
        subtotal() {
            return this.cartItems.reduce((sum, item) => {
                return sum + (item.product.Price * item.quantity);
            }, 0);
        },
        shippingFee() {
            // Fixed shipping fee of 1000
            return 1000;
        },
        total() {
            return this.subtotal + this.shippingFee;
        },
        hasUnavailableItems() {
            return this.unavailableItems.length > 0;
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
                this.isAddressLoading = true;
                const response = await api.get('/api/profile/');
                this.userAddress = response.data.address || 'No address on file';
                this.isAddressLoading = false;
            } catch (error) {
                console.error('Error fetching user profile:', error);
                this.userAddress = 'Address not available';
                this.isAddressLoading = false;
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

                    // Calculate total number of items (sum of quantities)
                    const totalQuantity = this.cartItems.reduce((sum, item) => sum + item.quantity, 0);

                    // Set cart count to total quantity of all items
                    localStorage.setItem('cartCount', totalQuantity.toString());
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
        },
        async updateQuantity(itemId, newQuantity) {
            try {
                // Add item to loading state
                this.itemsLoading.push(itemId);

                const itemToUpdate = this.cartItems.find(item => item.id === itemId);
                if (!itemToUpdate) return;

                // If quantity becomes 0, remove the item
                if (newQuantity === 0) {
                    await this.removeFromCart(itemId);
                    return;
                }

                // Calculate the quantity difference
                const quantityDifference = newQuantity - itemToUpdate.quantity;

                await api.patch(`/cart/${this.cart.cart_id}/items/${itemId}/`, {
                    quantity: newQuantity
                });

                // Update the item's quantity locally
                itemToUpdate.quantity = newQuantity;

                // Update cart count in localStorage to reflect the total quantities
                const currentCount = parseInt(localStorage.getItem('cartCount') || '0');
                localStorage.setItem('cartCount', (currentCount + quantityDifference).toString());

                // Emit cart-updated event to update the navbar
                window.dispatchEvent(new Event('cart-updated'));

                // Remove from loading state
                this.itemsLoading = this.itemsLoading.filter(id => id !== itemId);
            } catch (error) {
                console.error('Error updating quantity:', error);
                this.message = 'Failed to update cart. Please try again.';
                this.messageType = 'error';
                // Remove from loading state
                this.itemsLoading = this.itemsLoading.filter(id => id !== itemId);
            }
        },
        async removeFromCart(itemId) {
            try {
                // Add to removing state
                this.itemsRemoving.push(itemId);

                // Find the item and get its quantity before removing
                const itemToRemove = this.cartItems.find(item => item.id === itemId);
                const quantityToRemove = itemToRemove ? itemToRemove.quantity : 0;

                await api.delete(`/cart/${this.cart.cart_id}/items/${itemId}/`);

                // Remove item from cart items array
                this.cartItems = this.cartItems.filter(item => item.id !== itemId);

                // Update cart count - decrease by the full quantity of the removed item
                const currentCount = parseInt(localStorage.getItem('cartCount') || '0');
                localStorage.setItem('cartCount', Math.max(0, currentCount - quantityToRemove).toString());

                window.dispatchEvent(new Event('cart-updated'));

                // Remove from removing state
                this.itemsRemoving = this.itemsRemoving.filter(id => id !== itemId);

                // Also remove from unavailable items if it was there
                this.unavailableItems = this.unavailableItems.filter(id => id !== itemId);
            } catch (error) {
                console.error('Error removing item:', error);
                this.message = 'Failed to remove item. Please try again.';
                this.messageType = 'error';
                // Remove from removing state
                this.itemsRemoving = this.itemsRemoving.filter(id => id !== itemId);
            }
        },
        async clearCart() {
            try {
                if (!confirm('Are you sure you want to clear your cart? This action cannot be undone.')) {
                    return;
                }

                this.isLoading = true;

                if (this.cart) {
                    // Delete all items from the cart
                    for (const item of this.cartItems) {
                        await api.delete(`/cart/${this.cart.cart_id}/items/${item.id}/`);
                    }
                }

                // Reset cart data
                this.cartItems = [];
                localStorage.setItem('cartCount', '0');
                window.dispatchEvent(new Event('cart-updated'));

                this.isLoading = false;
            } catch (error) {
                console.error('Error clearing cart:', error);
                this.message = 'Failed to clear cart. Please try again.';
                this.messageType = 'error';
                this.isLoading = false;
            }
        },
        async proceedToCheckout() {
            if (this.unavailableItems.length > 0 || this.cartItems.length === 0) return;

            try {
                this.isCheckingOut = true;

                // Simulate checkout process - in a real app, you would redirect to checkout page
                // or make an API call to create an order
                await new Promise(resolve => setTimeout(resolve, 1000));

                // Redirect to checkout page
                this.$router.push('/checkout');
            } catch (error) {
                console.error('Error proceeding to checkout:', error);
                this.message = 'Failed to proceed to checkout. Please try again.';
                this.messageType = 'error';
                this.isCheckingOut = false;
            }
        },
        async handleCheckout() {
            if (!this.selectedPayment) {
                this.paymentError = "Please select a payment method.";
                return;
            }

            this.paymentError = "";
            this.isCheckingOut = true;

            try {
                const response = await axios.post("http://127.0.0.1:8000/payment/", {
                    method: this.selectedPayment
                }, {
                    withCredentials: true,
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                });
                if (response.status === 200) {
                    window.location.href = response.data.action_url;
                }
            } catch (error) {
                this.isCheckingOut = false;
                if (error.response && error.response.status === 400) {
                    const errorMessage = error.response.data?.detail;
                    this.paymentError = errorMessage;
                } else {
                    console.error("Payment failed:", error);
                    this.paymentError = "Payment Failed. Please try again.";
                    return;
                }
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

<style scoped>
@keyframes pulse {

    0%,
    100% {
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

.bg-yellow-50 {
    background-color: rgba(255, 193, 7, 0.05);
}

.text-yellow-500 {
    color: #f59e0b;
}

.border-yellow-500 {
    border-color: #f59e0b;
}

.hover\:bg-yellow-50:hover {
    background-color: rgba(255, 193, 7, 0.05);
}

.hover\:border-yellow-500:hover {
    border-color: #f59e0b;
}

.focus\:ring-yellow-500:focus {
    --tw-ring-color: rgba(245, 158, 11, 0.5);
}
</style>