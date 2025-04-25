from django.contrib import admin
from .models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_order_display',)
    
    def user_order_display(self, obj):
        return f"{obj.user.user.email} - {obj}"
    user_order_display.short_description = 'Order List'

admin.site.register(Order, OrderAdmin)
