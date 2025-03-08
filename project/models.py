from django.db import models
from django.contrib.auth.models import User

class Fruits(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=400, default='')
    image = models.ImageField(upload_to='media/fruit/') 
    stock = models.PositiveIntegerField(null=True, blank=True)

    @staticmethod
    def get_all_product():
        return Fruits.objects.all()

    def get_stock_status(self):
        if self.stock is None or self.stock == 0:
            return "Out of Stock"
        elif self.stock < 20:
            return "Limited Stock"
        else:
            return "In Stock"

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Fruits, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"
