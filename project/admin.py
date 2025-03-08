from django.contrib import admin
from .models import Fruits, Cart, CartItem
# Register your models here.
admin.site.register(Fruits)
admin.site.register(Cart)
admin.site.register(CartItem)
