<template>
  <div class="flex items-start pt-20 justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg overflow-hidden">
      <div class="bg-black text-white text-center py-6">
        <h2 class="text-lg font-semibold">Forgot Password</h2>
      </div>
      <div class="p-8">
        <h3 class="text-xl font-medium text-gray-900">Enter Your Email</h3>
        <form @submit.prevent="resetPassword" class="mt-4">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input v-model="email" type="email" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter your email" required />
          </div>
          <button type="submit" class="w-full mt-4 bg-black text-white py-2 rounded-full hover:bg-gray-800">Reset Password</button>
        </form>
        <div class="text-center text-sm text-gray-500 mt-3">
          Already have an account? <a href="/auth/login/" class="text-black font-medium hover:underline">Login now</a>
        </div>
        <div class="text-center text-sm text-gray-500 mt-3">
          Don't have an account? <a href="/auth/register/" class="text-black font-medium hover:underline">Sign up now</a>
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
      email: "",
    };
  },
  methods: {
    async resetPassword() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/auth/forgot-password/", {
          email: this.email
        });
        
        if (response.status === 200) {
          alert("Password reset instructions have been sent to your email.");
          this.$router.push("/auth/login/");
        }
      } catch (error) {
        console.error("Password reset error:", error);
        let errorMessage = "Failed to send reset instructions. ";
        if (error.response?.data?.email) {
          errorMessage += error.response.data.email[0];
        } else {
          errorMessage += "Please try again.";
        }
        alert(errorMessage);
      }
    },
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
