<template>
    <div class="p-6 font-sans max-w-screen-xl mx-auto">
        <h1 class="text-2xl font-bold mb-6">Order Management</h1>
        <div class="bg-white rounded-lg shadow overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full whitespace-nowrap">
                    <thead>
                        <tr class="bg-gray-100 text-center">
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
                        <!-- Product Row -->
                        <tr class="hover:bg-gray-50 transition-colors text-center">
                            <td class="px-6 py-4 whitespace-normal break-words max-w-[200px] text-left">
                                Placeholder GeForce RTX 3080
                            </td>
                            <td class="px-6 py-4">₱70,000.00</td>
                            <td class="px-6 py-4">1</td>
                            <td class="px-6 py-4 font-semibold">₱70,000.00</td>
                            <td class="px-6 py-4">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 min-w-15 justify-center">
                                    Paid
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
    name: 'ShoppingCart',
    data() {
        return {
            cartItems: [],
            cart: null,
            message: null,
            messageType: 'info',
            unavailableItems: [],
            userAddress: 'Loading...',
            isAuthenticated: false,
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
            return 1000;
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
                localStorage.removeItem('cartCount');
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
                        } catch (error) {
                            console.error(`Error fetching product ${item.product}:`, error);
                            this.unavailableItems.push(item.id);
                        }
                    }

                    localStorage.setItem('cartCount', this.cartItems.length.toString());
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
                const itemIndex = this.cartItems.findIndex(item => item.id === itemId);
                if (itemIndex === -1) return;

                const itemToUpdate = this.cartItems[itemIndex];

                if (newQuantity === 0) {
                    await this.removeFromCart(itemId);
                    return;
                }

                const quantityDifference = newQuantity - itemToUpdate.quantity;

                await api.patch(`/cart/${this.cart.cart_id}/items/${itemId}/`, {
                    quantity: newQuantity
                });

                this.cartItems[itemIndex].quantity = newQuantity;

                window.dispatchEvent(new Event('cart-updated'));
            } catch (error) {
                console.error('Error updating quantity:', error);
            }
        },
        async removeFromCart(itemId) {
            try {
                const itemIndex = this.cartItems.findIndex(item => item.id === itemId);
                if (itemIndex === -1) return;

                const itemToRemove = this.cartItems[itemIndex];

                await api.delete(`/cart/${this.cart.cart_id}/items/${itemId}/`);

                this.cartItems.splice(itemIndex, 1);

                const currentCount = parseInt(localStorage.getItem('cartCount') || '0');
                localStorage.setItem('cartCount', Math.max(0, currentCount - 1).toString());

                window.dispatchEvent(new Event('cart-updated'));

                if (this.cartItems.length === 0) {
                    this.cart = null;
                    localStorage.setItem('cartCount', '0');
                }
            } catch (error) {
                console.error('Error removing item:', error);
            }
        },
        async handleCheckout() {
        if (!this.selectedPayment) {
            this.paymentError = "Please select a payment method.";
            return;
        }

        this.paymentError = "";

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
        if (!this.isAuthenticated) {
            localStorage.removeItem('cartCount');
        }
    }
};
</script>