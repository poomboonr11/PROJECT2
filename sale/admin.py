from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Customer
from .models import Sale
from .models import SaleLineItem

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Sale)
admin.site.register(SaleLineItem)