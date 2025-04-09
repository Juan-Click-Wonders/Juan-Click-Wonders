<template>
    <div class="flex items-start pt-20 justify-center min-h-screen bg-gray-100">
      <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg overflow-hidden">
        <div class="bg-black text-white text-center py-6">
          <h2 class="text-lg font-semibold">Edit Profile</h2>
        </div>
        <div class="p-8">
          <form @submit.prevent="updateProfile" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Phone Number</label>
              <input type="text" v-model="phoneNumber" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Address</label>
              <input type="text" v-model="address" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input type="email" v-model="email" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Enter Current Password</label>
              <input type="password" v-model="currentPassword" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" required />
            </div>
            <div v-if="message" class="mb-4 p-4 rounded-lg bg-red-100 text-red-700 text-sm">
              {{ message }}
            </div>
            <button type="submit" class="w-full mt-4 bg-black text-white py-2 rounded-full hover:bg-gray-800">
              Confirm Changes
            </button>
          </form>
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
        message: null
      };
    },
    async created() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/profile/", {
          withCredentials: true
        });
        
        const profile = response.data;
        this.phoneNumber = profile.phone_number;
        this.address = profile.address;
        this.email = profile.email;
      } catch (error) {
        console.error("Error loading profile:", error);
        if (error.response?.status === 401) {
          this.$router.push("/auth/login/");
        }
      }
    },
    methods: {
      async updateProfile() {
        try {
          const response = await axios.put("http://127.0.0.1:8000/api/profile/update/", {
            phone_number: this.phoneNumber,
            address: this.address,
            email: this.email,
            current_password: this.currentPassword
          }, {
            withCredentials: true
          });

          this.$router.push("/profile/");
        } catch (error) {
          console.error("Profile update error:", error);
          if (error.response?.data?.current_password) {
            this.message = "Please check your password";
          } else if (error.response?.data?.email) {
            this.message = "Please check your email";
          } else {
            this.message = "Failed to update profile. Check your details.";
          }
        }
      }
    }
  };
  </script>
  
  <style scoped>
  input:focus {
    outline: none;
    border-color: black;
    box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.2);
  }
  </style>
  