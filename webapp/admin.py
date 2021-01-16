from django.contrib import admin

# Register your models here.
from .models import Item
from .models import Cart
from .models import Cart_Product

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Cart_Product)
