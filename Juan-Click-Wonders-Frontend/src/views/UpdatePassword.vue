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
          <h2 class="text-xl font-bold text-white">Update Password</h2>
        </div>

        <!-- Form section -->
        <div class="p-8">
          <div v-if="passwordUpdated" class="mb-6 p-4 rounded-lg bg-green-100 text-green-700 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Password updated successfully!
          </div>

          <form @submit.prevent="updatePassword" class="space-y-6">
            <!-- Current Password field -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input 
                  v-model="currentPassword" 
                  type="password" 
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-black focus:border-black" 
                  placeholder="Enter current password" 
                  required 
                />
              </div>
              <div v-if="errors.currentPassword" class="mt-1 text-sm text-red-600">{{ errors.currentPassword }}</div>
            </div>

            <!-- New Password field -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">New Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                  </svg>
                </div>
                <input 
                  v-model="newPassword" 
                  type="password" 
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-black focus:border-black" 
                  placeholder="Enter new password" 
                  required 
                />
              </div>
              <div v-if="errors.newPassword" class="mt-1 text-sm text-red-600">{{ errors.newPassword }}</div>
              
              <!-- Password strength meter -->
              <div v-if="newPassword" class="mt-2">
                <div class="mb-1 flex justify-between">
                  <p class="text-xs text-gray-500">Password strength:</p>
                  <p class="text-xs" :class="strengthColor">{{ strengthText }}</p>
                </div>
                <div class="h-1 w-full bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    class="h-full rounded-full transition-all duration-300" 
                    :class="strengthBarColor"
                    :style="{ width: `${passwordStrengthPercent}%` }"
                  ></div>
                </div>
                <ul class="mt-2 text-xs text-gray-500 space-y-1">
                  <li class="flex items-center">
                    <span :class="[newPassword.length >= 8 ? 'text-green-500' : 'text-gray-400']">
                      <svg v-if="newPassword.length >= 8" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </span>
                    At least 8 characters
                  </li>
                  <li class="flex items-center">
                    <span :class="[/[a-zA-Z]/.test(newPassword) ? 'text-green-500' : 'text-gray-400']">
                      <svg v-if="/[a-zA-Z]/.test(newPassword)" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </span>
                    Includes letters
                  </li>
                  <li class="flex items-center">
                    <span :class="[/\d/.test(newPassword) ? 'text-green-500' : 'text-gray-400']">
                      <svg v-if="/\d/.test(newPassword)" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </span>
                    Includes numbers
                  </li>
                </ul>
              </div>
            </div>

            <!-- Confirm New Password field -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Confirm New Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <input 
                  v-model="confirmNewPassword" 
                  type="password" 
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-black focus:border-black" 
                  placeholder="Confirm new password" 
                  required 
                />
              </div>
              <div v-if="passwordsMatch === false" class="mt-1 text-sm text-red-600">
                Passwords don't match
              </div>
              <div v-if="passwordsMatch === true" class="mt-1 text-sm text-green-600 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Passwords match
              </div>
            </div>

            <div v-if="errorMessage" class="p-4 rounded-lg bg-red-100 text-red-700 text-sm">
              {{ errorMessage }}
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
                :disabled="isSubmitting || (confirmNewPassword && !passwordsMatch)"
              >
                <span v-if="isSubmitting">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Updating...
                </span>
                <span v-else>Update Password</span>
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
import { validatePassword } from "../utils/validation";

export default {
  data() {
    return {
      currentPassword: '',
      newPassword: '',
      confirmNewPassword: '',
      passwordUpdated: false,
      isSubmitting: false,
      errorMessage: '',
      errors: {
        currentPassword: null,
        newPassword: null
      }
    };
  },
  computed: {
    passwordsMatch() {
      if (!this.confirmNewPassword) return null;
      return this.newPassword === this.confirmNewPassword;
    },
    passwordStrengthPercent() {
      if (!this.newPassword) return 0;
      
      let strength = 0;
      // Length check
      if (this.newPassword.length >= 8) strength += 30;
      // Letter check
      if (/[a-zA-Z]/.test(this.newPassword)) strength += 30;
      // Number check
      if (/\d/.test(this.newPassword)) strength += 30;
      // Special character bonus
      if (/[^a-zA-Z0-9]/.test(this.newPassword)) strength += 10;
      
      return Math.min(strength, 100);
    },
    strengthText() {
      const strength = this.passwordStrengthPercent;
      if (strength < 30) return "Very weak";
      if (strength < 60) return "Weak";
      if (strength < 80) return "Medium";
      return "Strong";
    },
    strengthColor() {
      const strength = this.passwordStrengthPercent;
      if (strength < 30) return "text-red-600";
      if (strength < 60) return "text-orange-500";
      if (strength < 80) return "text-yellow-500";
      return "text-green-600";
    },
    strengthBarColor() {
      const strength = this.passwordStrengthPercent;
      if (strength < 30) return "bg-red-600";
      if (strength < 60) return "bg-orange-500";
      if (strength < 80) return "bg-yellow-500";
      return "bg-green-600";
    }
  },
  created() {
    if (!localStorage.getItem('isAuthenticated')) {
      this.$router.push("/auth/login/");
    }
  },
  methods: {
    async updatePassword() {
      this.errors = {
        currentPassword: null,
        newPassword: null
      };
      this.errorMessage = '';
      
      // Validate new password
      const passwordError = validatePassword(this.newPassword);
      if (passwordError) {
        this.errors.newPassword = passwordError;
        return;
      }
      
      // Check if passwords match
      if (this.newPassword !== this.confirmNewPassword) {
        return;
      }

      this.isSubmitting = true;
      
      try {
        const response = await axios.put("http://127.0.0.1:8000/api/user/update-password/", {
          current_password: this.currentPassword,
          new_password: this.newPassword,
          confirm_new_password: this.confirmNewPassword
        }, {
          withCredentials: true
        });

        if (response.status === 200) {
          this.passwordUpdated = true;
          this.currentPassword = '';
          this.newPassword = '';
          this.confirmNewPassword = '';
          
          // Redirect after a short delay to show success message
          setTimeout(() => {
            this.$router.push("/profile/");
          }, 1500);
        }
      } catch (error) {
        console.error("Password update error:", error);
        if (error.response?.data?.current_password) {
          this.errors.currentPassword = error.response.data.current_password[0];
          this.errorMessage = error.response.data.current_password[0];
        } else if (error.response?.data?.new_password) {
          this.errors.newPassword = error.response.data.new_password[0];
          this.errorMessage = error.response.data.new_password[0];
        } else if (error.response?.data?.confirm_new_password) {
          this.errorMessage = error.response.data.confirm_new_password[0];
        } else if (error.response?.data?.non_field_errors) {
          this.errorMessage = error.response.data.non_field_errors[0];
        } else {
          this.errorMessage = "Failed to update password. Please try again.";
        }
      } finally {
        this.isSubmitting = false;
      }
    }
  }
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