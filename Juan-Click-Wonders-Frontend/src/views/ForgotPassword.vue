<template>
  <div class="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-xl mx-auto">
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-gray-900 to-gray-800 p-6 flex items-center">
          <router-link to="/auth/login" class="text-white mr-4 hover:text-gray-300 transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </router-link>
          <h2 class="text-xl font-bold text-white">Forgot Password</h2>
        </div>

        <!-- Form section -->
        <div class="p-8">
          <p class="text-gray-600 mb-6">
            Enter your email address and we'll send you a link to reset your password.
          </p>

          <div v-if="successMessage" class="mb-6 p-4 rounded-lg bg-green-100 text-green-700 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            {{ successMessage }}
          </div>
          
          <form @submit.prevent="resetPassword" class="space-y-6">
            <!-- Email field -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <input 
                  v-model="email" 
                  type="email" 
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-black focus:border-black" 
                  placeholder="Enter your email address" 
                  required 
                />
              </div>
            </div>

            <div v-if="errorMessage" class="p-4 rounded-lg bg-red-100 text-red-700 text-sm">
              {{ errorMessage }}
            </div>

            <!-- Action buttons -->
            <div class="flex space-x-4 pt-2">
              <router-link 
                to="/auth/login" 
                class="flex-1 py-3 border border-gray-300 rounded-lg text-center text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition"
              >
                Back to Login
              </router-link>
              <button 
                type="submit" 
                class="flex-1 bg-black text-white py-3 rounded-lg hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black transition"
                :disabled="isSubmitting"
              >
                <span v-if="isSubmitting">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Sending...
                </span>
                <span v-else>Send Reset Link</span>
              </button>
            </div>
          </form>

          <div class="mt-8 text-center">
            <p class="text-sm text-gray-600">
              Don't have an account? 
              <router-link to="/auth/register" class="font-medium text-black hover:underline transition">
                Create one now
              </router-link>
            </p>
          </div>
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
      email: "",
      errorMessage: "",
      successMessage: "",
      isSubmitting: false
    };
  },
  methods: {
    async resetPassword() {
      this.errorMessage = ""; // Clear any existing message
      this.successMessage = "";
      this.isSubmitting = true;
      
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/auth/forgot-password/", {
          email: this.email
        });
        
        if (response.status === 200) {
          this.successMessage = "Password reset instructions have been sent to your email.";
          
          // Redirect after a short delay
          setTimeout(() => {
            this.$router.push("/auth/login/");
          }, 3000);
        }
      } catch (error) {
        console.error("Password reset error:", error);
        if (error.response?.data?.email) {
          this.errorMessage = error.response.data.email[0];
        } else if (error.response?.data?.non_field_errors) {
          this.errorMessage = error.response.data.non_field_errors[0];
        } else {
          this.errorMessage = "Failed to send reset instructions. Please try again.";
        }
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>

<style scoped>
input:focus {
  outline: none;
  border-color: black;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1);
}

.transition {
  transition: all 0.3s ease;
}
</style>
