<template>
  <div class="flex items-start pt-20 justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg overflow-hidden">
      <div class="bg-black text-white text-center py-6">
        <h2 class="text-lg font-semibold">Profile</h2>
      </div>
      <div class="p-8">
        <h3 class="text-xl font-medium text-gray-900">Welcome, {{ user.Name }}</h3>
        <div class="mt-4 space-y-2 -ml-4">
          <div v-for="(value, label) in user" :key="label" class="flex items-center">
            <label class="text-sm font-medium text-gray-700 min-w-[70px] mr-3 text-right">{{ label }}:</label>
            <div class="flex-1 px-4 py-1.5 border rounded-full shadow-sm bg-gray-200 text-gray-700 truncate">
              {{ value }}
            </div>
          </div>
        </div>
        <div class="flex space-x-2 mt-6">
          <button 
            class="flex-1 bg-black text-white py-2 rounded-full hover:bg-gray-800 text-sm"
            @click="editProfile"
          >
            Edit Profile
          </button>
          <button 
            class="flex-1 bg-black text-white py-2 rounded-full hover:bg-gray-800 text-sm"
            @click="changePassword"
          >
            Change Password
          </button>
          <button 
            class="flex-1 bg-black text-white py-2 rounded-full hover:bg-gray-800 text-sm"
            @click="logout"
          >
            Logout
          </button>
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
      }
    };
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
    } catch (error) {
      console.error("Error fetching profile:", error);
      if (error.response?.status === 401) {
        localStorage.removeItem('isAuthenticated');
        this.$router.push('/auth/login/');
      }
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
        window.dispatchEvent(new Event('cart-updated'));
        window.dispatchEvent(new Event('auth-state-changed'));
        this.$router.push("/auth/login/");
      } catch (error) {
        console.error("Logout error:", error);
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('cartCount');
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
