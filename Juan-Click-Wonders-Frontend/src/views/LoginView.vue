<template>
    <div class="flex items-start pt-20 justify-center min-h-screen bg-gray-100">
      <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg overflow-hidden">
        <div class="bg-black text-white text-center py-6">
          <h2 class="text-lg font-semibold">Login</h2>
        </div>
        <div class="p-8">
          <h3 class="text-xl font-medium text-gray-900">Welcome Back</h3>
          <form @submit.prevent="login" class="mt-4">
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input v-model="email" type="email" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter your email" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">Password</label>
              <input v-model="password" type="password" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter your password" required />
            </div>
            <div v-if="message" class="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-base">
              {{ message }}
            </div>
            <div class="text-center text-sm text-gray-500">
              <a href="/auth/forgot-password" class="hover:underline">Forgot password?</a>
            </div>
            <button type="submit" class="w-full mt-4 bg-black text-white py-2 rounded-full hover:bg-gray-800">Login</button>
          </form>
          <div class="text-center text-sm text-gray-500 mt-3">
            Don't have an account? <a href="/auth/register" class="text-black font-medium hover:underline">Sign up now!</a>
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
        message: ""
      };
    },
    methods: {
      async login() {
        this.message = ""; // Clear any existing message
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
          
          this.message = "Invalid email or password, check your credentials.";
        }
      }
    }
  };
</script>