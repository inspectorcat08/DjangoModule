from django.contrib import admin
from .models import MyUser
from .models import Product, Purchase, Return

admin.site.register(MyUser)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Return)