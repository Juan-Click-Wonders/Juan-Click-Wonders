<template>
  <div class="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-xl mx-auto">
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <!-- Header with back button -->
        <div class="bg-gradient-to-r from-gray-900 to-gray-800 p-6 flex items-center">
          <button @click="$router.push('/profile/')" class="text-white mr-4 hover:text-gray-300 transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <h2 class="text-xl font-bold text-white">Edit Profile</h2>
        </div>

        <!-- Form section -->
        <div class="p-8">
          <div v-if="formSubmitted && !message" class="mb-6 p-4 rounded-lg bg-green-100 text-green-700 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Profile updated successfully!
          </div>
          
          <form @submit.prevent="updateProfile" class="space-y-6">
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
                  type="email" 
                  v-model="email" 
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-black focus:border-black" 
                  required 
                />
              </div>
              <div v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</div>
            </div>

            <!-- Phone field -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
                <input 
                  type="text" 
                  v-model="phoneNumber" 
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-black focus:border-black" 
                  required 
                />
              </div>
              <div v-if="errors.phoneNumber" class="mt-1 text-sm text-red-600">{{ errors.phoneNumber }}</div>
            </div>

            <!-- Address field -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <textarea 
                  v-model="address" 
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-black focus:border-black"
                  rows="3" 
                  required
                ></textarea>
              </div>
              <div v-if="errors.address" class="mt-1 text-sm text-red-600">{{ errors.address }}</div>
            </div>

            <!-- Current password field -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input 
                  type="password" 
                  v-model="currentPassword" 
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-black focus:border-black" 
                  required 
                />
              </div>
              <div v-if="errors.currentPassword" class="mt-1 text-sm text-red-600">{{ errors.currentPassword }}</div>
            </div>

            <!-- Error message -->
            <div v-if="message" class="p-4 rounded-lg bg-red-100 text-red-700 text-sm">
              {{ message }}
            </div>

            <!-- Action buttons -->
            <div class="flex space-x-4 pt-2">
              <button 
                type="button" 
                @click="$router.push('/profile/')" 
                class="flex-1 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition"
              >
                Cancel
              </button>
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
                  Updating...
                </span>
                <span v-else>Save Changes</span>
              </button>
            </div>
          </form>
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
      phoneNumber: '',
      address: '',
      email: '',
      currentPassword: '',
      message: null,
      isSubmitting: false,
      formSubmitted: false,
      errors: {
        email: null,
        phoneNumber: null,
        address: null,
        currentPassword: null
      }
    };
  },
  async created() {
    if (!localStorage.getItem('isAuthenticated')) {
      this.$router.push("/auth/login/");
      return;
    }
    
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/profile/", {
        withCredentials: true
      });
      
      const profile = response.data;
      this.phoneNumber = profile.phone_number || '';
      this.address = profile.address || '';
      this.email = profile.email || '';
    } catch (error) {
      console.error("Error loading profile:", error);
      if (error.response?.status === 401) {
        localStorage.removeItem('isAuthenticated');
        this.$router.push("/auth/login/");
      }
    }
  },
  methods: {
    validateForm() {
      let isValid = true;
      // Reset errors
      this.errors = {
        email: null,
        phoneNumber: null,
        address: null,
        currentPassword: null
      };
      
      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        this.errors.email = "Please enter a valid email address";
        isValid = false;
      }
      
      // Phone validation (simple check)
      if (this.phoneNumber.length < 10) {
        this.errors.phoneNumber = "Please enter a valid phone number";
        isValid = false;
      }
      
      // Address validation
      if (this.address.trim().length < 5) {
        this.errors.address = "Please enter a complete address";
        isValid = false;
      }
      
      // Password required
      if (!this.currentPassword) {
        this.errors.currentPassword = "Current password is required";
        isValid = false;
      }
      
      return isValid;
    },
    async updateProfile() {
      if (!this.validateForm()) {
        return;
      }
      
      this.isSubmitting = true;
      this.message = null;
      this.formSubmitted = false;
      
      try {
        const response = await axios.put("http://127.0.0.1:8000/api/profile/update/", {
          phone_number: this.phoneNumber,
          address: this.address,
          email: this.email,
          current_password: this.currentPassword
        }, {
          withCredentials: true
        });

        this.formSubmitted = true;
        this.currentPassword = '';
        
        // Redirect after a short delay to show success message
        setTimeout(() => {
          this.$router.push("/profile/");
        }, 1500);
      } catch (error) {
        console.error("Profile update error:", error);
        if (error.response?.data?.current_password) {
          this.message = "Incorrect password. Please check your current password.";
          this.errors.currentPassword = "Incorrect password";
        } else if (error.response?.data?.email) {
          this.message = "Email error: " + error.response.data.email[0];
          this.errors.email = error.response.data.email[0];
        } else if (error.response?.data?.phone_number) {
          this.message = "Phone error: " + error.response.data.phone_number[0];
          this.errors.phoneNumber = error.response.data.phone_number[0];
        } else if (error.response?.data?.address) {
          this.message = "Address error: " + error.response.data.address[0];
          this.errors.address = error.response.data.address[0];
        } else {
          this.message = "Failed to update profile. Please check your details and try again.";
        }
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
input:focus, textarea:focus {
  outline: none;
  border-color: black;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1);
}

.transition {
  transition: all 0.3s ease;
}
</style>
  