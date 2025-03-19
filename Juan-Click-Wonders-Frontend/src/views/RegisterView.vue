<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
      <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg overflow-hidden">
        <div class="bg-black text-white text-center py-6">
          <h2 class="text-lg font-semibold">Register</h2>
        </div>
        <div class="p-8">
          <h3 class="text-xl font-medium text-gray-900">Sign Up Now</h3>
          <form @submit.prevent="register" class="mt-4">
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">First Name</label>
              <input v-model="first_name" type="text" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter your first name" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">Last Name</label>
              <input v-model="last_name" type="text" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter your last name" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">Phone Number</label>
              <input v-model="phone_number" type="text" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter your phone number" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">Address</label>
              <input v-model="address" type="text" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter your address" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input v-model="email" type="email" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter your email" required />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">Password</label>
              <input v-model="password1" type="password" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Enter your password" required />
              <p v-if="passwordError" class="mt-1 text-sm text-red-600">{{ passwordError }}</p>
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700">Confirm Password</label>
              <input v-model="password2" type="password" class="mt-1 block w-full px-4 py-2 border rounded-full shadow-sm focus:ring-black focus:border-black" placeholder="Re-enter your password" required />
            </div>
            <button type="submit" class="w-full mt-4 bg-black text-white py-2 rounded-full hover:bg-gray-800">Sign Up</button>
          </form>
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
        passwordError: ""
      };
    },
    methods: {
      async register() {
        // Reset error message
        this.passwordError = "";
        
        // Validate password
        const passwordError = validatePassword(this.password1);
        if (passwordError) {
          this.passwordError = passwordError;
          return;
        }

        if (this.password1 !== this.password2) {
          alert("Passwords do not match!");
          return;
        }
  
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
            alert("Registered successfully!");
            this.$router.push("/auth/login/");
          }
        } catch (error) {
          if (error.response && error.response.status === 400) {
            const errorMessage = error.response.data?.detail || "Registration failed due to invalid input.";
            alert(errorMessage);
          } else {
            console.error("Registration failed:", error);
            alert("An unexpected error occurred. Please try again.");
          }
        }
      }
    }
  };
</script>  


<!-- asd@jcw.com - jcwadmin123
qwe@jcw.com - jcwadmin123
james@gmail.com - jamespogi123
james@jcw.com - admin123 -->