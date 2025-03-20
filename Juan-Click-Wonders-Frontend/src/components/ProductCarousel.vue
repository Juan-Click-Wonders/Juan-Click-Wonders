<template>
    <div class="relative">
        <div class="overflow-hidden relative">
            <div class="flex transition-transform duration-500 ease-in-out"
                :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
                <div v-for="(categoryProducts, index) in categorizedProducts" :key="index" class="w-full flex-shrink-0">
                    <h3 class="text-2xl font-semibold text-gray-200 mb-6 text-center">{{ categoryProducts.category }}
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        <router-link v-for="product in categoryProducts.products" :key="product.id"
                            :to="`/product/${product.id}`"
                            class="bg-gray-800 rounded-lg p-6 transform hover:scale-105 transition-transform duration-300">
                            <div class="h-48 flex items-center justify-center mb-4">
                                <img v-if="product.image_url" :src="product.image_url" :alt="product.name"
                                    class="h-full w-full object-contain" />
                            </div>
                            <div class="text-center">
                                <h3 class="font-bold text-lg mb-2 truncate">{{ product.name }}</h3>
                                <p class="text-xl font-semibold text-yellow-400">₱{{ product.price.toLocaleString() }}
                                </p>
                                <p class="text-sm text-gray-400 mt-2">{{ product.sold_products }} units sold</p>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
        <button @click="prevSlide"
            class="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-4 bg-gray-800 text-white rounded-full p-2 hover:bg-gray-700 transition-colors"
            :class="{ 'opacity-50 cursor-not-allowed': currentIndex === 0 }">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
        </button>
        <button @click="nextSlide"
            class="absolute right-0 top-1/2 transform -translate-y-1/2 translate-x-4 bg-gray-800 text-white rounded-full p-2 hover:bg-gray-700 transition-colors"
            :class="{ 'opacity-50 cursor-not-allowed': currentIndex === categorizedProducts.length - 1 }">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
        </button>

        <!-- Dots Navigation -->
        <div class="flex justify-center mt-4 space-x-2">
            <button v-for="(_, index) in categorizedProducts" :key="index" @click="goToSlide(index)"
                class="w-3 h-3 rounded-full transition-colors duration-200"
                :class="index === currentIndex ? 'bg-white' : 'bg-gray-600 hover:bg-gray-500'">
            </button>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        products: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            currentIndex: 0,
            autoplayInterval: null
        };
    },
    computed: {
        categorizedProducts() {
            const categories = {};
            this.products.forEach(product => {
                if (!categories[product.category_name]) {
                    categories[product.category_name] = {
                        category: product.category_name,
                        products: []
                    };
                }
                categories[product.category_name].products.push(product);
            });
            return Object.values(categories);
        }
    },
    methods: {
        startAutoplay() {
            this.autoplayInterval = setInterval(() => {
                this.nextSlide();
            }, 5000);
        },
        stopAutoplay() {
            if (this.autoplayInterval) {
                clearInterval(this.autoplayInterval);
            }
        },
        prevSlide() {
            if (this.currentIndex > 0) {
                this.currentIndex--;
            }
        },
        nextSlide() {
            if (this.currentIndex < this.categorizedProducts.length - 1) {
                this.currentIndex++;
            } else {
                this.currentIndex = 0;
            }
        },
        goToSlide(index) {
            this.currentIndex = index;
        }
    },
    mounted() {
        this.startAutoplay();
    },
    beforeDestroy() {
        this.stopAutoplay();
    }
};
</script>