<template>
    <div class="auth-container">
      <h2>Reset Password</h2>
      <form @submit.prevent="resetPassword">
        <input v-model="new_password" type="password" placeholder="New Password" required />
        <input v-model="confirm_new_password" type="password" placeholder="Confirm Password" required />
        <button type="submit">Reset Password</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        new_password: "",
        confirm_new_password: "",
        uidb64: this.$route.query.uidb64,
        token: this.$route.query.token,
      };
    },
    methods: {
      async resetPassword() {
        try {
          await axios.post("http://127.0.0.1:8000/auth/reset-password/", {
            uidb64: this.uidb64,
            token: this.token,
            new_password: this.new_password,
            confirm_new_password: this.confirm_new_password,
          });
          alert("Password reset successful. You can log in now.");
          this.$router.push("/auth/login");
        } catch (error) {
          alert("Error resetting password.");
        }
      },
    },
  };
  </script>