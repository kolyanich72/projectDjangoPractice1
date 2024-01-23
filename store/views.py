from django.shortcuts import render
from django.views import View
#import datetime
from datetime import datetime
from  django.http import HttpResponse
from django.db.models import Subquery, OuterRef, F,ExpressionWrapper, DecimalField, Case, When
from  django.utils import timezone
from  .models import Product, Category, Discount
from .serializers import CartSerializer



class ShopView(View):
    def get(self, request):
        discount_value = Case(When(discount__value__gte=0, discount__date_begin__lte=timezone.now(),
                              discount__date_end__gte=timezone.now(),then=F('discount__value')),
                              default=0, output_field=DecimalField(max_digits=10, decimal_places=2))
        price_with_discnt = ExpressionWrapper(
            (F('price') * (100.0-F('discount_value'))/100),
            output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        products = Product.objects.annotate(discount_value=discount_value, price_before=F('price'),
            price_after=price_with_discnt).values('id', 'name', 'image', 'price_before', 'price_after', 'discount_value')

        return render(request, 'store/shop.html',{'data':products})


        # context = {'data': [{'name': 'Bell Pepper',
        #                      'discount': 30,
        #                      'price_main': 120.00,
        #                      'price_discount': 80.00,
        #                      'id': 1,
        #                      'url': 'store/images/product-1.jpg'},
        #                     {'name': 'Strawberry',
        #                      'discount': None,
        #                      'price_main': 120.00,
        #                      'id': 2,
        #                      'url': 'store/images/product-2.jpg'},
        #                     {'name': 'Green Beans',
        #                      'discount': None,
        #                      'price_main': 120.00,
        #                      'id': 3,
        #                      'url': 'store/images/product-3.jpg'},
        #                     {'name': 'Purple Cabbage',
        #                      'discount': None,
        #                      'price_main': 120.00,
        #                      'id': 4,
        #                      'url': 'store/images/product-4.jpg'},
        #                     {'name': 'Tomatoe',
        #                      'discount': 30,
        #                      'price_main': 120.00,
        #                      'price_discount': 80.00,
        #                      'id': 5,
        #                      'url': 'store/images/product-5.jpg'},
        #                     {'name': 'Brocolli',
        #                      'discount': None,
        #                      'price_main': 120.00,
        #                      'id': 6,
        #                      'url': 'store/images/product-6.jpg'},
        #                     {'name': 'Carrots',
        #                      'discount': None,
        #                      'price_main': 120.00,
        #                      'id': 7,
        #                      'url': 'store/images/product-7.jpg'},
        #                     {'name': 'Fruit Juice',
        #                      'discount': None,
        #                      'price_main': 120.00,
        #                      'id': 8,
        #                      'url': 'store/images/product-8.jpg'},
        #                     {'name': 'Onion',
        #                      'discount': 30,
        #                      'price_main': 120.00,
        #                      'price_discount': 80.00,
        #                      'id': 9,
        #                      'url': 'store/images/product-9.jpg'},
        #                     {'name': 'Apple',
        #                      'discount': None,
        #                      'price_main': 120.00,
        #                      'id': 10,
        #                      'url': 'store/images/product-10.jpg'},
        #                     {'name': 'Garlic',
        #                      'discount': None,
        #                      'price_main': 120.00,
        #                      'id': 11,
        #                      'url': 'store/images/product-11.jpg'},
        #                     {'name': 'Chilli',
        #                      'discount': None,
        #                      'price_main': 120.00,
        #                      'id': 12,
        #                      'url': 'store/images/product-12.jpg'},
        #                     ]
        #            }
        # return render(request, 'store/shop.html', context)

class ProductSingleView(View):
    def get(self, request, id):
        data = Product.objects.get(id=id)
        return render(request, 'store/product-single.html',
                      context={'name':data.name, 'description':data.description,
                               'price': data.price, 'rating': 5.0,
                               'url': data.image.url,                       })
        # data = {1: {'name': 'Bell Pepper',
        #             'description': 'Bell Pepper',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-1.jpg'},
        #         2: {'name': 'Strawberry',
        #             'description': 'Strawberry',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-2.jpg'},
        #         3: {'name': 'Green Beans',
        #             'description': 'Green Beans',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-3.jpg'},
        #         4: {'name': 'Purple Cabbage',
        #             'description': 'Purple Cabbage',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-4.jpg'},
        #         5: {'name': 'Tomatoe',
        #             'description': 'Tomatoe',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-5.jpg'},
        #         6: {'name': 'Brocolli',
        #             'description': 'Brocolli',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-6.jpg'},
        #         7: {'name': 'Carrots',
        #             'description': 'Carrots',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-7.jpg'},
        #         8: {'name': 'Fruit Juice',
        #             'description': 'Fruit Juice',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-8.jpg'},
        #         9: {'name': 'Onion',
        #             'description': 'Onion',
        #             'price': 120.00,
        #             'rating': 5.0,
        #             'url': 'store/images/product-9.jpg'},
        #         10: {'name': 'Apple',
        #              'description': 'Apple',
        #              'price': 120.00,
        #              'rating': 5.0,
        #              'url': 'store/images/product-10.jpg'},
        #         11: {'name': 'Garlic',
        #              'description': 'Garlic',
        #              'price': 120.00,
        #              'rating': 5.0,
        #              'url': 'store/images/product-11.jpg'},
        #         12: {'name': 'Chilli',
        #              'description': 'Chilli',
        #              'price': 120.00,
        #              'rating': 5.0,
        #              'url': 'store/images/product-12.jpg'}
        #         }
        # return render(request, 'store/product-single.html', context=data[id])
