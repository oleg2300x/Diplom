from django.contrib import admin

from cart.models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'created_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'cart', 'labtest', 'quantity', 'price', 'total')
