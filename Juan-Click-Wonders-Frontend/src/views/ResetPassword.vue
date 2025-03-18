<template>
  <div class="flex items-start pt-20 justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg overflow-hidden">
      <div class="bg-black text-white text-center py-6">
        <h2 class="text-lg font-semibold">Reset Password</h2>
      </div>
      <div class="p-8">
        <h3 class="text-xl font-medium text-gray-900">Enter New Password</h3>
        <form @submit.prevent="resetPassword" class="mt-4">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">New Password</label>
            <input v-model="new_password" type="password" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter new password" required />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Confirm New Password</label>
            <input v-model="confirm_new_password" type="password" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Confirm new password" required />
          </div>
          <button type="submit" class="w-full mt-4 bg-black text-white py-2 rounded-full hover:bg-gray-800">Reset Password</button>
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
      new_password: "",
      confirm_new_password: "",
      uidb64: this.$route.params.uidb64,
      token: this.$route.params.token,
    };
  },
  methods: {
    async resetPassword() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/auth/reset-password/", {
          uidb64: this.uidb64,
          token: this.token,
          new_password: this.new_password,
          confirm_new_password: this.confirm_new_password,
        });

        if (response.status === 200) {
          alert("Password has been reset successfully!");
          this.$router.push("/auth/login/");
        }
      } catch (error) {
        console.error("Password reset error:", error);
        let errorMessage = "Failed to reset password. ";
        if (error.response?.data?.new_password) {
          errorMessage += error.response.data.new_password[0];
        } else if (error.response?.data?.token) {
          errorMessage += error.response.data.token[0];
        } else {
          errorMessage += "Please try again.";
        }
        alert(errorMessage);
      }
    },
  },
  created() {
    if (!this.uidb64 || !this.token) {
      alert("Invalid password reset link.");
      this.$router.push("/auth/login/");
    }
  },
};
</script>

<style scoped>
input:focus {
  outline: none;
  border-color: black;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.2);
}
</style>