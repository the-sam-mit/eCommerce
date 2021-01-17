from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Item(models.Model):
	item_name = models.CharField(max_length=200)
	item_price = models.FloatField(default = 0.0)	
	item_desc = models.CharField(max_length=500, default='Best deal offered')	
	item_category = models.CharField(max_length=100, default='others')	
	item_image = models.ImageField(upload_to = 'upload/', null=True, blank=True)
	def __str__(self):
		return self.item_name

class Cart(models.Model):
	cart_user = models.ForeignKey(User, on_delete=models.CASCADE)
	cart_total = models.FloatField(default = 0.0)
	def __str__(self):
		return self.cart_user.username

class Cart_Product(models.Model):
	cart_present = models.ForeignKey(Cart, on_delete=models.CASCADE)
	cart_product = models.ForeignKey(Item, on_delete=models.CASCADE)
	cart_subtotal = models.FloatField(default = 0.0)
	cart_quantity = models.IntegerField(default = 0)
	def __str__(self):
		return self.cart_product.item_name
