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
  import api, { isAuthenticated, getCsrfToken } from "../auth";
  
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
          console.log("Attempting login...");
          
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

          console.log("Login response:", {
            status: response.status,
            statusText: response.statusText,
            data: response.data
          });

          if (response.status === 200) {
            // The backend sets HTTP-only cookies automatically
            localStorage.setItem('isAuthenticated', 'true');
            
            console.log("Login successful - Navigating to profile...");
            
            try {
              await this.$router.push("/profile/");
              console.log("Navigation successful");
            } catch (routerError) {
              console.error("Router navigation error:", routerError);
              window.location.href = "/profile/";
            }
          } else {
            console.error("Login failed: Unexpected response status");
            alert("Login failed. Please try again.");
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
          
          let errorMessage = "Login failed. ";
          if (error.response?.data?.detail) {
            errorMessage += error.response.data.detail;
          } else if (error.response?.data?.message) {
            errorMessage += error.response.data.message;
          } else if (error.response?.status === 400) {
            errorMessage += "Please check your credentials.";
          } else {
            errorMessage += "Please try again.";
          }
          
          alert(errorMessage);
        }
      }
    }
  };
</script>