<template>
    <div class="w-full mx-auto mt-8">
        <div class="flex rounded-xl mx-4">
            <aside class="w-64 p-4 border-black border-2 rounded-xl h-fit mb-4">
                <!-- Sidebar -->
                <div class="mb-6">
                    <h2 class="text-xl font-semibold mb-2">Filter by Category</h2>
                    <div class="space-y-2">
                        <div v-for="category in displayedCategories" :key="category.category_id">
                            <label class="flex items-center space-x-2">
                                <input type="checkbox" v-model="selectedCategories" :value="category.category_id"
                                    @change="applyFilters">
                                <span>{{ category.category_name }}</span>
                            </label>
                        </div>
                        <button v-if="displayCategories.length > 5" @click="toggleCategories" class="text-blue-600 hover:text-blue-800 text-sm mt-2 flex items-center">
                            {{ hasMoreCategories ? 'View More' : 'Show Less' }}
                            <i :class="hasMoreCategories ? 'fas fa-chevron-down ml-1' : 'fas fa-chevron-up ml-1'"></i>
                        </button>
                    </div>
                </div>
                <div class="mb-6">
                    <h2 class="text-xl font-semibold mb-2">Filter by Brand</h2>
                    <div class="space-y-2">
                        <div v-for="brand in displayedBrands" :key="brand">
                            <label class="flex items-center space-x-2">
                                <input type="checkbox" v-model="selectedBrands" :value="brand" @change="applyFilters">
                                <span>{{ brand }}</span>
                            </label>
                        </div>
                        <button v-if="uniqueBrands.length > 5"@click="toggleBrands" class="text-blue-600 hover:text-blue-800 text-sm mt-2 flex items-center">
                            {{ hasMoreBrands ? 'View More' : 'Show Less' }}
                            <i :class="hasMoreBrands ? 'fas fa-chevron-down ml-1' : 'fas fa-chevron-up ml-1'"></i>
                        </button>
                    </div>
                </div>
                <div class="mb-6">
                    <h2 class="text-xl font-semibold mb-2">Price Range</h2>
                    <div class="space-y-4">
                        <div class="flex space-x-2">
                            <div class="flex-1">
                                <label class="text-sm text-gray-600 block mb-1">Min (₱)</label>
                                <input type="number" v-model.number="priceRange.min" min="0" placeholder="Min" class="w-full px-2 py-1.5 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" @change="handlePriceChange">
                            </div>
                            <div class="flex-1">
                                <label class="text-sm text-gray-600 block mb-1">Max (₱)</label>
                                <input type="number" v-model.number="priceRange.max" min="0" placeholder="Max" class="w-full px-2 py-1.5 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" @change="handlePriceChange">
                            </div>
                        </div>
                        <div class="flex justify-between items-center">
                            <button @click="clearPriceRange" v-if="priceRange.min || priceRange.max" class="text-sm text-blue-600 hover:text-blue-800">Clear</button>
                        </div>
                    </div>
                </div>
                <button @click="resetFilters" class="w-full border-2 border-gray-300 text-gray-600 py-2 px-4 rounded-lg hover:bg-gray-50 transition-colors duration-200 flex items-center justify-center space-x-2">
                    <i class="fas fa-undo"></i>
                    <span>Reset Filters</span>
                </button>
            </aside>

            <!-- Main Content  -->
            <div class="flex-1 flex flex-col ml-6">
                <div class="bg-white shadow-sm p-4 mb-4 flex justify-between items-center rounded-lg">
                    <div class="text-gray-700 ml-2">
                        <span v-if="searchQuery" class="font-medium">
                            Search Results for "{{ searchQuery }}"
                        </span>
                        <span v-else class="font-medium">
                            All Products
                        </span>
                    </div>
                    <div class="flex items-center space-x-6 mr-2">
                        <div class="relative">
                            <button @click="toggleSortDropdown" 
                                class="flex items-center space-x-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
                            >
                                <span>Sort By: {{ getSortLabel }}</span>
                                <i :class="sortDropdownOpen ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
                            </button>
                            
                            <!-- Dropdown Menu -->
                            <div v-if="sortDropdownOpen" 
                                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg z-10 border"
                            >
                                <button 
                                    v-for="option in sortOptions" 
                                    :key="option.value"
                                    @click="updateSort(option.value)"
                                    class="w-full text-left px-4 py-2 hover:bg-gray-100 flex justify-between items-center"
                                    :class="{ 'font-semibold': sortBy === option.value }"
                                >
                                    {{ option.label }}
                                    <span v-if="sortBy === option.value">
                                        <i :class="sortDirection === 'asc' ? 'fas fa-sort-numeric-down' : 'fas fa-sort-numeric-up'"></i>
                                    </span>
                                </button>
                            </div>
                        </div>
                        <div class="flex items-center space-x-2">
                            <span class="text-gray-700 font-medium">
                                {{ products.length === 0 ? '0/0' : `${currentPage}/${totalPages}` }}
                            </span>
                            <div class="flex space-x-1">
                                <button @click="previousPage" :disabled="currentPage === 1 || products.length === 0" class="px-2 py-1 bg-blue-500 text-white rounded-lg disabled:bg-gray-300 hover:bg-blue-600" :style="{ cursor: currentPage === 1 || products.length === 0 ? 'not-allowed' : 'pointer', pointerEvents: currentPage === 1 || products.length === 0 ? 'none' : 'auto' }">
                                    <i class="fas fa-chevron-left text-sm"></i>
                                </button>

                                <button @click="nextPage" :disabled="currentPage === totalPages || products.length === 0" class="px-2 py-1 bg-blue-500 text-white rounded-lg disabled:bg-gray-300 hover:bg-blue-600" :style="{ cursor: currentPage === totalPages || products.length === 0 ? 'not-allowed' : 'pointer', pointerEvents: currentPage === totalPages || products.length === 0 ? 'none' : 'auto' }">
                                    <i class="fas fa-chevron-right text-sm"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 p-6 auto-rows-max">
                    <router-link v-for="product in paginatedProducts" :key="product.product_id" :to="'/product/' + product.product_id" class="block border p-4 rounded-lg shadow-md bg-white hover:shadow-lg transition-transform transform hover:scale-105 h-fit">
                        <div class="h-40 bg-white flex items-center justify-center">
                            <img v-if="product.image_url" :src="product.image_url" :alt="product.name" class="max-h-full max-w-full object-contain">
                        </div>
                        <div class="mt-4">
                            <h3 class="font-bold truncate">{{ product.name }}</h3>
                            <p class="text-gray-700 font-semibold">₱{{ product.price.toLocaleString() }}</p>
                            <p class="text-sm text-gray-600">Category: {{ product.category_name }}</p>
                            <p class="text-sm text-gray-600">Brand: {{ product.brand }}</p>
                            <p class="text-sm text-gray-600">Stock: {{ product.stock }}</p>
                            <p class="text-sm text-gray-600">Sold: {{ product.sold_products }}</p>
                        </div>
                    </router-link>
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
            productsPerPage: 20,
            loading: false,
            sortBy: 'sold_products',
            sortDirection: 'desc',
            showAllCategories: false,
            showAllBrands: false,
            sortDropdownOpen: false,
            sortOptions: [
                { label: 'Price', value: 'price' },
                { label: 'Most Sold', value: 'sold_products' }
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
            const option = this.sortOptions.find(opt => opt.value === this.sortBy);
            return option ? option.label : 'Price';
        },
        hasMoreCategories() {
            return this.visibleCategoryCount < this.displayCategories.length;
        },
        hasMoreBrands() {
            return this.visibleBrandCount < this.uniqueBrands.length;
        },
        getSortIcon(value) {
            if (this.sortBy !== value) return '';
            return this.sortDirection === 'asc' ? 'fas fa-sort-numeric-down' : 'fas fa-sort-numeric-up';
        }
    },
    watch: {
        '$route.query': {
            immediate: true,
            deep: true,
            handler(newQuery) {
                this.searchQuery = newQuery.search || '';
                if (newQuery.category) {
                    this.selectedCategories = [Number(newQuery.category)];
                    this.pendingFilters.categories = [Number(newQuery.category)];
                } else {
                    this.selectedCategories = [];
                    this.pendingFilters.categories = [];
                }
                this.fetchProducts();
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
            }
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
        updateSort(value) {
            if (this.sortBy === value) {
                this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortBy = value;
                this.sortDirection = value === 'sold_products' ? 'desc' : 'asc';
            }
            this.sortDropdownOpen = false;
            this.fetchProducts();
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
        }
    },
    created() {
        this.fetchCategories();
    },
    mounted() {
        document.addEventListener('click', this.closeDropdown);
    },
    beforeUnmount() {
        document.removeEventListener('click', this.closeDropdown);
    }
};
</script>

<style>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css");
.z-10 {
    z-index: 10;
}
</style>
