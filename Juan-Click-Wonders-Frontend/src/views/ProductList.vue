<template>
    <div class="w-full mx-auto flex">
        <!-- Sidebar (Category Filter) -->
        <aside class="w-full sm:w-1/3 md:w-1/4 lg:w-1/10 mt-10 w-max h-max p-4 border-black border-2 rounded-xl ml-4">
            <h2 class="text-xl font-semibold mb-2">Filter by Category</h2>
            <div v-for="category in categories" :key="category.category_ID">
                <label class="flex items-center space-x-2">
                    <input type="checkbox" v-model="selectedCategories" :value="category.category_ID"
                        @change="filterProducts">
                    <span>{{ category.category_name }}</span>
                </label>
            </div>
        </aside>

        <!-- Product Grid -->
        <div class="flex-1 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4 p-6">
            <router-link v-for="product in filteredProducts" :key="product.product_ID"
                :to="'/product/' + product.product_ID"
                class="block border p-8 rounded-lg shadow-md bg-white hover:shadow-lg transition-transform transform hover:scale-105 w-full">
                <!-- Placeholder for Product Image -->
                <div class="h-40 bg-gray-300 flex items-center justify-center">
                    <img v-if="getImageUrl(product.product_image)" :src="getImageUrl(product.product_image)"
                        :alt="product.Product_Name" class="max-h-full max-w-full"
                        @error="handleImageError(product.product_ID)">
                    <span v-else>No Image Available</span>
                </div>

                <!-- Product Details -->
                <h3 class="mt-2 font-bold">{{ product.product_name }}</h3>
                <p class="text-gray-700 font-semibold">₱{{ product.price.toLocaleString() }}</p>
                <p class="text-sm text-gray-600">Brand: {{ product.brand }}</p>
                <p class="text-sm text-gray-600">Stock: {{ product.inventory_level }}</p>
                <p class="text-sm text-gray-500 mt-2 line-clamp-2">{{ product.description }}</p>
            </router-link>
        </div>
    </div>
</template>

<script>
import axios from "axios";

// Create an axios instance with the base URL
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Accept': 'application/json'
    }
});

export default {
    data() {
        return {
            products: [],
            categories: [],
            selectedCategories: [],
            imageLoadErrors: {} // Track image loading errors
        };
    },
    computed: {
        filteredProducts() {
            if (this.selectedCategories.length === 0) {
                return this.products;
            }
            return this.products.filter(product =>
                this.selectedCategories.includes(product.category_id)
            );
        }
    },
    methods: {
        getImageUrl(imagePath) {
            if (!imagePath) return null;
            return `http://127.0.0.1:8000/${imagePath}`;
        },

        handleImageError(productId) {
            console.error(`Failed to load image for product ${productId}`);
            const product = this.products.find(p => p.Product_ID === productId);
            if (product) {
                const url = this.getImageUrl(product.Product_Picture);
                console.error('Failed URL:', url);
            }
            this.imageLoadErrors[productId] = true;
        },

        fetchProducts() {
            api.get("/api/products/product-list/")
                .then(response => {
                    this.products = response.data;
                })
                .catch(error => {
                    console.error("Error fetching products:", error);
                });
        },

        fetchCategories() {
            api.get("/api/products/categories/")
                .then(response => {
                    this.categories = response.data;
                })
                .catch(error => {
                    console.error("Error fetching categories:", error);
                });
        },

        filterProducts() {
            this.$forceUpdate();
        }
    },
    created() {
        this.fetchProducts();
        this.fetchCategories();
    }
};
</script>

<style>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css");
</style>
