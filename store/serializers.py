from rest_framework import routers, serializers, viewsets
from .models import Cart, Person, WishList


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'short_name', 'reg_data' ]

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    # serializer_class = PersonSerializer

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'
