<template>
    <div class="flex items-start pt-20 justify-center min-h-screen bg-gray-100">
      <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg overflow-hidden">
        <div class="bg-black text-white text-center py-6">
          <h2 class="text-lg font-semibold">Update Password</h2>
        </div>
        <div class="p-8">
          <h3 class="text-xl font-medium text-gray-900">Change Your Password</h3>
          <form @submit.prevent="updatePassword" class="mt-4">
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">Current Password</label>
              <input v-model="currentPassword" type="password" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter current password" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">New Password</label>
              <input v-model="newPassword" type="password" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter new password" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">Confirm New Password</label>
              <input v-model="confirmNewPassword" type="password" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Confirm new password" required />
            </div>
            <button type="submit" class="w-full mt-4 bg-black text-white py-2 rounded-full hover:bg-gray-800">Confirm Changes</button>
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
        currentPassword: '',
        newPassword: '',
        confirmNewPassword: ''
      };
    },
    methods: {
      async updatePassword() {
        try {
          const response = await axios.put("http://127.0.0.1:8000/api/user/update-password/", {
            current_password: this.currentPassword,
            new_password: this.newPassword,
            confirm_new_password: this.confirmNewPassword
          }, {
            withCredentials: true
          });

          if (response.status === 200) {
            alert("Password updated successfully!");
            this.$router.push("/profile/");
          }
        } catch (error) {
          console.error("Password update error:", error);
          let errorMessage = "Failed to update password. ";
          if (error.response?.data?.current_password) {
            errorMessage += error.response.data.current_password[0];
          } else if (error.response?.data?.new_password) {
            errorMessage += error.response.data.new_password[0];
          } else {
            errorMessage += "Please try again.";
          }
          alert(errorMessage);
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