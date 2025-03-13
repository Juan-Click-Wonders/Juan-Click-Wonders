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
            <div class="flex-1 flex flex-col">
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 p-6 auto-rows-max">
                    <router-link v-for="product in paginatedProducts" :key="product.product_id"
                        :to="'/product/' + product.product_id"
                        class="block border p-4 rounded-lg shadow-md bg-white hover:shadow-lg transition-transform transform hover:scale-105 h-fit">
                        <!-- Product Image -->
                        <div class="h-40 bg-white flex items-center justify-center">
                            <img v-if="product.image_url" :src="getImageUrl(product.image_url)" :alt="product.name"
                                class="max-h-full max-w-full object-contain" @error="handleImageError(product.product_id)">
                            <span v-else>No Image Available</span>
                        </div>

                        <!-- Product Details -->
                        <div class="mt-4">
                            <h3 class="font-bold truncate">{{ product.name }}</h3>
                            <p class="text-gray-700 font-semibold">₱{{ product.price.toLocaleString() }}</p>
                            <p class="text-sm text-gray-600">Category: {{ product.category_name }}</p>
                            <p class="text-sm text-gray-600">Brand: {{ product.brand }}</p>
                            <p class="text-sm text-gray-600">Stock: {{ product.stock }}</p>
                        </div>
                    </router-link>
                </div>
                <!-- Pagination Controls -->
                <div class="flex justify-center items-center gap-4 pb-6">
                    <button 
                        @click="previousPage" 
                        :disabled="currentPage === 1"
                        class="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:bg-gray-300"
                        :style="{
                            cursor: currentPage === 1 ? 'not-allowed' : 'pointer',
                            pointerEvents: currentPage === 1 ? 'none' : 'auto'
                        }"
                    >
                        Previous
                    </button>

                    <span class="text-lg">Page {{ currentPage }} of {{ totalPages }}</span>

                    <button 
                        @click="nextPage" 
                        :disabled="currentPage === totalPages"
                        class="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:bg-gray-300"
                        :style="{
                            cursor: currentPage === totalPages ? 'not-allowed' : 'pointer',
                            pointerEvents: currentPage === totalPages ? 'none' : 'auto'
                        }"
                    >
                        Next
                    </button>
                </div>
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
            imageLoadErrors: {},
            currentPage: 1,
            productsPerPage: 18
        };
    },
    computed: {
        // Remove the mapping since category_name is already in the response
        productsWithCategories() {
            return this.products; // No need to map, category_name is already included
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
            const searchTerm = this.searchQuery.toLowerCase();
            return this.productsWithCategories.filter(product => {
                // Category filter - ensure we're comparing numbers with numbers
                const matchesCategory = this.selectedCategories.length === 0 ||
                    this.selectedCategories.includes(Number(product.category_id));
                
                // Brand filter
                const matchesBrand = this.selectedBrands.length === 0 ||
                    this.selectedBrands.includes(product.brand);
                
                // Simplified search matching
                const matchesSearch = !this.searchQuery || (
                    product.name.toLowerCase().includes(searchTerm) ||
                    product.category_name.toLowerCase().includes(searchTerm)
                );

                return matchesCategory && matchesBrand && matchesSearch;
            });
        },
        paginatedProducts() {
            const start = (this.currentPage - 1) * this.productsPerPage;
            const end = start + this.productsPerPage;
            return this.filteredProducts.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.filteredProducts.length / this.productsPerPage);
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
            // If the imagePath is already a full URL, return it as is
            if (imagePath.startsWith('http')) {
                return imagePath;
            }
            // Otherwise, construct the full URL
            return `http://127.0.0.1:8000/media/product_images/${imagePath}`;
        },
        handleImageError(productId) {
            const product = this.products.find(p => p.product_id === productId);
            if (product) {
                fetch(this.getImageUrl(product.image_url))
                    .catch(() => {
                        this.imageLoadErrors[productId] = true;
                    });
            }
            this.imageLoadErrors[productId] = true;
        },
        fetchCategories() {
            api.get("/category")
                .then(response => {
                    this.categories = response.data;
                })
                .catch(error => {
                    // Consider adding user-friendly error handling here
                });
        },
        fetchProducts() {
            api.get("/products/")
                .then(response => {
                    this.products = response.data;
                })
                .catch(error => {
                    // Consider adding user-friendly error handling here
                });
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        },
        previousPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        },
        filterProducts() {
            this.currentPage = 1; // Reset to first page when filtering
            this.$forceUpdate();
        },
        updateSearchQuery() {
            this.$router.push({ query: { ...this.$route.query, search: this.searchQuery } });
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
