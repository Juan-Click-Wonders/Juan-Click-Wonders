<template>
    <div class="bg-gray-50 min-h-screen pb-16">
        <!-- Loading State -->
        <div v-if="loading" class="container mx-auto px-4 py-12 h-screen flex items-center justify-center">
            <div class="text-center">
                <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-yellow-500 mx-auto"></div>
                <p class="text-gray-600 mt-6 text-lg">Loading product details...</p>
            </div>
        </div>

        <div v-else-if="!product" class="container mx-auto px-4 py-12 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="text-xl font-bold text-gray-700 mb-2">Product Not Found</h3>
            <p class="text-gray-600 mb-6">The product you're looking for could not be found</p>
            <router-link to="/product_list" class="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold px-6 py-2 rounded-lg transition-colors duration-200">
                Browse Products
            </router-link>
        </div>

        <div v-else>
            <!-- Breadcrumb Navigation -->
            <div class="bg-white border-b border-gray-200">
                <div class="container mx-auto px-4 py-3">
                    <div class="flex items-center text-sm text-gray-600">
                        <router-link to="/" class="hover:text-yellow-600 transition-colors">Home</router-link>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mx-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                        <router-link to="/product_list" class="hover:text-yellow-600 transition-colors">Products</router-link>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mx-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                        <span class="text-gray-800 font-medium truncate max-w-xs">{{ product.name }}</span>
                    </div>
                </div>
            </div>

            <!-- Product Content -->
            <div class="container mx-auto px-4 py-8">
                <div class="bg-white rounded-xl shadow-md overflow-hidden">
                    <div class="flex flex-col lg:flex-row">
                        <!-- Product Image -->
                        <div class="lg:w-1/2 p-8 bg-white">
                            <div class="relative h-96 bg-white rounded-lg flex items-center justify-center p-4 mb-3 mx-auto max-w-xl">
                                <img v-if="product.image_url" 
                                    :src="getImageUrl(product.image_url)" 
                                    :alt="product.name" 
                                    class="max-h-full max-w-full object-contain transition-transform duration-500 hover:scale-110 cursor-pointer"
                                    @click="openImageModal(product.image_url)">
                                <div v-else class="w-full h-full flex items-center justify-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                
                                <!-- Stock Badge -->
                                <div v-if="product.stock === 0" class="absolute top-3 left-3 bg-red-500 text-white text-xs font-bold uppercase px-3 py-1 rounded-lg">
                                    Out of Stock
                                </div>
                                <div v-else-if="product.stock < 5" class="absolute top-3 left-3 bg-orange-500 text-white text-xs font-bold uppercase px-3 py-1 rounded-lg">
                                    Low Stock: {{ product.stock }} left
                                </div>
                            </div>
                        </div>

                        <!-- Product Details -->
                        <div class="lg:w-1/2 p-8">
                            <div class="flex flex-col h-full">
                                <!-- Category & Brand -->
                                <div class="flex justify-between items-start mb-3">
                                    <span class="bg-yellow-100 text-yellow-600 text-xs font-medium px-2.5 py-0.5 rounded-full">
                                        {{ categoryName }}
                                    </span>
                                    <span class="text-gray-600 text-sm">Brand: <span class="font-medium">{{ product.brand }}</span></span>
                                </div>

                                <!-- Product Name -->
                                <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ product.name }}</h1>

                                <!-- Price -->
                                <div class="flex items-baseline mb-6">
                                    <span class="text-3xl font-bold text-gray-900">₱{{ product.price.toLocaleString() }}</span>
                                    <span class="ml-2 text-sm text-gray-500">{{ product.sold_products }} units sold</span>
                                </div>

                                <!-- Description -->
                                <div class="bg-gray-50 rounded-lg p-4 mb-6">
                                    <h3 class="font-semibold text-gray-800 mb-2">Description</h3>
                                    <p class="text-gray-700">{{ product.description || 'No description available for this product.' }}</p>
                                </div>

                                <!-- Specifications -->
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

                                <!-- Add to Cart -->
                                <div class="mt-auto">
                                    <div class="flex flex-col sm:flex-row sm:items-center gap-4">
                                        <div class="flex items-center bg-white border border-gray-300 rounded-lg overflow-hidden">
                                            <button @click="decreaseQuantity" 
                                                class="px-4 py-2 text-gray-600 hover:bg-gray-100 transition-colors disabled:opacity-50"
                                                :disabled="quantity <= 1 || product.stock === 0">
                                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                                                </svg>
                                            </button>
                                            <span class="w-12 text-center font-medium">{{ quantity }}</span>
                                            <button @click="increaseQuantity" 
                                                class="px-4 py-2 text-gray-600 hover:bg-gray-100 transition-colors disabled:opacity-50"
                                                :disabled="quantity >= product.stock || product.stock === 0">
                                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                                                </svg>
                                            </button>
                                        </div>
                                        <button @click="addToCart" 
                                            class="flex-1 bg-black text-white py-3 px-6 rounded-lg font-semibold hover:bg-gray-800 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                                            :disabled="product.stock === 0">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                                            </svg>
                                            <span>{{ product.stock === 0 ? 'Out of Stock' : 'Add to Cart' }}</span>
                                        </button>
                                    </div>
                                    <p v-if="!isLoggedIn" class="text-center text-sm text-gray-600 mt-3">
                                        <router-link to="/auth/login/" class="bg-black text-white px-3 py-1 rounded-lg font-medium hover:bg-gray-800 transition-colors inline-flex items-center text-sm text-white">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
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
            
            <!-- Reviews & Ratings Section -->
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
                                                class="h-5 w-5 fill-current" 
                                                viewBox="0 0 20 20" 
                                                fill="currentColor">
                                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118l-2.8-2.034c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                            </svg>
                                        </template>
                                    </div>
                                    <p class="text-sm text-gray-600 mt-1">{{ ratings.length }} {{ ratings.length === 1 ? 'review' : 'reviews' }}</p>
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
                            <div v-if="isLoggedIn && !hasUserRated && product" class="p-6 border-b border-gray-200">
                                <div v-if="ratingSubmitted" class="bg-green-50 p-4 rounded-md mb-4 text-green-700">
                                    Your review has been submitted successfully!
                                </div>
                                <h3 class="text-xl font-semibold mb-4">Write a Review</h3>
                                <div class="space-y-4">
                                    <div>
                                        <label class="block text-gray-700 mb-2">Rating</label>
                                        <div class="flex">
                                            <template v-for="i in 5" :key="i">
                                                <button 
                                                    @click="newRating.rating = i" 
                                                    class="focus:outline-none"
                                                    :class="{'text-yellow-500': i <= newRating.rating, 'text-gray-300': i > newRating.rating}">
                                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 fill-current transform transition-transform hover:scale-110" viewBox="0 0 20 20" fill="currentColor">
                                                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118l-2.8-2.034c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                                    </svg>
                                                </button>
                                            </template>
                                        </div>
                                    </div>
                                    <div>
                                        <label for="review-text" class="block text-gray-700 mb-2">Review</label>
                                        <textarea 
                                            id="review-text"
                                            v-model="newRating.description"
                                            rows="4"
                                            class="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-colors"
                                            placeholder="Share your experience with this product..."></textarea>
                                    </div>
                                    
                                    <!-- Image Upload (Optional) -->
                                    <div>
                                        <label for="review-image" class="block text-gray-700 mb-2">Add Photo (Optional)</label>
                                        <div class="flex items-center">
                                            <label class="cursor-pointer flex items-center justify-center border border-gray-300 rounded-lg p-3 text-gray-600 hover:bg-gray-50 transition-colors">
                                                <span v-if="!imagePreview" class="flex items-center">
                                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                    </svg>
                                                    Choose Photo
                                                </span>
                                                <span v-else class="text-green-600">Change Photo</span>
                                                <input 
                                                    type="file" 
                                                    id="review-image"
                                                    ref="fileInput" 
                                                    @change="handleImageUpload"
                                                    accept="image/jpeg,image/png,image/gif,image/jpg"
                                                    class="hidden"
                                                >
                                            </label>
                                            <button 
                                                v-if="imagePreview" 
                                                @click="removeImage" 
                                                class="ml-3 text-sm text-red-600 hover:text-red-700">
                                                Remove
                                            </button>
                                        </div>
                                        
                                        <!-- Image Preview -->
                                        <div v-if="imagePreview" class="mt-3">
                                            <img 
                                                :src="imagePreview" 
                                                class="h-24 rounded-md border border-gray-200 cursor-pointer hover:opacity-90 transition-opacity" 
                                                @click="openPreviewModal"
                                            />
                                        </div>
                                        <p class="text-xs text-gray-500 mt-1">Supported formats: JPG, JPEG, PNG, GIF (max 5MB)</p>
                                    </div>
                                    
                                    <button 
                                        @click="submitRating" 
                                        :disabled="!newRating.rating || !newRating.description || submittingRating"
                                        class="bg-black text-white px-6 py-3 rounded-lg font-semibold hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                                        <span v-if="!submittingRating">Submit Review</span>
                                        <span v-else class="flex items-center">
                                            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                            </svg>
                                            Submitting...
                                        </span>
                                    </button>
                                </div>
                            </div>
                            
                            <div v-else-if="isLoggedIn && hasUserRated" class="p-6 border-b border-gray-200 bg-gray-50">
                                <p class="text-gray-700">You have already reviewed this product. Thank you for your feedback!</p>
                            </div>
                            
                            <div v-else-if="!isLoggedIn" class="p-6 border-b border-gray-200 bg-gray-50">
                                <p class="text-gray-700">
                                    Please <router-link to="/auth/login" class="bg-black text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-800 transition-colors inline-flex items-center text-white">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                                        </svg>
                                        Log in
                                    </router-link> to leave a review.
                                </p>
                            </div>
                            
                            <!-- Reviews List -->
                            <div v-if="ratings.length > 0">
                                <div v-for="(rating, index) in ratings" :key="rating.id" 
                                    class="p-6" 
                                    :class="{'border-b border-gray-200': index < ratings.length - 1}">
                                    <div class="flex items-start">
                                        <div class="mr-4">
                                            <div class="w-10 h-10 bg-yellow-500 rounded-full flex items-center justify-center text-white font-bold">
                                                {{ (rating.user_name && rating.user_name.charAt(0)) || 
                                                   (typeof rating.user === 'string' ? rating.user.charAt(0) : 'U') }}
                                            </div>
                                        </div>
                                        <div class="flex-1">
                                            <!-- User and rating stars -->
                                            <div class="flex flex-wrap items-center gap-2 mb-1">
                                                <span class="font-medium text-gray-800">{{ rating.user_name || rating.first_name || rating.username || 'User' }}</span>
                                                <div class="flex">
                                                    <template v-for="i in 5" :key="i">
                                                        <svg xmlns="http://www.w3.org/2000/svg" 
                                                            :class="[i <= rating.rating ? 'text-yellow-500' : 'text-gray-300']"
                                                            class="h-4 w-4 fill-current" 
                                                            viewBox="0 0 20 20" 
                                                            fill="currentColor">
                                                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118l-2.8-2.034c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                                        </svg>
                                                    </template>
                                                </div>
                                            </div>

                                            <!-- Date -->
                                            <div class="text-sm text-gray-500 mb-2">{{ formatDate(rating.created_at) }}</div>
                                            
                                            <!-- Review content -->
                                            <p class="text-gray-700 whitespace-pre-line mb-3">{{ rating.description }}</p>
                                            
                                            <!-- Review image if any -->
                                            <div v-if="rating.image_url" class="mt-2">
                                                <img 
                                                    :src="getRatingImageUrl(rating.image_url)" 
                                                    alt="Review image" 
                                                    class="h-24 w-auto rounded-md border border-gray-200 cursor-pointer hover:opacity-90 transition-opacity" 
                                                    @click="openImageModal(rating.image_url)"
                                                />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div v-else class="p-6 text-center">
                                <p class="text-gray-600">No reviews yet. Be the first to review this product!</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Image Modal -->
        <div v-if="showImageModal" class="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4" @click="closeImageModal">
            <div class="relative max-w-4xl max-h-full">
                <img 
                    :src="isPreviewImage ? modalImageUrl : getRatingImageUrl(modalImageUrl)" 
                    alt="Enlarged image" 
                    class="max-w-full max-h-[90vh] object-contain rounded-lg shadow-xl"
                />
                <button 
                    @click.stop="closeImageModal" 
                    class="absolute top-3 right-3 bg-black bg-opacity-50 text-white rounded-full p-2 hover:bg-opacity-70 transition-colors"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

