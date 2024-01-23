from rest_framework import routers, serializers, viewsets
from .models import Cart, Person


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'short_name', 'reg_data' ]

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    # serializer_class = PersonSerializer