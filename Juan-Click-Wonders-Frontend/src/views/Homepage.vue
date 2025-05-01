<template>
    <div class="bg-white overflow-hidden">
        <!-- Hero Section with Animation -->
        <div class="relative bg-gradient-to-r from-gray-900 to-gray-800 overflow-hidden">
            <div class="absolute inset-0 bg-pattern opacity-10"></div>
            <div class="container mx-auto px-4 py-16 md:py-24 relative z-10">
                <div class="flex flex-col md:flex-row items-center justify-between gap-12">
                    <div class="flex flex-col items-center md:items-start space-y-6 md:w-1/2 animate-fade-in">
                        <h2 class="text-4xl md:text-6xl font-bold text-white leading-tight">
                            Get top-tier <span class="text-yellow-400">performance</span> without breaking the bank
                        </h2>
                        <p class="text-xl text-gray-300">Price starting at ₱65,000</p>
                        <div class="flex space-x-4">
                            <router-link :to="`/product/14`"
                                class="bg-yellow-500 text-gray-900 px-8 py-3 rounded-lg font-semibold hover:bg-yellow-400 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl">
                                BUY NOW
                            </router-link>
                        </div>
                    </div>

                    <div class="md:w-1/2 animate-float">
                        <div
                            class="relative transform hover:scale-105 transition-transform duration-500 cursor-pointer">
                            <div
                                class="absolute -inset-1 bg-gradient-to-r from-yellow-400 to-red-500 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-1000 group-hover:duration-200">
                            </div>
                            <div class="relative bg-gray-900 rounded-lg p-6">
                                <h1 class="text-3xl font-bold mb-4 text-center text-white">
                                    AMD Radeon RX 6800 XT
                                </h1>
                                <img src="https://www.amd.com/content/dam/amd/en/images/products/graphics/radeon-rx-9070/2922918-radeon-rx-9070xt-product.jpg"
                                    alt="AMD Radeon RX 9070 XT Graphics Card"
                                    class="w-full h-auto object-contain rounded-lg transform transition-all duration-500 hover:scale-105 hover:rotate-1" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Category Highlights -->
        <div class="bg-white py-16">
            <div class="container mx-auto px-4">
                <div class="flex flex-col items-center mb-12">
                    <h2 class="text-3xl md:text-4xl font-bold mb-3 relative">
                        <span class="bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-700">Shop By
                            Category</span>
                    </h2>
                    <div class="h-1 w-24 bg-yellow-500 rounded-full mb-6"></div>
                    <p class="text-gray-600 text-center max-w-2xl">Find the perfect hardware for your gaming setup</p>
                </div>

                <!-- Loading state for categories -->
                <div v-if="categoriesLoading" class="grid grid-cols-2 md:grid-cols-4 gap-6">
                    <div v-for="i in 4" :key="i" class="h-48 bg-gray-200 rounded-lg animate-pulse">
                        <div class="h-full flex items-center justify-center">
                            <div class="w-16 h-16 bg-gray-300 rounded-full"></div>
                        </div>
                    </div>
                </div>

                <!-- Categories grid -->
                <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-6">
                    <div v-for="(category, index) in categories" :key="index"
                        class="group relative overflow-hidden rounded-lg shadow-lg transform transition-all duration-300 hover:scale-105 hover:shadow-xl">
                        <div
                            class="absolute inset-0 bg-gradient-to-br from-gray-900 to-gray-800 opacity-90 group-hover:opacity-80 transition-opacity duration-300">
                        </div>
                        <router-link :to="{ path: '/product_list', query: { category_name: category.name } }"
                            class="block h-48 w-full">
                            <div class="absolute inset-0 flex flex-col items-center justify-center p-4">
                                <div
                                    class="w-16 h-16 mb-4 flex items-center justify-center bg-yellow-500 rounded-full text-gray-900 transform transition-transform duration-300 group-hover:scale-110">
                                    <i v-if="category.icon" :class="['fas', category.icon]" class="text-xl"></i>
                                    <svg v-else class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                        stroke-width="2">
                                        <rect x="4" y="6" width="16" height="12" rx="1" />
                                        <path d="M7 6v12" />
                                        <path d="M10 6v12" />
                                        <path d="M13 6v12" />
                                        <path d="M16 6v12" />
                                        <path d="M4 10h16" />
                                        <path d="M4 14h16" />
                                    </svg>
                                </div>
                                <h3 class="font-bold text-lg mb-1 text-white text-center">{{ category.name }}</h3>
                                <p class="text-gray-300 text-sm text-center">Shop Now</p>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>

        <!-- Best Sellers Section -->
        <div class="bg-gradient-to-b from-gray-100 to-white text-gray-900 py-16"
            v-if="!loading && topProducts.length > 0">
            <div class="container mx-auto px-4">
                <div class="flex flex-col items-center mb-12">
                    <h2 class="text-3xl md:text-4xl font-bold mb-3 relative">
                        <span class="bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-700">Best
                            Sellers</span>
                    </h2>
                    <div class="h-1 w-24 bg-yellow-500 rounded-full mb-6"></div>
                    <p class="text-gray-600 text-center max-w-2xl">Our most popular products based on actual sales data</p>
                </div>

                <div class="relative">
                    <div class="overflow-hidden rounded-xl">
                        <div class="flex transition-transform duration-700 ease-out"
                            :style="{ transform: `translateX(-${currentSlide * 25}%)` }">
                            <div v-for="product in topProducts" :key="product.product_id"
                                class="w-full md:w-1/2 lg:w-1/4 flex-shrink-0 px-3 py-4">
                                <router-link :to="`/product/${product.product_id}`"
                                    class="block bg-white rounded-xl overflow-hidden transform hover:scale-105 transition-all duration-300 h-full shadow-md hover:shadow-xl">
                                    <div class="relative">
                                        <div v-if="product.image_url" class="product-image-container h-48 p-4">
                                            <img :src="product.image_url" :alt="product.name"
                                                class="h-full max-w-full transition-transform duration-300 hover:scale-110" />
                                        </div>
                                        <div v-else class="h-48 bg-gray-100 flex items-center justify-center">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400"
                                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                            </svg>
                                        </div>
                                    </div>
                                    <div class="p-4">
                                        <p class="text-xs text-gray-500 mb-1 uppercase tracking-wider">{{
                                            product.category_name }}</p>
                                        <h3
                                            class="font-bold text-lg mb-2 truncate text-gray-900 hover:text-yellow-600 transition-colors">
                                            {{ product.name }}</h3>
                                        <div class="flex justify-between items-center">
                                            <p class="text-xl font-bold text-yellow-600">₱{{
                                                product.price.toLocaleString() }}</p>
                                            <p class="text-xs text-gray-500">
                                                <span class="text-gray-500">{{ product.sold_products
                                                }}</span> sold
                                            </p>
                                        </div>
                                    </div>
                                </router-link>
                            </div>
                        </div>
                    </div>

                    <button @click="prevSlide"
                        class="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-1 bg-white text-gray-900 p-3 rounded-full shadow-lg hover:bg-yellow-500 transition-colors z-10">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7">
                            </path>
                        </svg>
                    </button>

                    <button @click="nextSlide"
                        class="absolute right-0 top-1/2 transform -translate-y-1/2 translate-x-1 bg-white text-gray-900 p-3 rounded-full shadow-lg hover:bg-yellow-500 transition-colors z-10">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7">
                            </path>
                        </svg>
                    </button>

                    <div class="flex justify-center mt-8 space-x-2">
                        <button v-for="index in totalSlides" :key="index-1"
                            @click="goToSlide(index-1)" class="w-3 h-3 rounded-full transition-all duration-300"
                            :class="currentSlide === (index-1) ? 'bg-yellow-500 scale-125' : 'bg-gray-300 hover:bg-gray-400'">
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Featured Products Section -->
        <div class="bg-gray-50 py-16">
            <div class="container mx-auto px-4">
                <div class="flex flex-col items-center mb-12">
                    <h2 class="text-3xl md:text-4xl font-bold mb-3 relative">
                        <span class="bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-700">Featured
                            Products</span>
                    </h2>
                    <div class="h-1 w-24 bg-yellow-500 rounded-full mb-6"></div>
                    <p class="text-gray-600 text-center max-w-2xl">Discover our top-rated gaming hardware</p>
                </div>

                <div v-if="loading" class="text-center py-12">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-4 border-yellow-500 mx-auto"></div>
                    <p class="mt-4 text-gray-600">Loading amazing products...</p>
                </div>

                <div v-else>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
                        <div v-for="(product, index) in featuredProducts" :key="product.product_id"
                            class="group bg-white rounded-xl shadow-md overflow-hidden transform transition-all duration-500 hover:shadow-2xl"
                            :class="{ 'animate-fade-in-up-1': index < 2, 'animate-fade-in-up-2': index >= 2 && index < 4, 'animate-fade-in-up-3': index >= 4 }">
                            <router-link :to="`/product/${product.product_id}`">
                                <div class="relative overflow-hidden">
                                    <div v-if="product.image_url"
                                        class="product-image-container h-44 p-5 transition-transform duration-500 group-hover:scale-105">
                                        <img :src="product.image_url" :alt="product.name"
                                            class="h-full w-full transition-all duration-500" />
                                    </div>
                                    <div v-else class="h-44 bg-gray-100 flex items-center justify-center">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400"
                                            fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                        </svg>
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
                                        <div class="flex items-center space-x-1">
                                            <span class="text-xs text-gray-500">{{ product.sold_products }} sold</span>
                                        </div>
                                    </div>
                                    <h3
                                        class="font-bold text-lg mb-3 truncate text-gray-900 group-hover:text-yellow-600 transition-colors">
                                        {{ product.name }}</h3>
                                    <div class="flex justify-between items-center">
                                        <p class="text-xl font-bold text-gray-900">₱{{ product.price.toLocaleString() }}
                                        </p>
                                        <div
                                            class="px-3 py-1 bg-black text-white text-xs rounded-full transform transition-transform duration-300 group-hover:scale-110 group-hover:bg-yellow-500 group-hover:text-gray-900">
                                            View Details
                                        </div>
                                    </div>
                                </div>
                            </router-link>
                        </div>
                    </div>

                    <div class="text-center">
                        <router-link to="/product_list"
                            class="inline-block bg-black text-white px-10 py-4 rounded-lg font-semibold hover:bg-yellow-500 hover:text-gray-900 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg">
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
            autoSlideInterval: null,
            isIntersecting: false,
            categories: [],
            categoriesLoading: true
        };
    },
    computed: {
        // Calculate the total number of slides based on product count
        totalSlides() {
            // If products can be viewed 4 at a time (25% each), we need to calculate the number of possible slides
            if (!this.topProducts || this.topProducts.length === 0) return 0;
            
            // For products that can be displayed 4 at a time, calculate total slide positions
            // If we have 10 products, we need 7 slide positions (0-6)
            // Consider the edge case if there are fewer than 4 products
            return Math.max(1, this.topProducts.length - Math.min(this.topProducts.length, 4) + 1);
        },
        // Calculate whether we're on the last slide
        isLastSlide() {
            return this.currentSlide >= this.totalSlides - 1;
        }
    },
    methods: {
        prevSlide() {
            if (this.currentSlide > 0) {
                this.currentSlide--;
            } else {
                // Loop to the end when pressing previous on the first slide
                this.currentSlide = this.totalSlides - 1;
            }
            this.resetAutoSlide();
        },
        nextSlide() {
            if (this.currentSlide < this.totalSlides - 1) {
                this.currentSlide++;
            } else {
                // Loop to the beginning when pressing next on the last slide
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
            }, 5000);
        },
        resetAutoSlide() {
            if (this.autoSlideInterval) {
                clearInterval(this.autoSlideInterval);
                this.startAutoSlide();
            }
        },
        getIconClass(index) {
            const icons = ['fa-microchip', 'fa-server', 'fa-memory', 'fa-memory'];
            return `fas ${icons[index] || 'fa-desktop'}`;
        },
        checkScrollAnimation() {
            const elements = document.querySelectorAll('.animate-on-scroll');
            elements.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.top <= window.innerHeight * 0.8) {
                    el.classList.add('animate-fade-in');
                }
            });
        },
        observeElements() {
            if ('IntersectionObserver' in window) {
                const observer = new IntersectionObserver(
                    (entries) => {
                        entries.forEach(entry => {
                            if (entry.isIntersecting) {
                                entry.target.classList.add('is-visible');
                                observer.unobserve(entry.target);
                            }
                        });
                    },
                    { threshold: 0.1 }
                );

                document.querySelectorAll('.animate-on-scroll').forEach(el => {
                    observer.observe(el);
                });
            } else {
                // Fallback for browsers that don't support IntersectionObserver
                document.querySelectorAll('.animate-on-scroll').forEach(el => {
                    el.classList.add('is-visible');
                });
            }
        },
        async fetchCategories() {
            try {
                this.categoriesLoading = true;
                const response = await axios.get('http://127.0.0.1:8000/category/');

                // Map the categories to the format we need
                this.categories = response.data.slice(0, 4).map(category => {
                    // Map category names to appropriate icons
                    let icon = 'fa-microchip'; // Default icon

                    const categoryNameLower = category.category_name.toLowerCase();
                    if (categoryNameLower.includes('processor') || categoryNameLower.includes('cpu')) {
                        icon = 'fa-microchip';
                    } else if (categoryNameLower.includes('motherboard')) {
                        icon = 'fa-server';
                    } else if (categoryNameLower.includes('memory') || categoryNameLower.includes('ram')) {
                        icon = 'fa-memory';
                    } else if (categoryNameLower.includes('graphics') || categoryNameLower.includes('gpu')) {
                        icon = 'fa-desktop';
                    } else if (categoryNameLower.includes('storage') || categoryNameLower.includes('ssd') || categoryNameLower.includes('hdd')) {
                        icon = 'fa-hdd';
                    } else if (categoryNameLower.includes('power') || categoryNameLower.includes('psu')) {
                        icon = 'fa-bolt';
                    } else if (categoryNameLower.includes('case')) {
                        icon = 'fa-box';
                    } else if (categoryNameLower.includes('cooling')) {
                        icon = 'fa-fan';
                    }

                    return {
                        name: category.category_name,
                        icon: icon
                    };
                });

                // If we don't have enough categories, add some defaults
                if (this.categories.length < 4) {
                    const defaults = [
                        { name: 'Graphics Cards', icon: 'fa-desktop' },
                        { name: 'Processors', icon: 'fa-microchip' },
                        { name: 'Motherboards', icon: 'fa-server' },
                        { name: 'Memory', icon: 'fa-memory' }
                    ];

                    for (let i = this.categories.length; i < 4; i++) {
                        this.categories.push(defaults[i]);
                    }
                }

                this.categoriesLoading = false;
            } catch (error) {
                console.error('Error fetching categories:', error);

                // Fallback to default categories
                this.categories = [
                    { name: 'Graphics Cards', icon: 'fa-desktop' },
                    { name: 'Processors', icon: 'fa-microchip' },
                    { name: 'Motherboards', icon: 'fa-server' },
                    { name: 'Memory', icon: 'fa-memory' }
                ];

                this.categoriesLoading = false;
            }
        }
    },
    mounted() {
        this.startAutoSlide();
        this.observeElements();
        window.addEventListener('scroll', this.checkScrollAnimation);
    },
    beforeDestroy() {
        if (this.autoSlideInterval) {
            clearInterval(this.autoSlideInterval);
        }
        window.removeEventListener('scroll', this.checkScrollAnimation);
    },

    async created() {
        try {
            // Fetch categories and products in parallel
            const [productsResponse, topProductsResponse] = await Promise.all([
                axios.get('http://127.0.0.1:8000/products/'),
                axios.get('http://127.0.0.1:8000/products/?ordering=-sold_products')
            ]);

            this.featuredProducts = productsResponse.data.slice(0, 8);

            // Instead of grabbing one per category, get the actual top 10 best-selling products
            this.topProducts = topProductsResponse.data
                .sort((a, b) => b.sold_products - a.sold_products) // Sort by most sold
                .slice(0, 10); // Take top 10

            this.loading = false;

            // Fetch categories
            await this.fetchCategories();
        } catch (error) {
            console.error('Error fetching products:', error);
            this.loading = false;
        }
    }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.bg-pattern {
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.15'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2V6h4V4H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

/* Improved product image containers for white backgrounds */
.product-image-container {
    background: white;
    border: 1px solid rgba(229, 231, 235, 0.5);
    border-radius: 0.5rem;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    padding-bottom: 0;
    /* Remove bottom padding */
}

.product-image-container img {
    mix-blend-mode: multiply;
    /* This helps with white backgrounds */
    object-fit: contain;
    max-height: 95%;
    /* Increase max height for larger container */
    transition: transform 0.3s ease;
}

.animate-fade-in {
    animation: fadeIn 1s ease-out forwards;
}

.animate-float {
    animation: float 6s ease-in-out infinite;
}

.animate-fade-in-up-1 {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease-out 0.2s forwards;
}

.animate-fade-in-up-2 {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease-out 0.4s forwards;
}

.animate-fade-in-up-3 {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease-out 0.6s forwards;
}

.animate-on-scroll {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.animate-on-scroll.is-visible {
    opacity: 1;
    transform: translateY(0);
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes float {
    0% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-10px);
    }

    100% {
        transform: translateY(0px);
    }
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