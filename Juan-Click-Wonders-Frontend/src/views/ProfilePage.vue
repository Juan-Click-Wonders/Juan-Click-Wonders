<template>
  <div class="bg-gray-100 min-h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <div class="bg-white shadow-2xl rounded-3xl overflow-hidden">
        <!-- Profile Header with Background -->
        <div class="bg-gradient-to-r from-gray-900 to-gray-800 h-40 relative">
          <!-- User Avatar -->
          <div class="absolute -bottom-12 left-8">
            <div class="h-24 w-24 rounded-full bg-yellow-500 flex items-center justify-center border-4 border-white text-gray-900 text-4xl font-bold shadow-lg">
              {{ userInitial }}
            </div>
          </div>
        </div>

        <!-- Profile Content -->
        <div class="pt-16 pb-8 px-8">
          <div class="flex flex-col md:flex-row md:items-start md:justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">{{ user.Name }}</h1>
              <p class="text-gray-600">{{ user.Email }}</p>
            </div>
            <div class="mt-4 md:mt-0 flex flex-wrap gap-2">
              <button @click="editProfile" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gray-800 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Edit Profile
              </button>
              <button @click="changePassword" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gray-800 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
                Change Password
              </button>
            </div>
          </div>

          <!-- User Information Section -->
          <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Contact Information -->
            <div class="bg-gray-50 rounded-xl p-6">
              <h2 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                </svg>
                Contact Information
              </h2>
              <div class="space-y-3">
                <div class="flex items-center">
                  <div class="flex-shrink-0 text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-gray-900">Email</p>
                    <p class="text-sm text-gray-500">{{ user.Email }}</p>
                  </div>
                </div>
                <div class="flex items-center">
                  <div class="flex-shrink-0 text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-gray-900">Phone</p>
                    <p class="text-sm text-gray-500">{{ user.Phone }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Address Information -->
            <div class="bg-gray-50 rounded-xl p-6">
              <h2 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Address
              </h2>
              <div class="text-sm text-gray-500">
                {{ user.Address }}
              </div>
            </div>
          </div>

          <!-- Account Actions -->
          <div class="mt-8 border-t border-gray-200 pt-8">
            <h2 class="text-lg font-medium text-gray-900 mb-4">Account Actions</h2>
            <div class="space-y-3">
              <button 
                @click="logout"
                class="w-full md:w-auto flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Log Out
              </button>
            </div>
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
      user: {
        Email: "Loading...",
        Name: "Loading...",
        Phone: "Loading...",
        Address: "Loading...",
      },
      loading: true
    };
  },
  computed: {
    userInitial() {
      return this.user.Name.charAt(0).toUpperCase();
    }
  },
  async created() {
    if (!localStorage.getItem('isAuthenticated')) {
      this.$router.push('/auth/login/');
      return;
    }

    try {
      const response = await axios.get("http://127.0.0.1:8000/api/profile/", {
        withCredentials: true
      });
      this.user = {
        Email: response.data.email || 'N/A',
        Name: response.data.first_name && response.data.last_name 
          ? `${response.data.first_name} ${response.data.last_name}`
          : 'N/A',
        Phone: response.data.phone_number || 'N/A',
        Address: response.data.address || 'N/A'
      };

      // Save the user's name to localStorage for navbar display
      if (response.data.first_name) {
        localStorage.setItem('userName', response.data.first_name);
        // Update auth state to ensure navbar updates
        window.dispatchEvent(new Event('auth-state-changed'));
      }
      
      this.loading = false;
    } catch (error) {
      console.error("Error fetching profile:", error);
      if (error.response?.status === 401) {
        localStorage.removeItem('isAuthenticated');
        this.$router.push('/auth/login/');
      }
      this.loading = false;
    }
  },
  methods: {
    async logout() {
      try {
        await axios.post("http://127.0.0.1:8000/api/auth/logout/", {}, {
          withCredentials: true
        });
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('cartCount');
        localStorage.removeItem('userName');
        window.dispatchEvent(new Event('cart-updated'));
        window.dispatchEvent(new Event('auth-state-changed'));
        this.$router.push("/auth/login/");
      } catch (error) {
        console.error("Logout error:", error);
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('cartCount');
        localStorage.removeItem('userName');
        window.dispatchEvent(new Event('cart-updated'));
        window.dispatchEvent(new Event('auth-state-changed'));
        this.$router.push("/auth/login/");
      }
    },
    editProfile() {
      this.$router.push("/profile/edit");
    },
    changePassword() {
      this.$router.push("/profile/password");
    }
  }
};
</script>

<style scoped>
/* Any additional profile-specific styles */
</style>
