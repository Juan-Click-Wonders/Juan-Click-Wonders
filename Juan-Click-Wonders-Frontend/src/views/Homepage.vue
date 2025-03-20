<template>
    <div class="bg-white">
        <div class="container mx-auto px-4 py-12">
            <div class="flex flex-col md:flex-row items-center justify-between gap-8">
                <div class="flex flex-col items-center md:items-start space-y-4 md:w-1/2">
                    <h2 class="text-5xl font-bold">
                        Get top-tier performance without breaking the bank.
                    </h2>
                    <p class="text-lg">Price starting at ₱65,000</p>
                    <button
                        class="bg-black text-white !px-8 !py-3 rounded-md font-semibold hover:bg-gray-800 transition-colors">
                        <router-link :to="`/product/14`">BUY NOW</router-link>
                    </button>
                </div>

                <div class="w-1/2">
                    <h1 class="text-4xl font-bold mb-6 text-center">
                        AMD Radeon RX 6800 XT
                    </h1>
                    <img src="https://www.amd.com/content/dam/amd/en/images/products/graphics/radeon-rx-9070/2922918-radeon-rx-9070xt-product.jpg"
                        alt="AMD Radeon RX 9070 XT Graphics Card" class="w-full h-auto object-contain" />
                </div>
            </div>
        </div>
        <div class="bg-gray-100 text-gray-900 py-16" v-if="!loading && topProducts.length > 0">
            <div class="container mx-auto px-4">
                <h2 class="text-4xl font-bold mb-8 text-center">Best Sellers</h2>
                <div class="relative">
                    <div class="overflow-hidden">
                        <div class="flex transition-transform duration-500 ease-in-out"
                            :style="{ transform: `translateX(-${currentSlide * 25}%)` }">
                            <div v-for="product in topProducts" :key="product.id" class="w-1/4 flex-shrink-0 px-2">
                                <router-link :to="`/product/${product.id}`"
                                    class="block bg-white rounded-lg p-4 transform hover:scale-105 transition-transform duration-300 h-full shadow-md">
                                    <div class="h-36 flex items-center justify-center mb-3">
                                        <img v-if="product.image_url" :src="product.image_url" :alt="product.name"
                                            class="h-full w-full object-contain" />
                                    </div>
                                    <div class="text-center">
                                        <p class="text-sm text-gray-600 mb-1">{{ product.category_name }}</p>
                                        <h3 class="font-bold text-base mb-2 truncate text-gray-900">{{ product.name }}
                                        </h3>
                                        <p class="text-lg font-semibold text-yellow-600">₱{{
                            product.price.toLocaleString() }}</p>
                                        <p class="text-xs text-gray-600 mt-1">{{ product.sold_products }} units sold</p>
                                    </div>
                                </router-link>
                            </div>
                        </div>
                    </div>
                    <button @click="prevSlide"
                        class="absolute left-0 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 p-2 rounded-r hover:bg-opacity-75">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7">
                            </path>
                        </svg>
                    </button>
                    <button @click="nextSlide"
                        class="absolute right-0 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 p-2 rounded-l hover:bg-opacity-75">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7">
                            </path>
                        </svg>
                    </button>
                    <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 flex space-x-2 mb-4">
                        <button v-for="(_, index) in topProducts" :key="index" @click="goToSlide(index)"
                            class="w-2 h-2 rounded-full transition-colors duration-200"
                            :class="currentSlide === index ? 'bg-white' : 'bg-gray-500'"></button>
                    </div>
                </div>
            </div>
        </div>

        <div class="bg-gray-50 py-16">
            <div class="container mx-auto px-4">
                <div class="text-center mb-12">
                    <h2 class="text-4xl font-bold mb-4">Featured Products</h2>
                    <p class="text-gray-600">Discover our top-rated gaming hardware</p>
                </div>

                <div v-if="loading" class="text-center py-8">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
                </div>

                <div v-else>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
                        <router-link v-for="product in featuredProducts" :key="product.id"
                            :to="`/product/${product.id}`"
                            class="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden">
                            <div class="h-48 bg-white flex items-center justify-center p-4">
                                <img v-if="product.image_url" :src="product.image_url" :alt="product.name"
                                    class="h-full w-full object-contain" />
                            </div>
                            <div class="p-4">
                                <h3 class="font-bold text-lg mb-2 truncate">{{ product.name }}</h3>
                                <p class="text-gray-900 font-semibold">₱{{ product.price.toLocaleString() }}</p>
                                <p class="text-sm text-gray-600 mt-2">{{ product.category_name }}</p>
                            </div>
                        </router-link>
                    </div>

                    <div class="text-center">
                        <router-link to="/product_list"
                            class="inline-block bg-black text-white px-8 py-3 rounded-md font-semibold hover:bg-gray-800 transition-colors">
                            View All Products
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            featuredProducts: [],
            topProducts: [],
            loading: true,
            currentSlide: 0,
            autoSlideInterval: null
        };
    },
    methods: {
        prevSlide() {
            if (this.currentSlide > 0) {
                this.currentSlide--;
            } else {
                this.currentSlide = this.topProducts.length - 4;
            }
            this.resetAutoSlide();
        },
        nextSlide() {
            if (this.currentSlide < this.topProducts.length - 4) {
                this.currentSlide++;
            } else {
                this.currentSlide = 0;
            }
            this.resetAutoSlide();
        },
        goToSlide(index) {
            this.currentSlide = index;
            this.resetAutoSlide();
        },
        startAutoSlide() {
            this.autoSlideInterval = setInterval(() => {
                this.nextSlide();
            }, 3000);
        },
        resetAutoSlide() {
            if (this.autoSlideInterval) {
                clearInterval(this.autoSlideInterval);
                this.startAutoSlide();
            }
        }
    },
    mounted() {
        this.startAutoSlide();
    },
    beforeDestroy() {
        if (this.autoSlideInterval) {
            clearInterval(this.autoSlideInterval);
        }
    },
    async created() {
        try {
            const [productsResponse, topProductsResponse] = await Promise.all([
                axios.get('http://127.0.0.1:8000/products/'),
                axios.get('http://127.0.0.1:8000/products/?ordering=-sold_products')
            ]);

            this.featuredProducts = productsResponse.data.slice(0, 8);

            const categoriesMap = new Map();
            for (const product of topProductsResponse.data) {
                if (!categoriesMap.has(product.category_name)) {
                    categoriesMap.set(product.category_name, []);
                }
                categoriesMap.get(product.category_name).push(product);
            }

            this.topProducts = Array.from(categoriesMap.entries())
                .map(([_, products]) => products[0])
                .filter(product => product);

            this.loading = false;
        } catch (error) {
            console.error('Error fetching products:', error);
            this.loading = false;
        }
    }
};
</script>