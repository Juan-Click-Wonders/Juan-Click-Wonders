<template>
  <div class="bg-gray-100 min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-2xl">
      <div class="bg-white shadow-2xl rounded-3xl overflow-hidden">
        <!-- Header with Logo -->
        <div class="bg-gradient-to-r from-gray-900 to-gray-800 px-8 py-8 text-center">
          <img src="/icon.png" alt="Juan Click Wonders" class="h-16 w-16 mx-auto mb-2">
          <h2 class="text-2xl font-bold text-white">Create Your Account</h2>
          <p class="text-gray-300 mt-2">Join our community of shoppers today</p>
        </div>

        <!-- Form -->
        <div class="p-8">
          <form @submit.prevent="register" class="space-y-6">
            <!-- Two column layout for name fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
                <div class="mt-1 relative rounded-md">
                  <input 
                    id="first_name"
                    v-model="first_name" 
                    type="text" 
                    required
                    class="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                    placeholder="Enter your first name"
                  />
                </div>
              </div>

              <div>
                <label for="last_name" class="block text-sm font-medium text-gray-700">Last Name</label>
                <div class="mt-1 relative rounded-md">
                  <input 
                    id="last_name"
                    v-model="last_name" 
                    type="text" 
                    required
                    class="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                    placeholder="Enter your last name"
                  />
                </div>
              </div>
            </div>

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
              <label for="phone_number" class="block text-sm font-medium text-gray-700">Phone Number</label>
              <div class="mt-1 relative rounded-md">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
                <input 
                  id="phone_number"
                  v-model="phone_number" 
                  type="text" 
                  required
                  class="pl-10 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                  placeholder="Enter your phone number"
                />
              </div>
            </div>

            <div>
              <label for="address" class="block text-sm font-medium text-gray-700">Address</label>
              <div class="mt-1 relative rounded-md">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <input 
                  id="address"
                  v-model="address" 
                  type="text" 
                  required
                  class="pl-10 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                  placeholder="Enter your address"
                />
              </div>
            </div>

            <!-- Two column layout for password fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="password1" class="block text-sm font-medium text-gray-700">Password</label>
                <div class="mt-1 relative rounded-md">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <input 
                    id="password1"
                    v-model="password1" 
                    type="password" 
                    required
                    class="pl-10 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                    placeholder="Enter your password"
                  />
                </div>
                <p v-if="passwordError" class="mt-1 text-sm text-red-600">{{ passwordError }}</p>
              </div>

              <div>
                <label for="password2" class="block text-sm font-medium text-gray-700">Confirm Password</label>
                <div class="mt-1 relative rounded-md">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <input 
                    id="password2"
                    v-model="password2" 
                    type="password" 
                    required
                    class="pl-10 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                    placeholder="Confirm your password"
                  />
                </div>
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
                  Creating Account...
                </span>
                <span v-else>Create Account</span>
              </button>
            </div>
          </form>

          <div class="mt-6 text-center">
            <p class="text-sm text-gray-600">
              Already have an account? 
              <router-link to="/auth/login" class="font-medium text-yellow-600 hover:text-yellow-500">
                Sign in instead
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
import { validatePassword } from "../utils/validation";

export default {
  data() {
    return {
      first_name: "",
      last_name: "",
      phone_number: "",
      address: "",
      email: "",
      password1: "",
      password2: "",
      passwordError: "",
      message: "",
      isLoading: false
    };
  },
  methods: {
    async register() {
      // Reset error messages
      this.passwordError = "";
      this.message = "";
      
      // Validate password
      const passwordError = validatePassword(this.password1);
      if (passwordError) {
        this.passwordError = passwordError;
        return;
      }

      if (this.password1 !== this.password2) {
        this.message = "Passwords do not match!";
        return;
      }

      this.isLoading = true;

      const userData = {
        first_name: this.first_name,
        last_name: this.last_name,
        phone_number: this.phone_number,
        address: this.address,
        email: this.email,
        password1: this.password1,
        password2: this.password2
      };

      try {
        const response = await axios.post("http://127.0.0.1:8000/api/auth/register/", userData);
        if (response.status === 201) {
          // Display success message or redirect immediately
          setTimeout(() => {
            this.$router.push("/auth/login/?registered=true");
          }, 1000);
        }
      } catch (error) {
        this.isLoading = false;
        if (error.response && error.response.status === 400) {
          if (error.response.data) {
            // Handle specific validation errors from backend
            if (error.response.data.email) {
              this.message = `Email error: ${error.response.data.email[0]}`;
            } else if (error.response.data.password1) {
              this.passwordError = error.response.data.password1[0];
            } else {
              this.message = "Please check your details. Some information is invalid.";
            }
          } else {
            this.message = "Please check your details. All fields are required.";
          }
        } else {
          console.error("Registration failed:", error);
          this.message = "An unexpected error occurred. Please try again.";
        }
      }
    }
  }
};
</script>

<style scoped>
/* Add any page-specific styles here */
</style>


<!-- asd@jcw.com - jcwadmin123
qwe@jcw.com - jcwadmin123
james@gmail.com - jamespogi123
james@jcw.com - admin123 -->