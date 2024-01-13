from django.contrib import admin
from .models import Category, Product, Discount
#gsm9390061
#user1 qwerty123654
# Register your models here.

#admin.register(model_name)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Discount)
