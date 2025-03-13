<template>
    <div class="w-full mx-auto">
        <div class="flex rounded-xl">
            <!-- Sidebar (Category Filter) -->
            <aside class="w-64 mt-10 p-4 border-black border-2 rounded-xl ml-4 h-fit">
                <h2 class="text-xl font-semibold mb-2">Filter by Category</h2>
                <div v-for="category in displayCategories" :key="category.category_id">
                    <label class="flex items-center space-x-2">
                        <input type="checkbox" v-model="selectedCategories" :value="category.category_id"
                            @change="filterProducts">
                        <span>{{ category.category_name }}</span>
                    </label>
                </div>

                <!-- Brand Filter -->
                <h2 class="text-xl font-semibold mb-2 mt-6">Filter by Brand</h2>
                <div v-for="brand in uniqueBrands" :key="brand">
                    <label class="flex items-center space-x-2">
                        <input type="checkbox" v-model="selectedBrands" :value="brand" @change="filterProducts">
                        <span>{{ brand }}</span>
                    </label>
                </div>
            </aside>

            <!-- Product Grid -->
            <div
                class="flex-1 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 p-6 auto-rows-max">
                <router-link v-for="product in filteredProducts" :key="product.product_id"
                    :to="'/product/' + product.product_id"
                    class="block border p-4 rounded-lg shadow-md bg-white hover:shadow-lg transition-transform transform hover:scale-105 h-fit">
                    <!-- Product Image -->
                    <div class="h-40 bg-gray-300 flex items-center justify-center">
                        <img v-if="product.image_url" :src="getImageUrl(product.image_url)" :alt="product.name"
                            class="max-h-full max-w-full object-contain" @error="handleImageError(product.product_id)">
                        <span v-else>No Image Available</span>
                    </div>

                    <!-- Product Details -->
                    <div class="mt-4">
                        <h3 class="font-bold truncate">{{ product.name }}</h3>
                        <p class="text-gray-700 font-semibold">₱{{ product.price.toLocaleString() }}</p>
                        <p class="text-sm text-gray-600">Category: {{ product.categoryName }}</p>
                        <p class="text-sm text-gray-600">Brand: {{ product.brand }}</p>
                        <p class="text-sm text-gray-600">Stock: {{ product.stock }}</p>
                    </div>
                </router-link>
            </div>
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
            selectedBrands: [],
            searchQuery: '',
            imageLoadErrors: {}
        };
    },
    computed: {
        // Map products with category names
        productsWithCategories() {
            return this.products.map(product => ({
                ...product,
                categoryName: this.getCategoryName(product.category)
            }));
        },
        displayCategories() {
            return this.categories.map(category => ({
                category_id: category.category_id,
                category_name: category.category_name
            }));
        },
        uniqueBrands() {
            return [...new Set(this.products.map(product => product.brand))].sort();
        },
        filteredProducts() {
            return this.productsWithCategories.filter(product => {
                const matchesCategory = this.selectedCategories.length === 0 ||
                    this.selectedCategories.includes(product.category);
                const matchesBrand = this.selectedBrands.length === 0 ||
                    this.selectedBrands.includes(product.brand);
                const matchesSearch = !this.searchQuery ||
                    product.name.toLowerCase().includes(this.searchQuery.toLowerCase());
                return matchesCategory && matchesBrand && matchesSearch;
            });
        }
    },
    watch: {
        // Watch for route query changes to update search
        '$route.query': {
            immediate: true,
            handler(newQuery) {
                this.searchQuery = newQuery.search || '';
            }
        }
    },
    methods: {
        getCategoryName(categoryId) {
            const category = this.categories.find(cat => cat.category_id === categoryId);
            return category ? category.category_name : 'Unknown Category';
        },
        getImageUrl(imagePath) {
            if (!imagePath) return null;
            return `http://127.0.0.1:8000/media/product_images/${imagePath}`;
        },
        handleImageError(productId) {
            console.error(`Failed to load image for product ${productId}`);
            const product = this.products.find(p => p.product_id === productId);
            if (product) {
                console.error('Failed URL:', product.image_url);
            }
            this.imageLoadErrors[productId] = true;
        },
        fetchCategories() {
            api.get("/api/products/category")
                .then(response => {
                    console.log("Categories fetched:", response.data);
                    this.categories = response.data;
                })
                .catch(error => {
                    console.error("Error fetching categories:", error);
                });
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
        filterProducts() {
            this.$forceUpdate();
        }
    },
    created() {
        this.fetchCategories();
        this.fetchProducts();
    }
};
</script>

<style>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css");
</style>
