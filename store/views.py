from django.shortcuts import render, redirect
from django.views import View
# import datetime
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Subquery, OuterRef, F, ExpressionWrapper, DecimalField, Case, When
from django.utils import timezone
# from  .models import Product, Category, Discount, Cart
from .serializers import CartSerializer, WishlistSerializer
import store.models as models
from rest_framework import viewsets, response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class ShopView(View):
    def get(self, request):
        print(request, "   SHOP reqest")
        discount_value = Case(When(discount__value__gte=0, discount__date_begin__lte=timezone.now(),
                                   discount__date_end__gte=timezone.now(), then=F('discount__value')),
                              default=0, output_field=DecimalField(max_digits=10, decimal_places=2))
        price_with_discnt = ExpressionWrapper(
            (F('price') * (100.0 - F('discount_value')) / 100),

            output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        products = models.Product.objects.annotate(discount_value=discount_value, price_before=F('price'),
                                                   price_after=price_with_discnt).values('id', 'name', 'image',
                                                                                         'price_before', 'price_after',
                                                                                         'discount_value')

        return render(request, 'store/shop.html', {'data': products})


class ProductSingleView(View):
    def get(self, request, id):
        data = models.Product.objects.get(id=id)
        return render(request, 'store/product-single.html',
                      context={'name': data.name, 'description': data.description,
                               'price': data.price, 'rating': 5.0,
                               'url': data.image.url, })


class CartViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        ## Можно записать так, для получения товара (проверка что он уже есть в корзине)
        # cart_items = Cart.objects.filter(user=request.user,
        #  product__id = request.data.get('product'))
        # Или можно так, так как мы переопределили метод get_queryset
        cart_items = self.get_queryset().filter(product__id=request.data.get('product'))

        # request API передаёт параметры по названиям полей в БД, поэтому ловим product
        if cart_items:  # Если продукт уже есть в корзине
            cart_item = cart_items[0]
            if request.data.get('quantity'):  # Если в запросе передан параметр quantity,
                # то добавляем значение к значению в БД
                cart_item.quantity += int(request.data.get('quantity'))
            else:  # Иначе просто добавляем значение по умолчению 1
                cart_item.quantity += 1

        else:  # Если продукта ещё нет в корзине
            product = get_object_or_404(models.Product, id=request.data.get('product'))
            # Получаем продукт и проверяем что он вообще существует, если его нет,то выйдет ошибка 404
            if request.data.get('quantity'):  # Если передаём точное количество продукта,то передаём его
                cart_item = models.Cart(user=request.user, product=product, quantity=request.data.get('quantity'))
            else:  # Иначе создаём объект по умолчанию (quantity по умолчанию =  1, так прописали в моделях)
                cart_item = models.Cart(user=request.user, product=product)
        cart_item.save()  # Сохранили объект в БД
        return response.Response({'message': 'Product added to cart'})  # Вернули ответ, что всё прошло успешно

    def update(self, request, *args, **kwargs):
        # Для удобства в kwargs передаётся id строки для изменения в БД, под параметром pk
        cart_item = get_object_or_404(models.Cart, id=kwargs['pk'])
        if request.data.get('quantity'):
            cart_item.quantity = request.data['quantity']
        if request.data.get('product'):
            product = get_object_or_404(models.Product, id=request.data['product'])
        cart_item.product = product
        cart_item.save()
        return response.Response({'message': 'Product change to cart'}, status=201)

    def destroy(self, request, *args, **kwargs):
        # В этот раз напишем примерно так как это делает фреймфорк самостоятельно
        cart_item = self.get_queryset().get(id=kwargs['pk'])
        cart_item.delete()
        return response.Response({'message': 'Product delete from cart'}, status=201)


class CartView(View):

    def get(self, request, ):
        discount_value = Case(When(discount__value__gte=0, discount__date_begin__lte=timezone.now(),
                                   discount__date_end__gte=timezone.now(), then=F('discount__value')),
                              default=0, output_field=DecimalField(max_digits=10, decimal_places=2))

        price_with_discnt = ExpressionWrapper(
            (F('price') * (100.0 - F('discount_value')) / 100),

            output_field=DecimalField(max_digits=10, decimal_places=2)
            )

        products = models.Product.objects.annotate(discount_value=discount_value, price_before=F('price'),
                                                   price_after=price_with_discnt).values(
            'id', 'name', 'image', 'price_before', 'price_after', 'discount_value', 'description'
            )
        prod_cart = models.Cart.objects.all().filter(user=self.request.user)
        d1 = []
        for i in prod_cart:
            d1.append(i.product_id)

        return render(request, 'store/cart.html', {'data': products.filter(id__in=d1)})


class CartViewAddToList(View):

    def get(self,  request, action_do, id, quantity):
        print(request, '    from shop',  id)
        if not request.user.is_authenticated:
            # код который необходим для обработчика
            # return render(request, "store/wishlist.html")
            # Иначе отправляет авторизироваться
            return redirect('login:login')  # from django.shortcuts import redirect
        cartlist_data = models.Cart.objects.all()
        id_list = []

        for i in cartlist_data:
            print(i, '\n', i.id, '\n')

            id_list.append(i.product_id)
            print(id_list, "  +  ", end='')

        print(id_list)

        if action_do != 'buy_now' and action_do != 'add_to_cart':

            models.Cart.objects.filter(product_id=id).delete()
            if len(id_list) > 1:
                return redirect('store:cart')
            else:
                return redirect('store:shop')

        if id not in id_list:
            obj = models.Product.objects.get(id=id)
            obj_todo = models.Cart(user=request.user, product=obj, quantity=quantity)
            obj_todo.save()

        if action_do == 'add_to_cart':
            return redirect ('store:shop')
        else:
            return redirect('store:cart')


class WishlistView(View):

    def get(self, request, id=None):

        if not request.user.is_authenticated:
            # код который необходим для обработчика
            # return render(request, "store/wishlist.html")
            # Иначе отправляет авторизироваться
            return redirect('login:login')  # from django.shortcuts import redirect
        # wishlist_data = models.WishList.objects.all()
        # id_list = []
        #
        # for i in wishlist_data:
        #     print(id_list,"  +  ",  end='')
        #     id_list.append(i.product_id)
        #
        #     print(i.id)
        # print(id_list)
        #
        # if id not in id_list:
        #     obj = models.Product.objects.get(id=id)
        #     print(obj)
        #     # if wishlist_data.filter(id=id):
        #     #     print("da   ", wishlist_data.all().filter(id=id))
        #        # wishlist_data.filter(id=id)
        #        #  obj_todo = models.WishList.objects.filter(id=id).delete()
        #        #  obj_todo.save()
        #     # else:
        #     obj_todo = models.WishList(user=request.user, product=obj)
        #     obj_todo.save()
        #     print("create   ", obj_todo)
        # else:
        #     obj_todo =  models.WishList.objects.filter(product_id=id).delete()
        #     print(obj_todo, " DELETE TODO")
        #
        #

        discount_value = Case(When(discount__value__gte=0, discount__date_begin__lte=timezone.now(),
                                   discount__date_end__gte=timezone.now(), then=F('discount__value')),
                              default=0, output_field=DecimalField(max_digits=10, decimal_places=2))

        price_with_discnt = ExpressionWrapper(
            (F('price') * (100.0 - F('discount_value')) / 100),
            output_field=DecimalField(max_digits=10, decimal_places=2)
            )

        products = models.Product.objects.annotate(discount_value=discount_value, price_before=F('price'),
                                                   price_after=price_with_discnt).values(
            'id', 'name', 'image', 'price_before', 'price_after', 'discount_value', 'description'
            )
        prod_cart = models.WishList.objects.all().filter(user=self.request.user)
        d1 = []
        for i in prod_cart:
            d1.append(i.product_id)

        return render(request, 'store/wishlist.html', {'data': products.filter(id__in=d1)})


class WishlistViewAddDel(View):

    def get(self, request, id):

        if not request.user.is_authenticated:
            # код который необходим для обработчика
            # return render(request, "store/wishlist.html")
            # Иначе отправляет авторизироваться
            return redirect('login:login')  # from django.shortcuts import redirect
        wishlist_data = models.WishList.objects.all()
        id_list = []

        for i in wishlist_data:
            print(id_list, "  +  ", end='')
            id_list.append(i.product_id)

            print(i.id)
        print(id_list)

        if id not in id_list:
            obj = models.Product.objects.get(id=id)
            print(obj)

            obj_todo = models.WishList(user=request.user, product=obj)
            obj_todo.save()
            print("create   ", obj_todo)
            return redirect('store:wishlist')  # store/wishlist.html
        else:
            return redirect('store:shop')


class WishlistViewDel(View):

    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect('login:login')  # from django.shortcuts import redirect

        obj_todo = models.WishList.objects.filter(product_id=id).delete()
        print(obj_todo, " DELETE TODO")
        return redirect('store:wishlist')  # store/wishlist.html
