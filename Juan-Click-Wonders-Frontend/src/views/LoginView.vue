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
  
  export default {
    data() {
      return {
        email: "",
        password: "",
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post("http://127.0.0.1:8000/api/auth/login/", {
            email: this.email,
            password: this.password,
          });

          // Log response to check token structure
          console.log("API Response:", response.data);
          // Extract token from the correct response structure
          const accessToken = response.data.set_cookies.access_token;
          const refreshToken = response.data.set_cookies.refresh_token; // In case you also need refresh token

          if (accessToken) {
            localStorage.setItem("access_token", accessToken);
            localStorage.setItem("refresh_token", refreshToken); // Store refresh token if needed
            axios.defaults.headers.common["Authorization"] = `Bearer ${accessToken}`;
            this.$router.push("/profile/"); // Redirect to profile
          } else {
            console.error("Login failed: No access token received.");
          }
        } catch (error) {
          console.error("Login error:", error);
        }
        },
      },
    };
  </script>