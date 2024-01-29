from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator




class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   address = models.CharField(max_length=100, null=True, blank=True)


   phone_regex = RegexValidator(
       regex=r'^\+79\d{9}$',
       message="Phone number must be entered in the format: '+79123456789'."
   )
   phone_number = models.CharField(validators=[phone_regex],
                                   max_length=12,
                                   blank=True,
                                   null=True,
                                   unique=True,
                                   help_text="Формат +79123456789",
                                   )  # максимальная длина 12 символов


   def __str__(self):
       return f"{self.user}"




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
   if created:
       Profile.objects.create(user=instance)



# Create your models here.

class Person(models.Model):
    short_name = models.CharField(max_length=30, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    reg_data = models.DateTimeField(auto_now_add=True, null=True)  # ,  default='')
    last_visit_data = models.DateTimeField(auto_now=True, null=True)
    contact_mail_field_data = models.EmailField(null=True)

    def __str__(self):
        return self.short_name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/products', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    uploated_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.IntegerField()
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return f'{self.product.name}_{self.value}%_{self.date_end}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user} selected to cart- {self.product} price -{self.quantity}'


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user} selected to wish- {self.product} price -{self.product.price}'
