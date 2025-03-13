<template>
    <div>
        <header class="bg-gray-900 text-white">
            <div class="w-full px-4">
                <div class="flex items-center justify-between">
                    <div class="!h-full !py-2 !mx-25">
                        <a href="/">
                            <img src="/icon.png" alt="Logo" class="!h-16 !w-16 object-contain">
                        </a>
                    </div>
                    <div class="flex-1 max-w-7xl mx-4 relative flex items-center">
                        <div class="w-full relative">
                            <input type="text" placeholder="Search Products"
                                v-model="searchQuery"
                                @keyup.enter="handleSearch"
                                class="w-full !py-3 !pl-5 !pr-12 bg-white rounded-full text-gray-800 focus:outline-none" />
                            <button class="absolute right-0 top-0 h-full !px-4 flex items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                </svg>
                            </button>
                        </div>
                        <div class="!ml-4">
                            <a href="#" class="flex items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                                </svg>
                            </a>
                        </div>
                    </div>
                    <div>
                        <a href="#" class="font-medium hover:text-gray-300 !mx-25">LOGIN</a>
                    </div>
                </div>
                <nav class="flex justify-end !py-2 !mx-25">
                    <div class="flex !space-x-8 font-medium">
                        <a href="/" class="hover:text-gray-300">HOME</a>
                        <a href="/product_list" class="hover:text-gray-300">SHOP</a>
                        <a href="/about" class="hover:text-gray-300">ABOUT</a>
                    </div>
                </nav>
            </div>
        </header>
    </div>
</template>

<script>
export default {
    data() {
        return {
            searchQuery: '',
        }
    },
    methods: {
        handleSearch() {
            // If search is empty or only whitespace, remove search parameter
            if (!this.searchQuery || !this.searchQuery.trim()) {
                this.$router.push({
                    path: '/product_list'
                });
            } else {
                this.$router.push({
                    path: '/product_list',
                    query: { search: this.searchQuery.trim() }
                });
            }
        }
    }
}
</script>

<style scoped>
</style>