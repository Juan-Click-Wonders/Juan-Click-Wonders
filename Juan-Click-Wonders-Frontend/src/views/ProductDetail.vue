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
                <img :src="product.image" :alt="product.title" class="w-full max-h-[500px] object-contain">
            </div>

            <!-- Product Details -->
            <div class="w-1/2">
                <!-- Category -->
                <h4 class="text-sm text-gray-500 uppercase font-semibold">{{ product.category }}</h4>

                <!-- Title -->
                <h2 class="text-3xl font-bold mt-1">{{ product.title }}</h2>

                <!-- Ratings -->
                <div class="flex items-center text-yellow-500 mt-2">
                    <span v-for="star in 5" :key="star">
                        <i v-if="star <= Math.round(product.rating.rate)" class="fas fa-star"></i>
                        <i v-else class="far fa-star"></i>
                    </span>
                    <span class="ml-2 text-gray-500">({{ product.rating.count }} reviews)</span>
                </div>

                <!-- Description -->
                <p class="text-gray-700 mt-4">{{ product.description }}</p>

                <!-- Price -->
                <p class="text-2xl font-semibold text-gray-800 mt-4">₱{{ product.price }}</p>

                <!-- Quantity Selector & Buy Button -->
                <div class="flex items-center mt-6 gap-4">
                    <!-- Quantity Selector -->
                    <div class="relative flex items-center border rounded-full bg-white px-4"
                        style="height: 48px; min-width: 120px; position: relative;">
                        <input type="text" v-model="quantity"
                            class="w-10 text-center bg-transparent focus:outline-none text-lg font-semibold" readonly>
                        <div class="absolute right-3 flex flex-col">
                            <button @click="increaseQuantity" class="text-gray-700 hover:text-black leading-none">
                                <i class="fas fa-chevron-up"></i>
                            </button>
                            <button @click="decreaseQuantity" class="text-gray-700 hover:text-black leading-none">
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

export default {
    data() {
        return {
            product: null,
            quantity: 1,
        };
    },
    methods: {
        fetchProduct() {
            const productId = this.$route.params.id;
            axios.get(`https://fakestoreapi.com/products/${productId}`)
                .then(response => {
                    this.product = response.data;
                })
                .catch(error => console.error("Error fetching product:", error));
        },
        increaseQuantity() {
            if (this.quantity < 10) this.quantity++;
        },
        decreaseQuantity() {
            if (this.quantity > 1) this.quantity--;
        }
    },
    created() {
        this.fetchProduct();
    }
};
</script>

<style>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css");
</style>
