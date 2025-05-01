<template>
  <div class="bg-gray-100 min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-md">
      <div class="bg-white shadow-2xl rounded-3xl overflow-hidden">
        <!-- Header with Logo -->
        <div class="bg-gradient-to-r from-gray-900 to-gray-800 px-8 py-10 text-center">
          <img src="/icon.png" alt="Juan Click Wonders" class="h-20 w-20 mx-auto mb-2">
          <h2 class="text-2xl font-bold text-white">Log In</h2>
          <p class="text-gray-300 mt-2">Sign in to your account to continue</p>
        </div>

        <!-- Form -->
        <div class="p-8">
          <form @submit.prevent="login" class="space-y-6">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
              <div class="mt-1 relative rounded-md">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </div>
                <input
                  id="email"
                  v-model="email"
                  type="email"
                  required
                  class="pl-10 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                  placeholder="Enter your email"
                />
              </div>
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <div class="mt-1 relative rounded-md">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input
                  id="password"
                  v-model="password"
                  type="password"
                  required
                  class="pl-10 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                  placeholder="Enter your password"
                />
              </div>
            </div>

            <!-- Alert Message -->
            <div v-if="message" class="p-4 bg-red-50 border-l-4 border-red-500 rounded-md">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm text-red-700">{{ message }}</p>
                </div>
              </div>
            </div>

            <div class="flex items-center justify-end">
              <div class="text-sm">
              <a href="/auth/forgot-password" class="font-medium text-yellow-600 hover:text-yellow-500">
                Forgot password?
              </a>
              </div>
            </div>

            <div>
              <button
                type="submit"
                class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-gray-800 to-black hover:from-black hover:to-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition duration-150"
              >
                <span v-if="isLoading" class="flex items-center">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Signing in...
                </span>
                <span v-else>Sign in</span>
              </button>
            </div>
          </form>

          <div class="mt-8 text-center">
            <p class="text-sm text-gray-600">
              Don't have an account?
              <router-link to="/auth/register" class="font-medium text-yellow-600 hover:text-yellow-500">
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
import api, { isAuthenticated, getCsrfToken } from "../auth";

export default {
  data() {
    return {
      email: "",
      password: "",
      message: "",
      isLoading: false
    };
  },
  methods: {
    async login() {
      this.message = ""; // Clear any existing message
      this.isLoading = true;
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/auth/login/", {
          email: this.email,
          password: this.password
        }, {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        });

        if (response.status === 200) {
          // The backend sets HTTP-only cookies automatically
          localStorage.setItem('isAuthenticated', 'true');

          // Try to get user's name for better UX
          if (response.data?.user?.first_name) {
            localStorage.setItem('userName', response.data.user.first_name);
          }

          // Initialize cart count to 0 on fresh login
          localStorage.setItem('cartCount', '0');
          window.dispatchEvent(new Event('cart-updated'));
          window.dispatchEvent(new Event('auth-state-changed'));

          try {
            await this.$router.push("/profile/");
          } catch (routerError) {
            console.error("Router navigation error:", routerError);
            window.location.href = "/profile/";
          }
        } else {
          console.error("Login failed: Unexpected response status");
          this.message = "Login failed. Please try again.";
          this.isLoading = false;
        }
      } catch (error) {
        console.error("Login error:", {
          message: error.message,
          response: error.response ? {
            status: error.response.status,
            data: error.response.data,
            statusText: error.response.statusText
          } : 'No response'
        });

        this.message = "Invalid email or password, please check your credentials.";
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Add any page-specific styles here */
</style>