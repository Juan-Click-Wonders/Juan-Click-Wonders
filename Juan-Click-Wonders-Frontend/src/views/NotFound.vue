<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center justify-center px-4 py-12">
    <div class="max-w-lg w-full bg-white rounded-2xl shadow-xl overflow-hidden">
      <div class="bg-gradient-to-r from-gray-900 to-gray-800 p-6">
        <h2 class="text-2xl font-bold text-white text-center">Page Not Found</h2>
      </div>
      
      <div class="p-8">
        <div class="text-center">
          <div class="flex justify-center mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          
          <h3 class="text-3xl font-bold text-gray-800 mb-2">404</h3>
          <p class="text-xl text-gray-700 mb-6">Oops! The page you're looking for doesn't exist.</p>
          
          <p class="text-gray-600 mb-8" v-if="isAdmin">
            As an admin user, you don't have access to customer-facing pages. 
            Please use the admin panel to manage the system.
          </p>
          <p class="text-gray-600 mb-8" v-else>
            The page you are trying to access might have been removed, had its name changed, 
            or is temporarily unavailable.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link to="/" class="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold px-6 py-3 rounded-lg transition-colors duration-200 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7m-7-7v14" />
              </svg>
              Go to Homepage
            </router-link>
            
            <router-link v-if="!isAdmin" to="/product_list" class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold px-6 py-3 rounded-lg transition-colors duration-200 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              Browse Products
            </router-link>
            
            <router-link v-if="isAdmin" to="/admin" class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold px-6 py-3 rounded-lg transition-colors duration-200 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Go to Admin Panel
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  data() {
    return {
      isAdmin: false
    }
  },
  async created() {
    // Check if user is authenticated
    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
    
    if (isAuthenticated) {
      // Check if the user is an admin
      try {
        const response = await fetch('http://127.0.0.1:8000/admins/check/', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          this.isAdmin = data.is_admin;
        }
      } catch (error) {
        console.error('Error checking admin status:', error);
      }
    }
  }
}
</script>

<style scoped>
.transition-colors {
  transition: all 0.3s ease;
}
</style>