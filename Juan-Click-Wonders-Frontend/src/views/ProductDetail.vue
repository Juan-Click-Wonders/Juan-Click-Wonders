<template>
    <div class="bg-gray-50 min-h-screen pb-16">

        <div v-if="loading" class="container mx-auto px-4 py-12 h-screen flex items-center justify-center">
            <div class="text-center">
                <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-yellow-500 mx-auto"></div>
                <p class="text-gray-600 mt-6 text-lg">Loading product details...</p>
            </div>
        </div>

        <div v-else-if="!product" class="container mx-auto px-4 py-12 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="text-xl font-bold text-gray-700 mb-2">Product Not Found</h3>
            <p class="text-gray-600 mb-6">The product you're looking for could not be found</p>
            <router-link to="/product_list"
                class="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold px-6 py-2 rounded-lg transition-colors duration-200">
                Browse Products
            </router-link>
        </div>

        <div v-else>

            <div class="bg-white border-b border-gray-200">
                <div class="container mx-auto px-4 py-3">
                    <div class="flex items-center text-sm text-gray-600">
                        <router-link to="/" class="hover:text-yellow-600 transition-colors">Home</router-link>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mx-2" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                        <router-link to="/product_list"
                            class="hover:text-yellow-600 transition-colors">Products</router-link>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mx-2" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                        <span class="text-gray-800 font-medium truncate max-w-xs">{{ product.name }}</span>
                    </div>
                </div>
            </div>


            <div class="container mx-auto px-4 py-8">
                <div class="bg-white rounded-xl shadow-md overflow-hidden">
                    <div class="flex flex-col lg:flex-row">

                        <div class="lg:w-1/2 p-8 bg-white">
                            <div
                                class="relative h-96 bg-white rounded-lg flex items-center justify-center p-4 mb-3 mx-auto max-w-xl">
                                <img v-if="product.image_url" :src="getImageUrl(product.image_url)" :alt="product.name"
                                    class="max-h-full max-w-full object-contain transition-transform duration-500 hover:scale-110 cursor-pointer"
                                    @click="openImageModal(product.image_url)">
                                <div v-else class="w-full h-full flex items-center justify-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-300" fill="none"
                                        viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>


                                <div v-if="product.stock === 0"
                                    class="absolute top-3 left-3 bg-red-500 text-white text-xs font-bold uppercase px-3 py-1 rounded-lg">
                                    Out of Stock
                                </div>
                                <div v-else-if="product.stock < 5"
                                    class="absolute top-3 left-3 bg-orange-500 text-white text-xs font-bold uppercase px-3 py-1 rounded-lg">
                                    Low Stock: {{ product.stock }} left
                                </div>
                            </div>
                        </div>


                        <div class="lg:w-1/2 p-8">
                            <div class="flex flex-col h-full">

                                <div class="flex justify-between items-start mb-3">
                                    <span
                                        class="bg-yellow-100 text-yellow-600 text-xs font-medium px-2.5 py-0.5 rounded-full">
                                        {{ categoryName }}
                                    </span>
                                    <span class="text-gray-600 text-sm">Brand: <span class="font-medium">{{
                                        product.brand }}</span></span>
                                </div>


                                <div class="flex justify-between items-start mb-4">
                                    <h1 class="text-3xl font-bold text-gray-900">{{ product.name }}</h1>
                                    <button @click="toggleWishlist"
                                        class="p-2 rounded-full hover:bg-gray-100 transition-colors focus:outline-none"
                                        :class="{ 'animate-heartbeat': isInWishlist }">
                                        <svg xmlns="http://www.w3.org/2000/svg"
                                            :class="[isInWishlist ? 'text-red-500 fill-red-500' : 'text-gray-400']"
                                            class="h-7 w-7 transition-all duration-300 transform hover:scale-110"
                                            viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                        </svg>
                                    </button>
                                </div>


                                <div class="flex items-baseline mb-6">
                                    <span class="text-3xl font-bold text-gray-900">₱{{ product.price.toLocaleString()
                                        }}</span>
                                    <span class="ml-2 text-sm text-gray-500">{{ product.sold_products }} units
                                        sold</span>
                                </div>


                                <div class="bg-gray-50 rounded-lg p-4 mb-6">
                                    <h3 class="font-semibold text-gray-800 mb-2">Description</h3>
                                    <p class="text-gray-700">
                                        {{ product.description || 'No description available for this product.' }}
                                    </p>
                                </div>


                                <div class="border-t border-gray-200 pt-6 mb-6">
                                    <h3 class="font-semibold text-gray-800 mb-3">Specifications</h3>
                                    <div class="grid grid-cols-2 gap-4">
                                        <div class="flex flex-col">
                                            <span class="text-gray-600 text-sm">Category</span>
                                            <span class="font-medium">{{ categoryName }}</span>
                                        </div>
                                        <div class="flex flex-col">
                                            <span class="text-gray-600 text-sm">Brand</span>
                                            <span class="font-medium">{{ product.brand }}</span>
                                        </div>
                                        <div class="flex flex-col">
                                            <span class="text-gray-600 text-sm">Stock</span>
                                            <span class="font-medium">{{ product.stock }} units</span>
                                        </div>
                                        <div class="flex flex-col">
                                            <span class="text-gray-600 text-sm">Units Sold</span>
                                            <span class="font-medium">{{ product.sold_products }}</span>
                                        </div>
                                    </div>
                                </div>


                                <div class="mt-auto">
                                    <div class="flex flex-col sm:flex-row sm:items-center gap-4">
                                        <div
                                            class="flex items-center bg-white border border-gray-300 rounded-lg overflow-hidden">
                                            <button @click="decreaseQuantity"
                                                class="px-4 py-2 text-gray-600 hover:bg-gray-100 transition-colors disabled:opacity-50"
                                                :disabled="quantity <= 1 || product.stock === 0">
                                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                                    viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2" d="M20 12H4" />
                                                </svg>
                                            </button>
                                            <span class="w-12 text-center font-medium">{{ quantity }}</span>
                                            <button @click="increaseQuantity"
                                                class="px-4 py-2 text-gray-600 hover:bg-gray-100 transition-colors disabled:opacity-50"
                                                :disabled="quantity >= product.stock || product.stock === 0">
                                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                                    viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2" d="M12 4v16m8-8H4" />
                                                </svg>
                                            </button>
                                        </div>
                                        <button @click="addToCart"
                                            class="flex-1 bg-black text-white py-3 px-6 rounded-lg font-semibold hover:bg-gray-800 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                                            :disabled="product.stock === 0">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                                            </svg>
                                            <span>{{ product.stock === 0 ? 'Out of Stock' : 'Add to Cart' }}</span>
                                        </button>
                                    </div>
                                    <p v-if="!isLoggedIn" class="text-center text-sm text-gray-600 mt-3">
                                        <router-link to="/auth/login/"
                                            class="bg-black text-white px-3 py-1 rounded-lg font-medium hover:bg-gray-800 transition-colors inline-flex items-center text-sm">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1 text-white"
                                                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                                            </svg>
                                            Log in
                                        </router-link> to add items to your cart
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container mx-auto px-4 py-8">
                <div class="bg-white rounded-xl shadow-md overflow-hidden mt-8">
                    <div class="p-6 border-b border-gray-200">
                        <h2 class="text-2xl font-bold text-gray-800">Customer Reviews</h2>
                    </div>

                    <div class="flex flex-col lg:flex-row">
                        <!-- Review Stats - Moved to left side -->
                        <div class="lg:w-1/3 p-6 bg-gray-50 border-r border-gray-200">
                            <div class="flex flex-col">
                                <div class="flex flex-col items-center mb-6">
                                    <div class="flex items-center justify-center mb-2">
                                        <span class="text-4xl font-bold">{{ averageRating }}</span>
                                        <span class="text-lg text-gray-500 ml-1">/ 5</span>
                                    </div>
                                    <div class="flex items-center">
                                        <template v-for="i in 5" :key="i">
                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                :class="[i <= Math.round(averageRating) ? 'text-yellow-500' : 'text-gray-300']"
                                                class="h-5 w-5 fill-current" viewBox="0 0 20 20" fill="currentColor">
                                                <path
                                                    d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118l-2.8-2.034c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                            </svg>
                                        </template>
                                    </div>
                                    <p class="text-sm text-gray-600 mt-1">{{ ratings.length }} {{ ratings.length === 1 ?
                                        'review' : 'reviews' }}</p>
                                </div>

                                <div class="w-full">
                                    <div v-for="star in 5" :key="star" class="flex items-center mb-1">
                                        <span class="text-sm font-medium w-4 mr-2">{{ 6 - star }}</span>
                                        <div class="flex-1 h-3 bg-gray-200 rounded-full overflow-hidden">
                                            <div class="h-full bg-yellow-500 rounded-full"
                                                :style="{ width: `${getStarPercentage(6 - star)}%` }"></div>
                                        </div>
                                        <span class="text-sm text-gray-600 ml-2">{{ getStarCount(6 - star) }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Reviews Content - Moved to right side -->
                        <div class="lg:w-2/3">
                            <!-- Add Review Form -->
                            <div v-if="isLoggedIn && !hasUserRated && canUserRate && product" class="p-6 border-b border-gray-200">
                                <div v-if="ratingSubmitted" class="bg-green-50 p-4 rounded-md mb-4 text-green-700">
                                    Your review has been submitted successfully!
                                </div>
                                <h3 class="text-xl font-semibold mb-4">Write a Review</h3>
                                <div class="space-y-4">
                                    <div>
                                        <label class="block text-gray-700 mb-2">Rating</label>
                                        <div class="flex">
                                            <template v-for="i in 5" :key="i">
                                                <button @click="newRating.rating = i" class="focus:outline-none"
                                                    :class="{ 'text-yellow-500': i <= newRating.rating, 'text-gray-300': i > newRating.rating }">
                                                    <svg xmlns="http://www.w3.org/2000/svg"
                                                        class="h-8 w-8 fill-current transform transition-transform hover:scale-110"
                                                        viewBox="0 0 20 20" fill="currentColor">
                                                        <path
                                                            d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118l-2.8-2.034c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                                    </svg>
                                                </button>
                                            </template>
                                        </div>
                                    </div>
                                    <div>
                                        <label for="review-text" class="block text-gray-700 mb-2">Review</label>
                                        <textarea id="review-text" v-model="newRating.description" rows="4"
                                            class="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-colors"
                                            placeholder="Share your experience with this product..."></textarea>
                                    </div>

                                    <!-- Image Upload (Optional) -->
                                    <div>
                                        <label for="review-image" class="block text-gray-700 mb-2">Add Photo
                                            (Optional)</label>
                                        <div class="flex items-center">
                                            <label
                                                class="cursor-pointer flex items-center justify-center border border-gray-300 rounded-lg p-3 text-gray-600 hover:bg-gray-50 transition-colors">
                                                <span v-if="!imagePreview" class="flex items-center">
                                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2"
                                                        fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                    </svg>
                                                    Choose Photo
                                                </span>
                                                <span v-else class="text-green-600">Change Photo</span>
                                                <input type="file" id="review-image" ref="fileInput"
                                                    @change="handleImageUpload"
                                                    accept="image/jpeg,image/png,image/gif,image/jpg" class="hidden">
                                            </label>
                                            <button v-if="imagePreview" @click="removeImage"
                                                class="ml-3 text-sm text-red-600 hover:text-red-700">
                                                Remove
                                            </button>
                                        </div>

                                        <!-- Image Preview -->
                                        <div v-if="imagePreview" class="mt-3">
                                            <img :src="imagePreview"
                                                class="h-24 rounded-md border border-gray-200 cursor-pointer hover:opacity-90 transition-opacity"
                                                @click="openPreviewModal" />
                                        </div>
                                        <p class="text-xs text-gray-500 mt-1">Supported formats: JPG, JPEG, PNG, GIF
                                            (max 5MB)</p>
                                    </div>

                                    <button @click="submitRating"
                                        :disabled="!newRating.rating || !newRating.description || submittingRating"
                                        class="bg-black text-white px-6 py-3 rounded-lg font-semibold hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                                        <span v-if="!submittingRating">Submit Review</span>
                                        <span v-else class="flex items-center">
                                            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                                                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                    stroke-width="4">
                                                </circle>
                                                <path class="opacity-75" fill="currentColor"
                                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                                </path>
                                            </svg>
                                            Submitting...
                                        </span>
                                    </button>
                                </div>
                            </div>

                            <!-- Already reviewed message -->
                            <div v-else-if="isLoggedIn && hasUserRated" class="p-6 border-b border-gray-200 bg-gray-50">
                                <div class="flex items-center text-gray-700 mb-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                    </svg>
                                    <span class="font-medium">You have already reviewed this product</span>
                                </div>
                                <p class="text-gray-600 ml-7">Thank you for your feedback!</p>
                            </div>

                            <!-- Purchased but not delivered message -->
                            <div v-else-if="isLoggedIn && hasUserPurchased && !hasUserReceived" class="p-6 border-b border-gray-200 bg-gray-50">
                                <div class="flex items-start text-gray-700 mb-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <div>
                                        <span class="font-medium">Your order is on the way</span>
                                        <p class="text-gray-600 mt-1">You can leave a review once your order has been delivered. Please check your order status in your account.</p>
                                        <router-link to="/orders" 
                                            class="mt-3 bg-black text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors inline-flex items-center">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                                            </svg>
                                            View Orders
                                        </router-link>
                                    </div>
                                </div>
                            </div>

                            <div v-else-if="isLoggedIn && !hasUserPurchased" class="p-6 border-b border-gray-200 bg-gray-50">
                                <div class="flex items-start text-gray-700 mb-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <div>
                                        <span class="font-medium">You need to purchase this product before rating</span>
                                        <p class="text-gray-600 mt-1">Only customers who have purchased this product can leave a review.</p>
                                    </div>
                                </div>
                            </div>

                            <!-- Loading state while checking eligibility -->
                            <div v-else-if="isLoggedIn && checkingRatingEligibility" class="p-6 border-b border-gray-200 bg-gray-50">
                                <div class="flex items-center text-gray-700 space-x-2">
                                    <div class="animate-spin h-4 w-4 border-b-2 border-yellow-500 rounded-full"></div>
                                    <span>Checking if you can review this product...</span>
                                </div>
                            </div>

                            <!-- Not logged in message -->
                            <div v-else-if="!isLoggedIn" class="p-6 border-b border-gray-200 bg-gray-50">
                                <p class="text-gray-700">
                                    Please <router-link to="/auth/login"
                                        class="bg-black text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-800 transition-colors inline-flex items-center">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-white"
                                            fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                                        </svg>
                                        Log in
                                    </router-link> to leave a review.
                                </p>
                            </div>

                            <div v-if="ratings.length > 0">
                                <div v-for="(rating, index) in ratings" :key="rating.id" class="p-6"
                                    :class="{ 'border-b border-gray-200': index < ratings.length - 1 }">
                                    <div class="flex items-start">
                                        <div class="mr-4">
                                            <div
                                                class="w-10 h-10 bg-yellow-500 rounded-full flex items-center justify-center text-white font-bold">
                                                {{ (rating.user_name && rating.user_name.charAt(0)) ||
                                                    (typeof rating.user === 'string' ? rating.user.charAt(0) : 'U') }}
                                            </div>
                                        </div>
                                        <div class="flex-1">
                                            <div class="flex flex-wrap items-center gap-2 mb-1">
                                                <span class="font-medium text-gray-800">{{ rating.user_name ||
                                                    rating.first_name ||
                                                    rating.username || 'User' }}</span>
                                                <div class="flex">
                                                    <template v-for="i in 5" :key="i">
                                                        <svg xmlns="http://www.w3.org/2000/svg"
                                                            :class="[i <= rating.rating ? 'text-yellow-500' : 'text-gray-300']"
                                                            class="h-4 w-4 fill-current" viewBox="0 0 20 20"
                                                            fill="currentColor">
                                                            <path
                                                                d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118l-2.8-2.034c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                                        </svg>
                                                    </template>
                                                </div>
                                            </div>

                                            <div class="text-sm text-gray-500 mb-2">{{ formatDate(rating.created_at) }}
                                            </div>

                                            <p class="text-gray-700 whitespace-pre-line mb-3">{{ rating.description }}
                                            </p>

                                            <div v-if="rating.image_url" class="mt-2">
                                                <img :src="getRatingImageUrl(rating.image_url)" alt="Review image"
                                                    class="h-24 w-auto rounded-md border border-gray-200 cursor-pointer hover:opacity-90 transition-opacity"
                                                    @click="openImageModal(rating.image_url)" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div v-else class="p-6 text-left">
                                <p class="text-gray-600">No reviews yet. Be the first to review this product!</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="showImageModal"
            class="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4"
            @click="closeImageModal">
            <div class="relative max-w-4xl max-h-full">
                <img :src="isPreviewImage ? modalImageUrl : getRatingImageUrl(modalImageUrl)" alt="Enlarged image"
                    class="max-w-full max-h-[90vh] object-contain rounded-lg shadow-xl" />
                <button @click.stop="closeImageModal"
                    class="absolute top-3 right-3 bg-black bg-opacity-50 text-white rounded-full p-2 hover:bg-opacity-70 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";


const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    withCredentials: true
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


api.interceptors.request.use(config => {
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

export default {
    data() {
        return {
            product: null,
            categories: [],
            ratings: [],
            quantity: 1,
            cart: null,
            loading: true,
            newRating: {
                rating: 0,
                description: '',
                product: null
            },
            submittingRating: false,
            ratingSubmitted: false,
            currentUserId: null,
            imagePreview: null,
            userProfile: null,
            userHasRatedProduct: false,
            showImageModal: false,
            modalImageUrl: null,
            isPreviewImage: false,
            isInWishlist: false,
            hasUserPurchased: false,
            hasUserReceived: false,
            canUserRate: false,
            checkingRatingEligibility: false,
            userAuthState: localStorage.getItem('isAuthenticated') === 'true'
        };
    },
    computed: {
        categoryName() {
            if (!this.product) return 'Loading...';
            return this.product.category_name || 'Unknown Category';
        },
        isLoggedIn() {
            return this.userAuthState;
        },
        averageRating() {
            if (!this.ratings || this.ratings.length === 0) return 0;
            const sum = this.ratings.reduce((total, rating) => total + rating.rating, 0);
            return (sum / this.ratings.length).toFixed(1);
        },
        hasUserRated() {
            return this.userHasRatedProduct;
        }
    },
    methods: {
        getImageUrl(imagePath) {
            if (!imagePath) return null;
            return imagePath;
        },
        getRatingImageUrl(imagePath) {
            if (!imagePath) return null;


            if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
                return imagePath;
            }


            if (imagePath.includes('/media/rating_images/')) {

                if (imagePath.startsWith('/')) {
                    return `http://127.0.0.1:8000${imagePath}`;
                }
                return `http://127.0.0.1:8000/${imagePath}`;
            }


            if (!imagePath.includes('/')) {
                return `http://127.0.0.1:8000/media/rating_images/${imagePath}`;
            }


            return `http://127.0.0.1:8000/media/rating_images/${imagePath.split('/').pop()}`;
        },
        formatDate(dateString) {
            return new Date(dateString).toLocaleDateString();
        },
        async fetchCategories() {
            try {
                const response = await api.get("/category");
                this.categories = response.data;
            } catch (error) {
                console.error("Error fetching categories:", error);
            }
        },
        async fetchProduct() {
            try {
                this.loading = true;
                this.hasUserPurchased = false;
                this.hasUserReceived = false;
                this.canUserRate = false;
                
                const productId = this.$route.params.id;
                const response = await api.get(`/products/${productId}`);
                this.product = response.data;
                this.newRating.product = this.product.product_id;
                this.loading = false;
                this.fetchRatings();

                if (this.isLoggedIn) {
                    this.checkWishlistStatus();
                }
            } catch (error) {
                console.error("Error fetching product:", error);
                this.loading = false;
            }
        },

        async checkWishlistStatus() {
            try {
                const response = await api.get('/wishlist/');
                if (response.data && Array.isArray(response.data)) {
                    this.isInWishlist = response.data.some(item =>
                        item.product === this.product.product_id
                    );
                }
            } catch (error) {
                console.error('Error checking wishlist status:', error);
            }
        },
        async checkRatingEligibility() {
            if (!this.isLoggedIn || !this.product || this.userHasRatedProduct) return;
            
            try {
                this.checkingRatingEligibility = true;
                
                // Check user's orders for this product
                const ordersResponse = await api.get('/orders/');
                
                if (!ordersResponse.data || !Array.isArray(ordersResponse.data) || ordersResponse.data.length === 0) {
                    console.error('No orders found or invalid order data format');
                    this.hasUserPurchased = false;
                    this.hasUserReceived = false;
                    this.canUserRate = false;
                    return;
                }
                
                // Get current product ID and name for matching
                const productId = parseInt(this.product.product_id || this.product.id || this.product.ID || '0');
                const productName = this.product.name;
                
                // Track if we found any matching orders
                let foundMatchingOrders = false;
                let foundDeliveredOrders = false;
                
                // Process each order to check if it contains our product
                for (const order of ordersResponse.data) {
                    let orderContainsProduct = false;
                    let matchReason = 'None';
                    
                    // Case 1: Order has a direct product property that is an object with name property
                    if (order.product && typeof order.product === 'object') {
                        // Try to match by name first if available (most reliable in this system)
                        if (order.product.name && productName && order.product.name.trim().toLowerCase() === productName.trim().toLowerCase()) {
                            orderContainsProduct = true;
                            matchReason = 'Name match';
                        }
                        
                        // Also try to match by ID (various possible properties)
                        const orderProductId = parseInt(order.product.product_id || order.product.id || order.product.ID || '0');
                        
                        if (orderProductId > 0 && orderProductId === productId) {
                            orderContainsProduct = true;
                            matchReason = 'ID match';
                        }
                    } 
                    // Case 2: Order has a direct product property that is a primitive value
                    else if (order.product && (typeof order.product === 'number' || typeof order.product === 'string')) {
                        const orderProductId = parseInt(order.product);
                        
                        if (orderProductId === productId) {
                            orderContainsProduct = true;
                            matchReason = 'Direct ID match';
                        }
                    }
                    
                    // Case 3: Order has array of order_items
                    if (!orderContainsProduct && order.order_items && Array.isArray(order.order_items)) {
                        
                        for (const item of order.order_items) {                            
                            if (item.product) {
                                if (typeof item.product === 'object') {
                                    // Try name match first
                                    if (item.product.name && productName && 
                                        item.product.name.trim().toLowerCase() === productName.trim().toLowerCase()) {
                                        orderContainsProduct = true;
                                        matchReason = 'Item name match';
                                        break;
                                    }
                                    
                                    // Try ID match
                                    const itemProductId = parseInt(item.product.product_id || item.product.id || item.product.ID || '0');
                                    
                                    if (itemProductId > 0 && itemProductId === productId) {
                                        orderContainsProduct = true;
                                        matchReason = 'Item ID match';
                                        break;
                                    }
                                } else if (typeof item.product === 'number' || typeof item.product === 'string') {
                                    const itemProductId = parseInt(item.product);
                                    
                                    if (itemProductId === productId) {
                                        orderContainsProduct = true;
                                        matchReason = 'Item direct ID match';
                                        break;
                                    }
                                }
                            }
                        }
                    }
                    
                    // Case 4: Check order fields directly (some API formats simplify this way)
                    if (!orderContainsProduct) {
                        // Try matching the order's own fields
                        if (order.product_id && parseInt(order.product_id) === productId) {
                            orderContainsProduct = true;
                            matchReason = 'Order product_id field match';
                        } else if (order.name && productName && order.name.trim().toLowerCase() === productName.trim().toLowerCase()) {
                            orderContainsProduct = true;
                            matchReason = 'Order name field match';
                        }
                    }
                    
                    // If this order contains our product, check if it's been delivered
                    if (orderContainsProduct) {
                        foundMatchingOrders = true;
                        
                        // Check order status (various possible formats)
                        const status = typeof order.status === 'string' ? order.status.toLowerCase() : '';
                        if (
                            status === 'd' || 
                            status === 'delivered' || 
                            status === 'complete' || 
                            status === 'completed' ||
                            status.includes('deliver') ||
                            status.includes('complet')
                        ) {
                            foundDeliveredOrders = true;
                        }
                    }
                }
                
                // Final determination
                this.hasUserPurchased = foundMatchingOrders;
                this.hasUserReceived = foundDeliveredOrders;
                this.canUserRate = foundDeliveredOrders;
            } catch (error) {
                console.error("Error checking rating eligibility:", error);
                // Set defaults in case of error
                this.hasUserPurchased = false;
                this.hasUserReceived = false;
                this.canUserRate = false;
            } finally {
                this.checkingRatingEligibility = false;
            }
        },
        async fetchRatings() {
            if (!this.product) return;

            try {
                const response = await api.get(`/ratings/`, {
                    params: {
                        product: this.product.product_id
                    }
                });

                this.ratings = response.data.map(rating => {
                    const processedRating = { ...rating };

                    if (!processedRating.user_name) {
                        if (typeof processedRating.user === 'object' && processedRating.user !== null) {
                            processedRating.user_name = processedRating.user.first_name ||
                                processedRating.user.username ||
                                processedRating.user.name ||
                                processedRating.user.Name;
                        } else if (processedRating.username) {
                            processedRating.user_name = processedRating.username;
                        } else if (processedRating.first_name) {
                            processedRating.user_name = processedRating.first_name;
                        } else if (processedRating.user_first_name) {
                            processedRating.user_name = processedRating.user_first_name;
                        }
                    }

                    return processedRating;
                });

                if (this.isLoggedIn) {
                    try {
                        const userRatingsResponse = await api.get(`/ratings/`, {
                            params: {
                                product: this.product.product_id,
                                user_ratings: true
                            }
                        });

                        if (userRatingsResponse.data && userRatingsResponse.data.length > 0) {
                            this.userHasRatedProduct = true;
                        } else {
                            this.userHasRatedProduct = false;
                            // Check if the user is eligible to rate the product
                            this.checkRatingEligibility();
                        }
                    } catch (userRatingError) {
                        console.error("Could not fetch user-specific ratings:", userRatingError);
                        this.checkRatingEligibility();
                    }

                    this.getCurrentUser();
                }
            } catch (error) {
                console.error("Error fetching ratings:", error);
            }
        },
        async getCurrentUser() {
            try {
                // Use the correct endpoint path with the /api prefix
                const response = await api.get('/api/profile/');

                this.userProfile = response.data;

                if (response.data) {
                    this.userProfile = response.data;

                    if (response.data.id) {
                        this.currentUserId = response.data.id;
                    } else if (response.data.user && response.data.user.id) {
                        this.currentUserId = response.data.user.id;
                    } else if (response.data.user_id) {
                        this.currentUserId = response.data.user_id;
                    } else {
                        this.currentUserId = 1;
                    }
                }
            } catch (error) {
                console.error("Could not fetch user profile:", error);
            }
        },
        getStarCount(star) {
            if (!this.ratings) return 0;
            return this.ratings.filter(rating => rating.rating === star).length;
        },
        getStarPercentage(star) {
            if (!this.ratings || this.ratings.length === 0) return 0;
            const count = this.getStarCount(star);
            return (count / this.ratings.length) * 100;
        },
        async toggleWishlist() {
            if (!this.isLoggedIn) {
                this.$router.push('/auth/login');
                return;
            }

            const wasInWishlist = this.isInWishlist;
            this.isInWishlist = !wasInWishlist;

            try {
                const response = await api.post('/wishlist/toggle/', {
                    product: this.product.product_id
                });

                if (response.data && response.data.is_in_wishlist !== undefined) {
                    this.isInWishlist = response.data.is_in_wishlist;
                }
            } catch (error) {
                console.error('Error updating wishlist:', error);
                this.isInWishlist = wasInWishlist;

                if (error.response && error.response.status === 401) {
                    this.$router.push('/auth/login');
                }
            }
        },
        async submitRating() {
            if (!this.newRating.rating || !this.newRating.description || !this.product) return;

            this.submittingRating = true;

            try {
                let userId = null;
                let profileResponse = null;

                try {
                    profileResponse = await api.get('/api/profile/');

                    if (profileResponse.data) {
                        this.userProfile = profileResponse.data;

                        if (profileResponse.data.id) {
                            userId = profileResponse.data.id;
                        } else if (profileResponse.data.user && profileResponse.data.user.id) {
                            userId = profileResponse.data.user.id;
                        } else if (profileResponse.data.user_id) {
                            userId = profileResponse.data.user_id;
                        } else {
                            userId = 1;
                        }
                    } else {
                        console.error("No profile data received");
                    }
                } catch (profileError) {
                    console.error("Error fetching profile:", profileError);
                    if (profileError.response) {
                        console.error("Profile error status:", profileError.response.status);
                    }
                }

                const ratingData = {
                    product: this.product.product_id,
                    rating: this.newRating.rating,
                    description: this.newRating.description,
                };

                if (userId) {
                    ratingData.user = userId;
                }

                if (profileResponse && profileResponse.data) {
                    if (profileResponse.data.first_name) {
                        ratingData.user_name = profileResponse.data.first_name;
                    } else if (profileResponse.data.Name) {
                        ratingData.user_name = profileResponse.data.Name;
                    } else if (profileResponse.data.name) {
                        ratingData.user_name = profileResponse.data.name;
                    } else if (profileResponse.data.username) {
                        ratingData.user_name = profileResponse.data.username;
                    }
                }

                ratingData.auth_token = localStorage.getItem('token') || 'auth_session_active';

                const fileInput = this.$refs.fileInput;
                const hasImage = fileInput && fileInput.files && fileInput.files.length > 0;

                let response;

                if (hasImage) {
                    const formData = new FormData();

                    formData.append('product', this.product.product_id);
                    formData.append('rating', this.newRating.rating);
                    formData.append('description', this.newRating.description);

                    if (userId) {
                        formData.append('user', userId);
                    }

                    formData.append('auth_token', localStorage.getItem('token') || 'auth_session_active');

                    if (profileResponse && profileResponse.data) {
                        if (profileResponse.data.first_name) {
                            formData.append('user_name', profileResponse.data.first_name);
                        } else if (profileResponse.data.Name) {
                            formData.append('user_name', profileResponse.data.Name);
                        } else if (profileResponse.data.name) {
                            formData.append('user_name', profileResponse.data.name);
                        } else if (profileResponse.data.username) {
                            formData.append('user_name', profileResponse.data.username);
                        }
                    }

                    const file = fileInput.files[0];
                    formData.append('image_url', file);

                    const ratingEndpoint = '/ratings/create/';

                    try {
                        response = await api.post(ratingEndpoint, formData, {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            },
                            withCredentials: true // Ensure cookies are passed
                        });
                    } catch (innerError) {
                        console.error("Error with first endpoint:", innerError);

                        const altEndpoint = '/api/ratings/create/';
                        response = await api.post(altEndpoint, formData, {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            },
                            withCredentials: true
                        });
                    }
                } else {
                    const ratingEndpoint = '/ratings/create/';

                    try {
                        response = await api.post(ratingEndpoint, ratingData, {
                            withCredentials: true // Ensure cookies are passed
                        });
                    } catch (innerError) {
                        console.error("Error with first endpoint:", innerError);

                        const altEndpoint = '/api/ratings/create/';
                        response = await api.post(altEndpoint, ratingData, {
                            withCredentials: true
                        });
                    }
                }

                this.ratingSubmitted = true;

                if (response && response.data) {
                    const processedNewRating = { ...response.data };

                    if (profileResponse && profileResponse.data) {
                        if (profileResponse.data.first_name) {
                            processedNewRating.user_name = profileResponse.data.first_name;
                        } else if (profileResponse.data.Name) {
                            processedNewRating.user_name = profileResponse.data.Name;
                        } else if (profileResponse.data.name) {
                            processedNewRating.user_name = profileResponse.data.name;
                        } else if (profileResponse.data.username) {
                            processedNewRating.user_name = profileResponse.data.username;
                        }
                    }

                    this.ratings.unshift(processedNewRating);
                }

                this.newRating = {
                    rating: 0,
                    description: '',
                    product: this.product.product_id
                };
                this.imagePreview = null;
                if (fileInput) fileInput.value = '';

                this.fetchRatings();

                setTimeout(() => {
                    this.ratingSubmitted = false;
                }, 3000);
            } catch (error) {
                console.error("Error submitting rating:", error);

                if (error.response) {
                    console.error("Error response status:", error.response.status);

                    if (error.response.status === 403) {
                        // Check for specific error messages
                        if (error.response.data && error.response.data.detail) {
                            if (error.response.data.detail.includes("must purchase")) {
                                alert("You must purchase this product before you can rate it.");
                            } else if (error.response.data.detail.includes("can only rate products that have been delivered")) {
                                alert("You can only rate products that have been delivered to you.");
                            } else if (error.response.data.detail.includes("already rated")) {
                                alert("You have already reviewed this product.");
                            } else {
                                alert(error.response.data.detail);
                            }
                        } else {
                            alert("You have already reviewed this product.");
                        }
                        this.fetchRatings();
                    } else if (error.response.status === 400) {
                        let errorMessage = "There was an error submitting your review. ";

                        if (error.response.data) {
                            if (typeof error.response.data === 'string') {
                                errorMessage += error.response.data;
                            } else if (typeof error.response.data === 'object') {
                                const errorFields = Object.keys(error.response.data);
                                if (errorFields.length > 0) {
                                    errorMessage += "Issues with: ";
                                    errorFields.forEach(field => {
                                        const fieldError = error.response.data[field];
                                        errorMessage += `${field} (${fieldError}) `;
                                    });
                                } else {
                                    errorMessage += JSON.stringify(error.response.data);
                                }
                            } else {
                                errorMessage += JSON.stringify(error.response.data);
                            }
                        }

                        alert(errorMessage);
                    } else if (error.response.status === 401) {
                        alert("You must be logged in to submit a review. Please log in and try again.");
                        this.$router.push('/auth/login/');
                    } else {
                        alert(`Error (${error.response.status}): ${error.message}`);
                    }
                } else if (error.request) {
                    alert("Network error - the server didn't respond. Please check your connection and try again.");
                } else {
                    alert("An unexpected error occurred: " + error.message);
                }
            } finally {
                this.submittingRating = false;
            }
        },
        increaseQuantity() {
            if (this.quantity < this.product.stock) this.quantity++;
        },
        decreaseQuantity() {
            if (this.quantity > 1) this.quantity--;
        },
        async addToCart() {
            if (!this.isLoggedIn) {
                this.$router.push('/auth/login/');
                return;
            }

            try {
                // Get the user's cart (should exist from registration)
                const cartResponse = await api.get('/cart/');
                if (!cartResponse.data || cartResponse.data.length === 0) {
                    throw new Error('Cart not found. Please try logging out and logging back in.');
                }

                const cart = cartResponse.data[0];

                // Add the item to the cart
                const response = await api.post(`/cart/${cart.cart_id}/items/`, {
                    product: this.product.product_id,
                    quantity: this.quantity
                });

                // Update the cart count in localStorage
                const currentCount = parseInt(localStorage.getItem('cartCount') || '0');
                localStorage.setItem('cartCount', (currentCount + this.quantity).toString());

                // Dispatch event to update cart count in other components
                window.dispatchEvent(new Event('cart-updated'));

                // Redirect to cart page
                this.$router.push('/cart');
            } catch (error) {
                console.error('Error adding to cart:', error);
                if (error.response) {
                    if (error.response.status === 401) {
                        this.$router.push('/auth/login/');
                    } else if (error.response.status === 400) {
                        alert(error.response.data.error || 'Failed to add item to cart. Please try again.');
                    } else {
                        alert('An error occurred while adding to cart. Please try again.');
                    }
                } else {
                    alert(error.message || 'Network error. Please check your connection and try again.');
                }
            }
        },
        handleImageUpload(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.imagePreview = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        },
        removeImage() {
            this.imagePreview = null;
        },
        // Modal functions
        openImageModal(imageUrl) {
            this.modalImageUrl = imageUrl;
            this.isPreviewImage = false;
            this.showImageModal = true;
            document.body.style.overflow = 'hidden';
        },
        closeImageModal() {
            this.showImageModal = false;
            document.body.style.overflow = 'auto';
        },
        openPreviewModal() {
            this.modalImageUrl = this.imagePreview;
            this.isPreviewImage = true;
            this.showImageModal = true;
            document.body.style.overflow = 'hidden';
        },
        async debugOrderCheck() {
            if (!this.product) {
                alert("Product not loaded yet. Please wait.");
                return;
            }
            
            try {
                // Get the user's orders
                const ordersResponse = await api.get('/orders/');
                
                const productId = this.product.product_id || this.product.id || this.product.ID;
                const productName = this.product.name;
                
                let matchingOrders = [];
                
                if (Array.isArray(ordersResponse.data)) {
                    // Process each order to find matches
                    for (const order of ordersResponse.data) {
                        let orderInfo = {
                            order_id: order.order_id || order.id || 'Unknown',
                            status: order.status || 'Unknown',
                            contains_product: false,
                            match_reason: '',
                            order_data: order
                        };
                        
                        // Check direct product match
                        if (order.product) {
                            if (typeof order.product === 'object') {
                                const orderProductId = order.product.product_id || order.product.id || order.product.ID;
                                if (parseInt(orderProductId) === parseInt(productId)) {
                                    orderInfo.contains_product = true;
                                    orderInfo.match_reason = 'Direct product object match';
                                }
                            } else if (typeof order.product === 'number' || typeof order.product === 'string') {
                                if (parseInt(order.product) === parseInt(productId)) {
                                    orderInfo.contains_product = true;
                                    orderInfo.match_reason = 'Direct product ID match';
                                }
                            }
                        }
                        
                        // Case 2: Order has array of order_items
                        if (!orderInfo.contains_product && order.order_items && Array.isArray(order.order_items)) {
                            
                            for (const item of order.order_items) {
                                if (item.product) {
                                    if (typeof item.product === 'object') {
                                        const itemProductId = item.product.product_id || item.product.id || item.product.ID;
                                        if (itemProductId === productId) {
                                            orderInfo.contains_product = true;
                                            orderInfo.match_reason = 'Match in order_items array (object)';
                                            break;
                                        }
                                    } else if (typeof item.product === 'number' || typeof item.product === 'string') {
                                        if (parseInt(item.product) === parseInt(productId)) {
                                            orderInfo.contains_product = true;
                                            orderInfo.match_reason = 'Match in order_items array (ID)';
                                            break;
                                        }
                                    }
                                }
                            }
                        }
                        
                        // Case 3: The order itself might be the product entry (simplified API response)
                        if (!orderInfo.contains_product) {
                            if (order.product_id && parseInt(order.product_id) === parseInt(productId)) {
                                orderInfo.contains_product = true;
                                orderInfo.match_reason = 'Order has matching product_id';
                            } else if (order.name && order.name === productName) {
                                // Matching by name as a last resort if IDs don't match
                                orderInfo.contains_product = true;
                                orderInfo.match_reason = 'Order has matching product name';
                            }
                        }
                        
                        if (orderInfo.contains_product) {
                            matchingOrders.push(orderInfo);
                        }
                    }
                }
                
                if (matchingOrders.length === 0) {
                    alert(`No orders found containing this product (ID: ${productId}, Name: ${productName})`);
                } else {
                    const orderSummary = matchingOrders.map(order => 
                        `Order #${order.order_id} - Status: ${order.status}\nMatch found: ${order.match_reason}`
                    ).join('\n\n');
                    
                    alert(`Found ${matchingOrders.length} orders with this product:\n\n${orderSummary}`);
                    
                    // Rerun the eligibility check with the new information
                    await this.checkRatingEligibility();
                }
            } catch (error) {
                console.error("Error with debug order check:", error);
                alert("An error occurred while checking orders. See console for details.");
            }
        }
    },
    async created() {
        try {
            await this.fetchCategories();
            await this.fetchProduct();
            
            if (this.isLoggedIn && this.product) {
                // First check if user has already rated the product
                const userRatingsResponse = await api.get(`/ratings/`, {
                    params: {
                        product: this.product.product_id,
                        user_ratings: true
                    }
                });
                
                this.userHasRatedProduct = !!(userRatingsResponse.data && userRatingsResponse.data.length > 0);
                
                if (!this.userHasRatedProduct) {
                    // Add a slight delay to ensure all data is properly loaded
                    setTimeout(() => {
                        this.checkRatingEligibility();
                    }, 1000);
                }
            }
        } catch (error) {
            console.error("Error during component initialization:", error);
        }
    },
    watch: {
        '$route.params.id'() {
            this.quantity = 1;
            this.product = null;
            this.fetchProduct();
        }
    }
};
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css");

@keyframes pulse {

    0%,
    100% {
        opacity: 0.5;
    }

    50% {
        opacity: 0.8;
    }
}

.animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes heartbeat {
    0% {
        transform: scale(1);
    }

    25% {
        transform: scale(1.2);
    }

    50% {
        transform: scale(1);
    }

    75% {
        transform: scale(1.2);
    }

    100% {
        transform: scale(1);
    }
}

.animate-heartbeat {
    animation: heartbeat 0.6s ease-in-out;
}
</style>