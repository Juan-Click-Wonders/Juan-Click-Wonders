<template>
  <div class="flex items-start pt-20 justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg overflow-hidden">
      <div class="bg-black text-white text-center py-6">
        <h2 class="text-lg font-semibold">Profile</h2>
      </div>
      <div class="p-8">
        <h3 class="text-xl font-medium text-gray-900">Your Information</h3>
        <div class="mt-4">
          <div v-for="(value, label) in user" :key="label" class="mb-4">
            <label class="block text-sm font-medium text-gray-700">{{ label }}:</label>
            <div class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm bg-gray-200 text-gray-700">
              {{ value }}
            </div>
          </div>
        </div>
        <button 
          class="w-full mt-4 bg-black text-white py-2 rounded-full hover:bg-gray-800"
          @click="logout"
        >
          Logout
        </button>
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
  created() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem("access_token");  // Get token from storage
        if (!token) {
          console.error("No token found! Redirecting to login...");
          this.$router.push("/auth/login/"); // Redirect to login if no token
          return;
        }
        console.log("Token used for fetching profile:", token); // Log the token
        const response = await axios.get("http://127.0.0.1:8000/api/profile/", {
          headers: {
            Authorization: `Bearer ${token}`, // Include token in request
          },
        });

        this.user = response.data;
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/auth/login/");
    },
  },
};
</script>
