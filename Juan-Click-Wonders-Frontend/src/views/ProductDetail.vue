<template>
    <div class="container mx-auto p-6">
        <!-- Back to Catalog -->
        <router-link 
            to="/product_list"
            class="inline-block mb-4 px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-900 cursor-pointer"
        >
            ← Back to Catalog
        </router-link>

        <div v-if="product" class="flex gap-8 mt-4">
            <!-- Product Image -->
            <div class="w-1/2">
                <img v-if="product.image_url" :src="getImageUrl(product.image_url)" :alt="product.name" class="w-full max-h-[500px] object-contain">
                <div v-else class="w-full h-[500px] bg-gray-200 flex items-center justify-center">
                    <span>No Image Available</span>
                </div>
            </div>

            <!-- Product Details -->
            <div class="w-1/2">
                <!-- Category -->
                <h4 class="text-sm text-gray-500 uppercase font-semibold mt-2">{{ categoryName }}</h4>

                <!-- Title -->
                <h2 class="text-3xl font-bold mt-1">{{ product.name }}</h2>

                <!-- Brand -->
                <p class="text-gray-700 mt-4">Brand: {{ product.brand }}</p>

                <!-- Description -->
                <p class="text-gray-700 mt-4">{{ product.description }}</p>

                <!-- Price -->
                <p class="text-2xl font-semibold text-gray-800 mt-4">₱{{ product.price.toLocaleString() }}</p>

                <!-- Stock -->
                <p class="text-gray-700 mt-2">Stock Available: {{ product.stock }}</p>

                <!-- Quantity Selector & Buy Button -->
                <div class="flex items-center mt-6 gap-4">
                    <!-- Quantity Selector -->
                    <div class="relative flex items-center border rounded-full bg-white px-4"
                        style="height: 48px; min-width: 120px; position: relative;">
                        <input type="text" v-model="quantity"
                            class="w-10 text-center bg-transparent focus:outline-none text-lg font-semibold" readonly>
                        <div class="absolute right-3 flex flex-col">
                            <button @click="increaseQuantity" class="text-gray-700 hover:text-black cursor-pointer">
                                <i class="fas fa-chevron-up"></i>
                            </button>
                            <button @click="decreaseQuantity" class="text-gray-700 hover:text-black cursor-pointer">
                                <i class="fas fa-chevron-down"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Buy Button -->
                    <button
                        @click="addToCart"
                        class="px-6 bg-black text-white rounded-full font-semibold hover:bg-gray-800 transition-colors"
                        style="height: 48px;">
                        Add to Cart
                    </button>
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
            loading: false
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
        fetchCategories() {
            api.get("/category")
                .then(response => {
                    this.categories = response.data;
                })
                .catch(error => {
                    console.error("Error fetching categories:", error);
                });
        },
        fetchProduct() {
            const productId = this.$route.params.id;
            api.get(`/products/${productId}`)
                .then(response => {
                    this.product = response.data;
                })
                .catch(error => {
                    console.error("Error fetching product:", error);
                });
        },
        fetchRatings(productId) {
            api.get(`/products/ratings/${productId}`)
                .then(response => {
                    this.ratings = response.data;
                })
                .catch(error => {
                    console.error("Error fetching ratings:", error);
                });
        },
        increaseQuantity() {
            if (this.quantity < this.product.stock) this.quantity++;
        },
        decreaseQuantity() {
            if (this.quantity > 1) this.quantity--;
        },
        async addToCart() {
            if (!this.isLoggedIn) {
                alert('Please log in to add items to your cart.');
                this.$router.push('/auth/login/');
                return;
            }

            try {
                const cartResponse = await api.get('/cart/');
                const cart = cartResponse.data[0]; 

                await api.post(`/cart/${cart.cart_id}/items/`, {
                    product: this.product.product_id,
                    quantity: this.quantity
                });

                // Update cart count in localStorage
                const currentCount = parseInt(localStorage.getItem('cartCount') || '0');
                localStorage.setItem('cartCount', currentCount + this.quantity);

                // Emit cart-updated event
                window.dispatchEvent(new Event('cart-updated'));

                // Show success message
                alert('Product added to cart successfully!');
            } catch (error) {
                console.error('Error adding to cart:', error);
                if (error.response && error.response.status === 401) {
                    alert('Please log in to add items to your cart.');
                    this.$router.push('/auth/login/');
                } else if (error.response && error.response.data) {
                    alert(error.response.data.detail || 'Failed to add item to cart. Please try again.');
                } else {
                    alert('Failed to add item to cart. Please try again.');
                }
            }
        }
    },
    created() {
        this.fetchCategories();
        this.fetchProduct();
    }
};
</script>

<style>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css");
</style>
