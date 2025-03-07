<template>
    <div class="w-full mx-auto flex">
        <!-- Sidebar (Category Filter) -->
        <aside class="w-1/4 p-4">
            <h2 class="text-xl font-semibold mb-2">Filter by Category</h2>
            <div v-for="category in categories" :key="category">
                <label class="flex items-center space-x-2">
                    <input type="checkbox" v-model="selectedCategories" :value="category" @change="filterProducts">
                    <span>{{ category }}</span>
                </label>
            </div>
        </aside>

        <!-- Product Grid -->
        <div class="flex-1 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4 p-6">
            <router-link v-for="product in filteredProducts" :key="product.id" :to="'/product/' + product.id"
                class="block border p-8 rounded-lg shadow-md bg-white hover:shadow-lg transition-transform transform hover:scale-105 w-full">
                <!-- Placeholder for Product Image -->
                <div class="h-40 bg-gray-300 flex items-center justify-center">
                    <img :src="product.image" :alt="product.title" class="max-h-full max-w-full">
                </div>

                <!-- Product Details -->
                <h3 class="mt-2 font-bold">{{ product.title }}</h3>
                <p class="text-gray-700 font-semibold">₱{{ product.price }}</p>

                <!-- Ratings -->
                <div class="flex items-center text-yellow-500">
                    <span v-for="star in 5" :key="star">
                        <i v-if="star <= Math.round(product.rating.rate)" class="fas fa-star"></i>
                        <i v-else class="far fa-star"></i>
                    </span>
                    <span class="ml-2 text-gray-500">({{ product.rating.count }})</span>
                </div>
            </router-link>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            products: [],
            categories: [],
            selectedCategories: [],
        };
    },
    computed: {
        filteredProducts() {
            if (this.selectedCategories.length === 0) {
                return this.products;
            }
            return this.products.filter(product =>
                this.selectedCategories.includes(product.category)
            );
        }
    },
    methods: {
        fetchProducts() {
            axios.get("https://fakestoreapi.com/products")
                .then(response => {
                    this.products = response.data;
                    this.extractCategories();
                })
                .catch(error => console.error("Error fetching products:", error));
        },
        extractCategories() {
            this.categories = [...new Set(this.products.map(p => p.category))];
        },
        filterProducts() {
            this.$forceUpdate();
        }
    },
    created() {
        this.fetchProducts();
    }
};
</script>

<style>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css");
</style>
