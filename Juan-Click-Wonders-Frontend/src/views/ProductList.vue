<template>
    <div class="bg-gray-50 min-h-screen pt-8 pb-16">
        <!-- Page Header -->
        <div class="container mx-auto px-4 mb-8">
            <div class="flex flex-col">
                <h1 class="text-3xl md:text-4xl font-bold mb-3 text-gray-900">
                    <span v-if="searchQuery">Search Results for "{{ searchQuery }}"</span>
                    <span v-else>Browse Products</span>
                </h1>
                <div class="h-1 w-24 bg-yellow-500 rounded-full mb-4"></div>
                <p class="text-gray-600 max-w-2xl">
                    Find the perfect hardware to upgrade your gaming experience
                </p>
            </div>
        </div>

        <!-- Main Content Area -->
        <div class="container mx-auto px-4">
            <div class="flex flex-col lg:flex-row gap-8">
                <!-- Sidebar -->
                <aside class="lg:w-64 w-full lg:sticky top-4 h-fit">
                    <div class="bg-white rounded-xl shadow-md overflow-hidden">
                        <!-- Filter Header -->
                        <div class="bg-gradient-to-r from-gray-900 to-gray-800 px-6 py-4">
                            <h2 class="text-xl font-bold text-white flex items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                                </svg>
                                Filters
                            </h2>
                        </div>

                        <!-- Filter Sections -->
                        <div class="p-6 space-y-6">
                            <!-- Category Filter -->
                            <div class="border-b border-gray-200 pb-6">
                                <h3 class="text-lg font-semibold mb-4 flex items-center text-gray-900">
                                    <span class="h-1 w-4 bg-yellow-500 rounded-full mr-2"></span>
                                    Categories
                                </h3>
                                <div class="space-y-2 max-h-60 overflow-y-auto pr-2 scrollbar">
                                    <div v-for="category in displayedCategories" :key="category.category_id"
                                        class="transition-all duration-200">
                                        <label class="flex items-center space-x-3 cursor-pointer group">
                                            <input type="checkbox" v-model="selectedCategories"
                                                :value="category.category_id" @change="applyFilters"
                                                class="form-checkbox h-4 w-4 text-yellow-500 rounded focus:ring-yellow-500 transition duration-150">
                                            <span class="text-gray-700 group-hover:text-yellow-600">{{
                                                category.category_name }}</span>
                                        </label>
                                    </div>
                                    <button v-if="displayCategories.length > 5" @click="toggleCategories"
                                        class="text-yellow-600 hover:text-yellow-700 text-sm mt-3 flex items-center font-medium">
                                        {{ hasMoreCategories ? 'View More' : 'Show Less' }}
                                        <i
                                            :class="hasMoreCategories ? 'fas fa-chevron-down ml-1' : 'fas fa-chevron-up ml-1'"></i>
                                    </button>
                                </div>
                            </div>

                            <!-- Brand Filter -->
                            <div class="border-b border-gray-200 pb-6">
                                <h3 class="text-lg font-semibold mb-4 flex items-center text-gray-900">
                                    <span class="h-1 w-4 bg-yellow-500 rounded-full mr-2"></span>
                                    Brands
                                </h3>
                                <div class="space-y-2 max-h-60 overflow-y-auto pr-2 scrollbar">
                                    <div v-for="brand in displayedBrands" :key="brand"
                                        class="transition-all duration-200">
                                        <label class="flex items-center space-x-3 cursor-pointer group">
                                            <input type="checkbox" v-model="selectedBrands" :value="brand"
                                                @change="applyFilters"
                                                class="form-checkbox h-4 w-4 text-yellow-500 rounded focus:ring-yellow-500 transition duration-150">
                                            <span class="text-gray-700 group-hover:text-yellow-600">{{ brand }}</span>
                                        </label>
                                    </div>
                                    <button v-if="uniqueBrands.length > 5" @click="toggleBrands"
                                        class="text-yellow-600 hover:text-yellow-700 text-sm mt-3 flex items-center font-medium">
                                        {{ hasMoreBrands ? 'View More' : 'Show Less' }}
                                        <i
                                            :class="hasMoreBrands ? 'fas fa-chevron-down ml-1' : 'fas fa-chevron-up ml-1'"></i>
                                    </button>
                                </div>
                            </div>

                            <!-- Price Range Filter -->
                            <div class="pb-6">
                                <h3 class="text-lg font-semibold mb-4 flex items-center text-gray-900">
                                    <span class="h-1 w-4 bg-yellow-500 rounded-full mr-2"></span>
                                    Price Range
                                </h3>
                                <div class="space-y-4">
                                    <div class="flex space-x-4">
                                        <div class="flex-1">
                                            <label class="text-sm text-gray-600 block mb-2 font-medium">Min (₱)</label>
                                            <input type="number" v-model.number="priceRange.min" min="0"
                                                placeholder="Min"
                                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent text-sm"
                                                @change="handlePriceChange">
                                        </div>
                                        <div class="flex-1">
                                            <label class="text-sm text-gray-600 block mb-2 font-medium">Max (₱)</label>
                                            <input type="number" v-model.number="priceRange.max" min="0"
                                                placeholder="Max"
                                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent text-sm"
                                                @change="handlePriceChange">
                                        </div>
                                    </div>
                                    <div class="flex justify-end">
                                        <button @click="clearPriceRange" v-if="priceRange.min || priceRange.max"
                                            class="text-sm text-yellow-600 hover:text-yellow-700 font-medium">
                                            Clear Price Range
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <!-- Reset Filters Button -->
                            <button @click="resetFilters"
                                class="w-full bg-black text-white py-3 px-4 rounded-lg hover:bg-gray-800 transition-colors duration-300 flex items-center justify-center space-x-2 font-medium">
                                <i class="fas fa-undo-alt mr-2"></i>
                                <span>Reset All Filters</span>
                            </button>
                        </div>
                    </div>
                </aside>

                <!-- Main Content -->
                <div class="flex-1">
                    <!-- Controls Bar -->
                    <div
                        class="bg-white rounded-xl shadow-md p-4 mb-6 flex flex-col md:flex-row md:justify-between md:items-center gap-4">
                        <div class="flex items-center">
                            <div class="relative group">
                                <button @click="toggleSortDropdown"
                                    class="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors duration-200">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none"
                                        viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                                    </svg>
                                    <span class="text-gray-700 font-medium">Sort: {{ getSortLabel }}</span>
                                    <i :class="sortDropdownOpen ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"
                                        class="text-gray-600"></i>
                                </button>

                                <!-- Dropdown Menu -->
                                <div v-if="sortDropdownOpen"
                                    class="absolute left-0 mt-2 w-48 bg-white rounded-lg shadow-xl z-20 border border-gray-200 overflow-hidden">
                                    <button v-for="option in sortOptions" :key="option.value"
                                        @click="updateSort(option.value)"
                                        class="w-full text-left px-4 py-3 hover:bg-gray-100 flex justify-between items-center border-b border-gray-100 last:border-0 group"
                                        :class="{ 'bg-gray-50': sortBy === option.value && sortDirection === option.direction }">
                                        <span
                                            :class="{ 'text-yellow-600 font-semibold': sortBy === option.value && sortDirection === option.direction }"
                                            class="group-hover:text-yellow-600">
                                            {{ option.label }}
                                        </span>
                                        <span v-if="sortBy === option.value && sortDirection === option.direction"
                                            class="text-yellow-600">
                                            <i
                                                :class="sortDirection === 'asc' ? 'fas fa-sort-amount-up-alt' : 'fas fa-sort-amount-down'"></i>
                                        </span>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div class="flex items-center justify-between md:justify-end w-full md:w-auto">
                            <div class="text-gray-600 font-medium">
                                {{ products.length === 0 ? 'No products' : `${products.length} products found` }}
                            </div>

                            <div class="flex items-center space-x-2 ml-4">
                                <span class="text-gray-600 font-medium hidden sm:inline">
                                    Page {{ products.length === 0 ? '0/0' : `${currentPage}/${totalPages}` }}
                                </span>
                                <div class="flex space-x-2">
                                    <button @click="previousPage" :disabled="currentPage === 1 || products.length === 0"
                                        class="p-2 rounded-lg transition-colors duration-200"
                                        :class="currentPage === 1 || products.length === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-800 text-white hover:bg-yellow-500 hover:text-gray-900'">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                            viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M15 19l-7-7 7-7" />
                                        </svg>
                                    </button>

                                    <button @click="nextPage"
                                        :disabled="currentPage === totalPages || products.length === 0"
                                        class="p-2 rounded-lg transition-colors duration-200"
                                        :class="currentPage === totalPages || products.length === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-800 text-white hover:bg-yellow-500 hover:text-gray-900'">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                            viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M9 5l7 7-7 7" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Loading State -->
                    <div v-if="loading" class="bg-white rounded-xl shadow-md p-12 text-center">
                        <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-yellow-500 mx-auto"></div>
                        <p class="text-gray-600 mt-6 text-lg">Loading amazing products...</p>
                    </div>

                    <!-- No Results State -->
                    <div v-else-if="products.length === 0" class="bg-white rounded-xl shadow-md p-12 text-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <h3 class="text-xl font-bold text-gray-700 mb-2">No Products Found</h3>
                        <p class="text-gray-600 mb-6">Try adjusting your filters or search query</p>
                        <button @click="resetFilters"
                            class="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold px-6 py-2 rounded-lg transition-colors duration-200">
                            Reset Filters
                        </button>
                    </div>

                    <!-- Product Grid -->
                    <div v-else
                        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 auto-rows-max">
                        <div v-for="(product, index) in paginatedProducts" :key="product.product_id"
                            class="group bg-white rounded-xl shadow-md overflow-hidden transform transition-all duration-300 hover:shadow-xl"
                            :class="{ 'animate-fade-in-up-1': index % 4 === 0, 'animate-fade-in-up-2': index % 4 === 1, 'animate-fade-in-up-3': index % 4 === 2, 'animate-fade-in-up-4': index % 4 === 3 }">
                            <router-link :to="'/product/' + product.product_id" @click="scrollToTop">
                                <div class="relative overflow-hidden">
                                    <!-- Out of Stock Badge -->
                                    <div v-if="product.stock === 0"
                                        class="absolute top-0 left-0 bg-red-500 text-white text-xs font-bold uppercase px-3 py-1 rounded-br-lg z-10">
                                        Out of Stock
                                    </div>

                                    <!-- Low Stock Badge -->
                                    <div v-else-if="product.stock < 5"
                                        class="absolute top-0 left-0 bg-orange-500 text-white text-xs font-bold uppercase px-3 py-1 rounded-br-lg z-10">
                                        Low Stock: {{ product.stock }} left
                                    </div>

                                    <div
                                        class="h-48 bg-gray-50 flex items-center justify-center p-4 transition-transform duration-500 group-hover:scale-105">
                                        <img v-if="product.image_url" :src="product.image_url" :alt="product.name"
                                            class="h-full max-w-full object-contain transition-all duration-500">
                                        <div v-else class="w-full h-full flex items-center justify-center bg-gray-100">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-300"
                                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                            </svg>
                                        </div>
                                    </div>
                                    <div
                                        class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent h-16 opacity-0 group-hover:opacity-70 transition-opacity duration-300">
                                    </div>
                                </div>

                                <div class="p-5">
                                    <div class="flex justify-between items-start mb-2">
                                        <p
                                            class="text-xs font-semibold text-yellow-600 bg-yellow-100 px-2 py-1 rounded-full">
                                            {{ product.category_name }}</p>
                                        <p class="text-xs text-gray-500">{{ product.brand }}</p>
                                    </div>

                                    <h3
                                        class="font-bold text-lg mb-3 truncate text-gray-900 group-hover:text-yellow-600 transition-colors">
                                        {{ product.name }}</h3>

                                    <div class="flex justify-between items-center">
                                        <p class="text-xl font-bold text-gray-900">₱{{ product.price.toLocaleString() }}
                                        </p>
                                        <div class="flex items-center">
                                            <span class="text-xs text-gray-600 mr-2">{{ product.sold_products }}
                                                sold</span>
                                            <div
                                                class="px-3 py-1 bg-black text-white text-xs rounded-full transform transition-transform duration-300 group-hover:scale-110 group-hover:bg-yellow-500 group-hover:text-gray-900">
                                                View
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </router-link>
                        </div>
                    </div>

                    <!-- Pagination - Bottom -->
                    <div v-if="products.length > 0" class="flex justify-center mt-8">
                        <div class="flex items-center space-x-1">
                            <button v-for="page in Math.min(totalPages, 5)" :key="page"
                                @click="currentPage = page; scrollToTop()"
                                class="w-10 h-10 flex items-center justify-center rounded-full transition-colors duration-200 text-sm font-medium"
                                :class="currentPage === page ? 'bg-yellow-500 text-gray-900' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'">
                                {{ page }}
                            </button>

                            <span v-if="totalPages > 5" class="px-2 text-gray-600">...</span>

                            <button v-if="totalPages > 5" @click="currentPage = totalPages; scrollToTop()"
                                class="w-10 h-10 flex items-center justify-center rounded-full transition-colors duration-200 text-sm font-medium"
                                :class="currentPage === totalPages ? 'bg-yellow-500 text-gray-900' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'">
                                {{ totalPages }}
                            </button>
                        </div>
                    </div>
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
            displayCategories: [],
            selectedCategories: [],
            selectedBrands: [],
            searchQuery: '',
            currentPage: 1,
            productsPerPage: 16,
            loading: false,
            sortBy: 'sold_products',
            sortDirection: 'desc',
            showAllCategories: false,
            showAllBrands: false,
            sortDropdownOpen: false,
            sortOptions: [
                { label: 'Price: Low to High', value: 'price', direction: 'asc' },
                { label: 'Price: High to Low', value: 'price', direction: 'desc' },
                { label: 'Most Popular', value: 'sold_products', direction: 'desc' },
                { label: 'Newest', value: 'product_id', direction: 'desc' }
            ],
            priceRange: {
                min: null,
                max: null
            },
            pendingFilters: {
                categories: [],
                brands: [],
                priceRange: {
                    min: null,
                    max: null
                }
            },
            uniqueBrands: [],
            visibleCategoryCount: 5,
            visibleBrandCount: 5
        };
    },
    computed: {
        paginatedProducts() {
            const start = (this.currentPage - 1) * this.productsPerPage;
            const end = start + this.productsPerPage;
            return this.products.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.products.length / this.productsPerPage);
        },
        displayedCategories() {
            return this.displayCategories.slice(0, this.visibleCategoryCount);
        },
        displayedBrands() {
            return this.uniqueBrands.slice(0, this.visibleBrandCount);
        },
        getSortLabel() {
            const option = this.sortOptions.find(opt => opt.value === this.sortBy && opt.direction === this.sortDirection);
            return option ? option.label : 'Most Popular';
        },
        hasMoreCategories() {
            return this.visibleCategoryCount < this.displayCategories.length;
        },
        hasMoreBrands() {
            return this.visibleBrandCount < this.uniqueBrands.length;
        }
    },
    watch: {
        '$route.query': {
            immediate: true,
            deep: true,
            handler(newQuery) {
                this.searchQuery = newQuery.search || '';

                // Handle category filtering
                if (newQuery.category) {
                    this.selectedCategories = [Number(newQuery.category)];
                    this.pendingFilters.categories = [Number(newQuery.category)];
                } else if (newQuery.category_name) {
                    // This is for when a category name is passed from the homepage
                    this.handleCategoryNameFilter(newQuery.category_name);
                } else {
                    this.selectedCategories = [];
                    this.pendingFilters.categories = [];
                }

                this.fetchProducts();
            }
        },
        '$route': {
            handler() {
                this.scrollToTop();
            }
        },
        sortDropdownOpen(newVal) {
            if (newVal) {
                const closeDropdown = (e) => {
                    if (!e.target.closest('.relative')) {
                        this.sortDropdownOpen = false;
                        document.removeEventListener('click', closeDropdown);
                    }
                };
                setTimeout(() => {
                    document.addEventListener('click', closeDropdown);
                }, 0);
            }
        }
    },
    methods: {
        async fetchCategories() {
            try {
                const response = await api.get("/category/");
                this.displayCategories = response.data;
            } catch (error) {
                console.error('Error fetching categories:', error);
            }
        },
        async fetchProducts() {
            this.loading = true;
            const params = new URLSearchParams();

            // Text search for product name
            if (this.searchQuery) {
                params.append('search', this.searchQuery);
            }

            // Check for category_name in URL query
            const categoryNameFromQuery = this.$route.query.category_name;

            // Multiple category filter
            if (this.selectedCategories.length > 0) {
                const selectedCategoryNames = this.selectedCategories
                    .map(categoryId => {
                        const category = this.displayCategories.find(cat => cat.category_id === categoryId);
                        return category ? category.category_name : null;
                    })
                    .filter(name => name !== null);

                selectedCategoryNames.forEach(categoryName => {
                    params.append('category', categoryName);
                });
            }
            // If no categories are selected but we have a category_name in the URL
            else if (categoryNameFromQuery && !this.$route.query.category) {
                params.append('category', categoryNameFromQuery);
            }

            // Multiple brand filter
            if (this.selectedBrands.length > 0) {
                this.selectedBrands.forEach(brand => {
                    params.append('brand', brand);
                });
            }

            if (this.priceRange.min !== null && this.priceRange.min !== '') {
                params.append('min_price', this.priceRange.min);
            }
            if (this.priceRange.max !== null && this.priceRange.max !== '') {
                params.append('max_price', this.priceRange.max);
            }

            let orderingField = this.sortBy;
            if (this.sortDirection === 'desc') {
                orderingField = `-${orderingField}`;
            }
            params.append('ordering', orderingField);

            try {
                const response = await api.get(`/products/?${params.toString()}`);
                this.products = response.data;
                this.currentPage = 1;

                this.uniqueBrands = [...new Set(response.data.map(product => product.brand))];
            } catch (error) {
                console.error("Error fetching products:", error);
            } finally {
                this.loading = false;
                this.scrollToTop();
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                this.scrollToTop();
            }
        },
        previousPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.scrollToTop();
            }
        },
        updateSort(value) {
            const option = this.sortOptions.find(opt => opt.value === value);
            if (option) {
                this.sortBy = option.value;
                this.sortDirection = option.direction;
                this.sortDropdownOpen = false;
                this.fetchProducts();
            }
        },
        toggleCategories() {
            if (this.visibleCategoryCount === 5) {
                this.visibleCategoryCount = this.displayCategories.length;
            } else {
                this.visibleCategoryCount = 5;
            }
        },
        toggleBrands() {
            if (this.visibleBrandCount === 5) {
                this.visibleBrandCount = this.uniqueBrands.length;
            } else {
                this.visibleBrandCount = 5;
            }
        },
        toggleSortDropdown() {
            this.sortDropdownOpen = !this.sortDropdownOpen;
        },
        async handleCategoryNameFilter(categoryName) {
            // First make sure categories are loaded
            if (this.displayCategories.length === 0) {
                await this.fetchCategories();
            }

            // Find the category ID that matches the name
            const category = this.displayCategories.find(
                cat => cat.category_name.toLowerCase() === categoryName.toLowerCase()
            );

            if (category) {
                this.selectedCategories = [category.category_id];
                this.pendingFilters.categories = [category.category_id];
            } else {
                console.warn(`Category with name "${categoryName}" not found`);
                this.selectedCategories = [];
                this.pendingFilters.categories = [];
            }
        },
        handlePriceChange() {
            let min = parseFloat(this.priceRange.min);
            let max = parseFloat(this.priceRange.max);

            // Handle NaN cases
            if (isNaN(min)) min = null;
            if (isNaN(max)) max = null;

            // Ensure min doesn't exceed max
            if (min !== null && max !== null && min > max) {
                this.priceRange.max = this.priceRange.min;
            }

            // Ensure non-negative values
            if (min !== null && min < 0) this.priceRange.min = 0;
            if (max !== null && max < 0) this.priceRange.max = 0;

            this.fetchProducts();
        },
        clearPriceRange() {
            this.priceRange.min = null;
            this.priceRange.max = null;
            this.fetchProducts();
        },
        applyFilters() {
            this.pendingFilters = {
                categories: [...this.selectedCategories],
                brands: [...this.selectedBrands],
                priceRange: {
                    min: this.priceRange.min,
                    max: this.priceRange.max
                }
            };
            this.fetchProducts();
        },
        resetFilters() {
            this.selectedCategories = [];
            this.selectedBrands = [];
            this.priceRange = {
                min: null,
                max: null
            };
            this.sortBy = 'sold_products';
            this.sortDirection = 'desc';
            this.pendingFilters = {
                categories: [],
                brands: [],
                priceRange: {
                    min: null,
                    max: null
                }
            };
            this.fetchProducts();
        },
        closeDropdown(e) {
            if (!e.target.closest('.relative')) {
                this.sortDropdownOpen = false;
            }
        },
        scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    },
    created() {
        this.fetchCategories();
        this.scrollToTop();
    },
    mounted() {
        document.addEventListener('click', this.closeDropdown);
        this.scrollToTop();
    },
    beforeUnmount() {
        document.removeEventListener('click', this.closeDropdown);
    }
};
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css");

.z-10 {
    z-index: 10;
}

.z-20 {
    z-index: 20;
}

.scrollbar {
    scrollbar-width: thin;
    scrollbar-color: #d1d5db transparent;
}

.scrollbar::-webkit-scrollbar {
    width: 6px;
}

.scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.scrollbar::-webkit-scrollbar-thumb {
    background-color: #d1d5db;
    border-radius: 6px;
}

.scrollbar::-webkit-scrollbar-thumb:hover {
    background-color: #9ca3af;
}

.animate-fade-in-up-1 {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease-out 0.1s forwards;
}

.animate-fade-in-up-2 {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease-out 0.2s forwards;
}

.animate-fade-in-up-3 {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease-out 0.3s forwards;
}

.animate-fade-in-up-4 {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease-out 0.4s forwards;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
