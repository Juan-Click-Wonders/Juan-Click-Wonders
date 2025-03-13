<template>
    <div class="container mx-auto p-6">
        <!-- Back to Catalog -->
        <button @click="$router.push('/product_list')"
            class="mb-4 px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-900">
            ← Back to Catalog
        </button>

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

                <!-- Ratings -->
                <div v-if="ratings.length > 0" class="mt-4">
                    <h3 class="font-semibold mb-2">Customer Reviews</h3>
                    <div v-for="rating in ratings" :key="rating.rating_id" class="mb-4 p-4 bg-gray-50 rounded">
                        <div class="flex items-center text-yellow-500">
                            <span v-for="star in 5" :key="star">
                                <i v-if="star <= rating.rating" class="fas fa-star"></i>
                                <i v-else class="far fa-star"></i>
                            </span>
                            <span class="ml-2 text-gray-500">{{ formatDate(rating.created_at) }}</span>
                        </div>
                        <p class="mt-2 text-gray-700">{{ rating.description }}</p>
                    </div>
                </div>

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
                        class="px-6 bg-black text-white rounded-full font-semibold hover:bg-gray-800 transition-colors"
                        style="height: 48px;">
                        Buy Now
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
        'Accept': 'application/json'
    }
});

export default {
    data() {
        return {
            product: null,
            categories: [],
            ratings: [],
            quantity: 1,
        };
    },
    computed: {
        categoryName() {
            if (!this.product || !this.categories.length) return 'Loading...';
            const category = this.categories.find(cat => cat.category_id === this.product.category);
            return category ? category.category_name : 'Unknown Category';
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
                    this.fetchRatings(productId);
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
