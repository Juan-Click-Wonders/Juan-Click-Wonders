<script setup>
import NavBar from "./components/NavBar.vue";
</script>

<template>
  <NavBar />
  <div class="flex-grow">
    <RouterView />
  </div>
  <footer class="bg-gray-900 text-white py-6 w-full mt-auto">
    <div class="container mx-auto text-center sticky top-[100vh]">
      <p>© 2025 Your Website. All rights reserved.</p>
    </div>
  </footer>
</template>