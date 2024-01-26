from django.urls import path
# from .views import ShopView, ProductSingleView, CartViewSet, WishListViewSet, CartView, WishlistView
from rest_framework import routers

import store.views as view

router = routers.DefaultRouter()
router.register(r'cart', view.CartViewSet)
# router.register(r'wishlist', view.WishListViewSet)

app_name = 'store'
urlpatterns = [
    path('', view.ShopView.as_view(), name='shop'),
    path('index/', view.ShopView.as_view(), name='shop'),
    path('cart/', view.CartView.as_view(), name='cart'),
    path('product/<int:id>', view.ProductSingleView.as_view(), name='product'),
    path('wishlist/', view.WishlistView.as_view(), name='wishlist'),
    path('wishlistadd/<int:id>', view.WishlistViewAddDel.as_view(), name='wishlistadd'),
    path('wishlistdel/<int:id>', view.WishlistViewDel.as_view(), name='wishlistdel'),
    ]
