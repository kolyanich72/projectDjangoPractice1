import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')  #

django.setup()
from store.models import Category, Product

if __name__ == '__main__':
    #вариант1
    category = Category.objects.get(name='Vegitables')
    obj = Product(name= 'onion', description='red onion', price=45, image='static/products/product-9.jpg', category=category)
    obj.save()
    obj = Product(name='garlic', description='garlic', price=45, image='static/products/product-11.jpg',
                  category=category)
    obj.save()
    obj = Product(name='chili pepper', description='hot chili pepper', price=150, image='static/products/product-12.jpg',
                  category=category)
    obj.save()

    # вариант2
    obj = Product.objects.create(name='Fruit Juice', description='Fruit Juice', price=45,
                  image='static/products/product-8.jpg',
                  category=Category.objects.get(name='Juice'))
    # вариант3
    data =     ({'name': 'Apple',
                 'description': 'Apple',
                 'price': 120.00,
                 'category': 'Fruits',
                 'image': 'static/products/product-10.jpg'},
                {'name': 'Green Chilli',
                 'description': 'green Chilli',
                 'price': 120.00,
                 'category': 'Vegitables',
                 'image': 'static/products/product-12.jpg'})

    categ = {'Fruits': Category.objects.get(name='Fruits'),
             'Vegitables': Category.objects.get(name='Vegitables')}
    object_to_create = [Product(name=val['name'], description=val['description'],
                                price=val['price'], image=val['image'],
                                category=categ[val['category']]) for val in data]

    Product.objects.bulk_create(object_to_create)

