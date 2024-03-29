from django.contrib import admin
from . import models

# gsm9390061
# user1 qwerty123654
# Register your models here.

# admin.register(model_name)
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.Discount)
admin.site.register(models.Person)
admin.site.register(models.Cart)
admin.site.register(models.Profile)

# admin.site.register(models.WishList)

# 2й вариант
@admin.register(models.WishList)
class WishableListAdmin(admin.ModelAdmin):
    ...

# @admin.register(models.Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'total_amount']
#
#     def total_amount(self, obj):
#         return obj.Product.count()