// Create axios instance with CSRF token handling
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    withCredentials: true
});

// Get CSRF token from cookies
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

// Add request interceptor to set CSRF token
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
            userHasRatedProduct: false,  // Flag set by fetchRatings when user has already rated
            showImageModal: false,       // Controls the modal visibility
            modalImageUrl: null,         // URL of the image to display in the modal
            isPreviewImage: false        // Flag to differentiate between preview images and review images
        };
    },
    computed: {
        categoryName() {
            if (!this.product) return 'Loading...';
            return this.product.category_name || 'Unknown Category';
        },
        isLoggedIn() {
            return localStorage.getItem('isAuthenticated') === 'true';
        },
        averageRating() {
            if (!this.ratings || this.ratings.length === 0) return 0;
            const sum = this.ratings.reduce((total, rating) => total + rating.rating, 0);
            return (sum / this.ratings.length).toFixed(1);
        },
        hasUserRated() {
            // Use the flag set by the fetchRatings method that checks directly with the backend
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
            
            // Check if the path is already a complete URL
            if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
                return imagePath;
            }
            
            // If path contains '/media/rating_images/', it's a relative Django path
            if (imagePath.includes('/media/rating_images/')) {
                // Make sure it starts with the base URL if it's a relative path
                if (imagePath.startsWith('/')) {
                    return `http://127.0.0.1:8000${imagePath}`;
                }
                return `http://127.0.0.1:8000/${imagePath}`;
            }
            
            // If it's just a filename, construct the full URL with all necessary parts
            if (!imagePath.includes('/')) {
                return `http://127.0.0.1:8000/media/rating_images/${imagePath}`;
            }
            
            // For any other format, ensure the URL is properly formed
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
                const productId = this.$route.params.id;
                const response = await api.get(`/products/${productId}`);
                this.product = response.data;
                this.newRating.product = this.product.product_id;
                this.loading = false;
                this.fetchRatings();
            } catch (error) {
                console.error("Error fetching product:", error);
                this.loading = false;
            }
        },
        async fetchRatings() {
            if (!this.product) return;
            
            try {
                // Get ratings for this product
                const response = await api.get(`/ratings/`, {
                    params: {
                        product: this.product.product_id
                    }
                });
                
                // Log the complete first rating object to see all available fields
                if (response.data && response.data.length > 0) {
                    console.log("First rating object:", response.data[0]);
                }
                
                // Process the ratings to ensure image URLs are correct
                this.ratings = response.data.map(rating => {
                    // Log for debugging
                    console.log("Original rating image_url:", rating.image_url);
                    
                    // Process rating to ensure we have a username for display
                    const processedRating = { ...rating };
                    
                    // Try to extract the username from various possible fields
                    if (!processedRating.user_name) {
                        if (typeof processedRating.user === 'object' && processedRating.user !== null) {
                            // If user is an object, try to get name from it
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
                
                // Log the first rating's processed image URL if available
                if (this.ratings.length > 0 && this.ratings[0].image_url) {
                    console.log("Processed first rating image URL:", 
                                this.getRatingImageUrl(this.ratings[0].image_url));
                }
                
                // Check if user-specific ratings exist
                if (this.isLoggedIn) {
                    try {
                        // Try to get user-specific ratings to determine if the user has already rated
                        const userRatingsResponse = await api.get(`/ratings/`, {
                            params: {
                                product: this.product.product_id,
                                user_ratings: true  // This flag is in the backend view to filter by user
                            }
                        });
                        
                        // If we get any ratings back, the user has already rated this product
                        if (userRatingsResponse.data && userRatingsResponse.data.length > 0) {
                            this.userHasRatedProduct = true;
                        } else {
                            this.userHasRatedProduct = false;
                        }
                    } catch (userRatingError) {
                        console.error("Could not fetch user-specific ratings:", userRatingError);
                    }
                    
                    // Still get the user profile for display purposes
                    this.getCurrentUser();
                }
            } catch (error) {
                console.error("Error fetching ratings:", error);
            }
        },
        async getCurrentUser() {
            try {
                // Get the profile data from the API - this is just for displaying user info
                // We don't need to extract the ID, as Django will use request.user.id on the backend
                const response = await api.get('/api/profile/');
                
                // Store the profile data for display purposes
                this.userProfile = response.data;
                
                // For the hasUserRated check, we just need some user identifier
                if (response.data) {
                    // Get user profile information
                    this.userProfile = response.data;
                    
                    // Django's UserProfile model likely has a user field that links to the auth.User model
                    // It could be accessed in different ways
                    if (response.data.id) {
                        // If the profile itself has an ID
                        this.currentUserId = response.data.id;
                    } else if (response.data.user && response.data.user.id) {
                        // If the profile has a user object with ID
                        this.currentUserId = response.data.user.id;
                    } else if (response.data.user_id) {
                        // If the profile has a user_id field directly
                        this.currentUserId = response.data.user_id;
                    } else {
                        // Last resort - use a default ID
                        this.currentUserId = 1; // Your system might use Django's first user, which is often ID 1
                    }
                }
            } catch (error) {
                console.error("Could not fetch user profile:", error);
                // Continue without user profile data - Django will still use session auth
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
        async submitRating() {
            if (!this.newRating.rating || !this.newRating.description || !this.product) return;
            
            this.submittingRating = true;
            
            try {
                console.log("Starting submitRating process");
                // First, we need to find the current user's ID
                let userId = null;
                let profileResponse = null;
                
                // Make a request to the profile endpoint to get the current user information
                try {
                    console.log("Fetching user profile data");
                    profileResponse = await api.get('/api/profile/');
                    console.log("Profile response:", profileResponse.data);
                    
                    if (profileResponse.data) {
                        // Get user profile information
                        this.userProfile = profileResponse.data;
                        
                        // Django's UserProfile model likely has a user field that links to the auth.User model
                        // It could be accessed in different ways
                        if (profileResponse.data.id) {
                            // If the profile itself has an ID
                            userId = profileResponse.data.id;
                            console.log("Using profile ID:", userId);
                        } else if (profileResponse.data.user && profileResponse.data.user.id) {
                            // If the profile has a user object with ID
                            userId = profileResponse.data.user.id;
                            console.log("Using user.id:", userId);
                        } else if (profileResponse.data.user_id) {
                            // If the profile has a user_id field directly
                            userId = profileResponse.data.user_id;
                            console.log("Using user_id:", userId);
                        } else {
                            // Look at all available fields to help debug
                            console.log("Profile object keys:", Object.keys(profileResponse.data));
                            console.log("Full profile data:", JSON.stringify(profileResponse.data));
                            
                            // Last resort - use a default ID
                            userId = 1; // Your system might use Django's first user, which is often ID 1
                            console.log("Using default ID:", userId);
                        }
                    } else {
                        console.log("No profile data received");
                    }
                } catch (profileError) {
                    console.error("Error fetching profile:", profileError);
                    if (profileError.response) {
                        console.error("Profile error response:", profileError.response.data);
                        console.error("Profile error status:", profileError.response.status);
                    }
                    // Continue with the attempt even if profile fetch fails
                }
                
                // Prepare rating data with user ID explicitly included
                const ratingData = {
                    product: this.product.product_id,
                    rating: this.newRating.rating,
                    description: this.newRating.description,
                };
                
                // Only add the user field if we have a valid ID
                if (userId) {
                    ratingData.user = userId;
                }
                
                // Add user name if available from the profile response
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
                
                // Add a special token to indicate this is an authenticated request
                // Some Django backends can use this with custom authentication
                ratingData.auth_token = localStorage.getItem('token') || 'auth_session_active';
                
                // Check if we have a file to upload
                const fileInput = this.$refs.fileInput;
                const hasImage = fileInput && fileInput.files && fileInput.files.length > 0;
                
                console.log("Rating data being submitted:", { ...ratingData, auth_token: "[redacted]" });
                console.log("Has image:", hasImage);
                
                let response;
                
                // Handle form data if we have an image
                if (hasImage) {
                    const formData = new FormData();
                    
                    // Add essential data
                    formData.append('product', this.product.product_id);
                    formData.append('rating', this.newRating.rating);
                    formData.append('description', this.newRating.description);
                    
                    // Only add user ID if we have one
                    if (userId) {
                        formData.append('user', userId);
                    }
                    
                    // Add auth token for authenticated requests
                    formData.append('auth_token', localStorage.getItem('token') || 'auth_session_active');
                    
                    // Add user name if available
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
                    
                    // Add the file
                    const file = fileInput.files[0];
                    console.log("File being uploaded:", file);
                    console.log("File name:", file.name);
                    console.log("File type:", file.type);
                    console.log("File size:", file.size, "bytes");
                    
                    // Use only one field name for image upload
                    formData.append('image_url', file);
                    
                    // Debug FormData content
                    console.log("FormData entries:");
                    for (let pair of formData.entries()) {
                        console.log(pair[0] + ': ' + (pair[0] === 'image_url' ? '[FILE]' : pair[1]));
                    }
                    
                    // Ensure correct endpoint is being used
                    const ratingEndpoint = '/ratings/create/';
                    console.log(`Submitting rating with image to ${ratingEndpoint}`);
                    
                    try {
                        response = await api.post(ratingEndpoint, formData, {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            },
                            withCredentials: true // Ensure cookies are passed
                        });
                    } catch (innerError) {
                        // Try alternative endpoint if the first one fails
                        console.error("Error with first endpoint:", innerError);
                        console.log("Trying alternative endpoint...");
                        
                        // Some Django configurations might use a different endpoint pattern
                        const altEndpoint = '/api/ratings/create/';
                        response = await api.post(altEndpoint, formData, {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            },
                            withCredentials: true
                        });
                    }
                } else {
                    // Simple JSON post with user ID included
                    const ratingEndpoint = '/ratings/create/';
                    console.log(`Submitting rating without image to ${ratingEndpoint}`);
                    
                    try {
                        response = await api.post(ratingEndpoint, ratingData, {
                            withCredentials: true // Ensure cookies are passed
                        });
                    } catch (innerError) {
                        // Try alternative endpoint if the first one fails
                        console.error("Error with first endpoint:", innerError);
                        console.log("Trying alternative endpoint...");
                        
                        // Some Django configurations might use a different endpoint pattern
                        const altEndpoint = '/api/ratings/create/';
                        response = await api.post(altEndpoint, ratingData, {
                            withCredentials: true
                        });
                    }
                }
                
                console.log("Rating submission successful:", response.data);
                
                // Show success message
                this.ratingSubmitted = true;
                
                // Make sure the submitted rating includes a proper user_name
                if (response && response.data) {
                    // Create a processed rating with user name attached
                    const processedNewRating = { ...response.data };
                    
                    // Add the user name from the profile data since it's not in the response
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
                    
                    // Add the new rating to the top of the list
                    this.ratings.unshift(processedNewRating);
                    
                    console.log("Successfully added rating with user_name:", processedNewRating.user_name);
                }
                
                // Reset form
                this.newRating = {
                    rating: 0,
                    description: '',
                    product: this.product.product_id
                };
                this.imagePreview = null;
                if (fileInput) fileInput.value = '';
                
                // Refresh ratings
                this.fetchRatings();
                
                // If we had an image, make sure the UI is updated with the correct URL
                if (response && response.data && response.data.image_url) {
                    console.log("Submitted rating with image:", response.data.image_url);
                }
                
                // Hide success message after a few seconds
                setTimeout(() => {
                    this.ratingSubmitted = false;
                }, 3000);
            } catch (error) {
                console.error("Error submitting rating:", error);
                
                if (error.response) {
                    console.error("Error response data:", error.response.data);
                    console.error("Error response status:", error.response.status);
                    console.error("Error response headers:", error.response.headers);
                    
                    if (error.response.status === 403) {
                        alert("You have already reviewed this product.");
                        this.fetchRatings();
                    } else if (error.response.status === 400) {
                        // Handle 400 Bad Request
                        let errorMessage = "There was an error submitting your review. ";
                        
                        if (error.response.data) {
                            if (typeof error.response.data === 'string') {
                                errorMessage += error.response.data;
                            } else if (typeof error.response.data === 'object') {
                                // Check for specific field errors
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
                    console.error("No response received:", error.request);
                    alert("Network error - the server didn't respond. Please check your connection and try again.");
                } else {
                    console.error("Error message:", error.message);
                    console.error("Full error:", error);
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
                const cartResponse = await api.get('/cart/');
                const cart = cartResponse.data[0]; 

                const existingItem = cart.cart_items.find(item => item.product === this.product.product_id);
                
                // Calculate the quantity difference for the cart count
                let quantityToAdd = this.quantity;
                
                // If item exists, we're only adding the difference in quantity
                if (existingItem) {
                    quantityToAdd = this.quantity - existingItem.quantity;
                    if (quantityToAdd < 0) quantityToAdd = 0; // Prevent negative values
                }
                
                await api.post(`/cart/${cart.cart_id}/items/`, {
                    product: this.product.product_id,
                    quantity: this.quantity
                });

                // Update total item count
                const currentCount = parseInt(localStorage.getItem('cartCount') || '0');
                localStorage.setItem('cartCount', (currentCount + quantityToAdd).toString());
                window.dispatchEvent(new Event('cart-updated'));

                // Redirect to cart page
                this.$router.push('/cart');
            } catch (error) {
                console.error('Error adding to cart:', error);
                if (error.response && error.response.status === 401) {
                    this.$router.push('/auth/login/');
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
            // Prevent scrolling when modal is open
            document.body.style.overflow = 'hidden';
        },
        closeImageModal() {
            this.showImageModal = false;
            // Re-enable scrolling when modal is closed
            document.body.style.overflow = 'auto';
        },
        openPreviewModal() {
            // For preview images, use the imagePreview directly since it's already a data URL
            this.modalImageUrl = this.imagePreview;
            this.isPreviewImage = true;
            this.showImageModal = true;
            document.body.style.overflow = 'hidden';
        }
    },
    created() {
        this.fetchCategories();
        this.fetchProduct();
    },
    watch: {
        // Reset and refetch when the route changes (for navigating between products)
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

/* Add animation for placeholder loading */
@keyframes pulse {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.8;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
