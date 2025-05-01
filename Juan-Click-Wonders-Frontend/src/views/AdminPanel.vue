<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="!isAdmin" class="text-center py-12">
      <h1 class="text-2xl font-bold text-red-600">Access Denied</h1>
      <p class="mt-4 text-gray-600">You don't have permission to access this page.</p>
      <router-link to="/"
        class="mt-6 inline-block bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-medium py-2 px-4 rounded-lg transition-colors">
        Return to Home
      </router-link>
    </div>

    <div v-else>
      <h1 class="text-3xl font-bold mb-8 text-center">Admin Panel</h1>

      <!-- Tab Navigation -->
      <div class="border-b border-gray-200 mb-6">
        <nav class="flex -mb-px">
          <button @click="activeTab = 'orders'" :class="[
            'py-4 px-6 font-medium text-sm',
            activeTab === 'orders'
              ? 'border-b-2 border-yellow-500 text-yellow-600'
              : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]">
            Orders Management
          </button>
        </nav>
      </div>

      <!-- Orders Tab Content -->
      <div v-if="activeTab === 'orders'" class="bg-white rounded-lg shadow p-6">
        <div class="flex flex-col md:flex-row justify-between items-center mb-6">
          <h2 class="text-xl font-semibold mb-4 md:mb-0">All Orders</h2>

          <!-- Filter by User -->
          <div class="w-full md:w-1/3">
            <div class="relative">
              <input type="text" v-model="userFilter" @input="filterOrders" placeholder="Filter by user email"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500" />
              <button v-if="userFilter" @click="clearFilter"
                class="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="flex justify-center items-center py-12">
          <svg class="animate-spin h-8 w-8 text-yellow-500" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
          </svg>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Orders Table -->
        <div v-else-if="orders.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order ID</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="order in orders" :key="order.order_id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{{ order.order_id }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ getUserEmail(order) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ order.product.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ order.quantity }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusClass(order.status)"
                    class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                    {{ order.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <select v-model="order.statusCode" @change="updateOrderStatus(order)"
                    class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 sm:text-sm rounded-md">
                    <option value="P">Paid</option>
                    <option value="S">To Ship</option>
                    <option value="R">To Receive</option>
                    <option value="D">Delivered</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- No Orders State -->
        <div v-else class="text-center py-12">
          <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-gray-400" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No orders found</h3>
          <p class="mt-1 text-sm text-gray-500">
            {{ userFilter ? 'No orders match your filter criteria.' : 'There are no orders in the system yet.' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  withCredentials: true
});

export default {
  name: 'AdminPanel',
  data() {
    return {
      isAdmin: false,
      isLoading: true,
      error: null,
      activeTab: 'orders',
      orders: [],
      userFilter: '',
      users: [],
      statusMap: {
        'P': 'Paid',
        'S': 'To Ship',
        'R': 'To Receive',
        'D': 'Delivered'
      }
    };
  },
  methods: {
    async checkAdminStatus() {
      try {
        const response = await api.get('/admins/check/');
        const data = response.data;
        this.isAdmin = data.is_admin;

        // Log admin status details
        console.log('Admin Panel - Admin status check:', {
          is_admin: data.is_admin,
          is_staff: data.is_staff,
          is_superuser: data.is_superuser
        });

        return this.isAdmin;
      } catch (error) {
        console.error('Error checking admin status:', error);
        this.isAdmin = false;
        return false;
      }
    },
    async fetchOrders() {
      this.isLoading = true;
      this.error = null;

      try {
        const url = this.userFilter
          ? `/admins/orders/?user_email=${encodeURIComponent(this.userFilter)}`
          : '/admins/orders/';

        const response = await api.get(url);
        this.orders = response.data.map(order => ({
          ...order,
          statusCode: this.getStatusCode(order.status)
        }));
      } catch (error) {
        console.error('Error fetching orders:', error);
        this.handleApiError(error);
      } finally {
        this.isLoading = false;
      }
    },
    async fetchUsers() {
      try {
        const response = await api.get('/admins/users/');
        this.users = response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    async updateOrderStatus(order) {
      this.error = null;

      try {
        await api.put(`/orders/${order.order_id}/status/`, {
          status: order.statusCode
        });

        // Update the displayed status
        order.status = this.statusMap[order.statusCode];
      } catch (error) {
        console.error('Error updating order status:', error);
        this.handleApiError(error);
        // Revert the status in the UI
        await this.fetchOrders();
      }
    },
    filterOrders() {
      this.fetchOrders();
    },
    clearFilter() {
      this.userFilter = '';
      this.fetchOrders();
    },
    getStatusCode(statusText) {
      // Convert status text back to code
      for (const [code, text] of Object.entries(this.statusMap)) {
        if (text === statusText) return code;
      }
      return 'P'; // Default to Paid
    },
    getStatusClass(status) {
      switch (status) {
        case 'Paid':
          return 'bg-green-100 text-green-800';
        case 'To Ship':
          return 'bg-blue-100 text-blue-800';
        case 'To Receive':
          return 'bg-yellow-100 text-yellow-800';
        case 'Delivered':
          return 'bg-purple-100 text-purple-800';
        default:
          return 'bg-gray-100 text-gray-800';
      }
    },
    getUserEmail(order) {
      // Use the user_email field from the serializer
      return order.user_email || 'Unknown User';
    },
    handleApiError(error) {
      if (error.response) {
        if (error.response.status === 401) {
          this.error = 'Your session has expired. Please log in again.';
          this.$router.push('/auth/login');
        } else if (error.response.status === 403) {
          this.error = 'You do not have permission to perform this action.';
        } else {
          this.error = error.response.data.error || 'An error occurred while processing your request.';
        }
      } else {
        this.error = 'Unable to connect to the server. Please try again later.';
      }
    }
  },
  async created() {
    const isAdmin = await this.checkAdminStatus();
    if (isAdmin) {
      await this.fetchOrders();
      await this.fetchUsers();
    }
  }
};
</script>
