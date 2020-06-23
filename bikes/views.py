from django.db import IntegrityError
from django.db import models
from rest_framework import exceptions
from rest_framework import generics
from .utills import query_value_serialize
from .models import Bike, BikeImage
from .serializers import (
    BikePaymentMethodSerializer,
    BikeListSerializer,
    BikeCreateSerializer,
    BikeUpdateSerializer,
    BikeImageCreateSerializer,
    BikeImageDeleteSerializer,
    RegisteredBikeListSerializer
)

class BikeList(generics.ListAPIView):
    serializer_class = BikeListSerializer

    default_limit = 6

    def get_queryset(self):
        query_params = query_value_serialize(self.request.query_params)
        page = query_params.pop('page') if 'page' in query_params.keys() else 0

        queryset = Bike.objects.select_related(
            'payment_method', 'user',
        ).prefetch_related(
            'bike_image',
        ).filter(
            **query_params,
        ).order_by('-pk').all()[page*self.default_limit:(page+1)*self.default_limit]

        return queryset

class BikeCreate(generics.CreateAPIView):
    serializer_class = BikeCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class BikeUpdate(generics.UpdateAPIView):
    serializer_class = BikeUpdateSerializer

    def get_queryset(self):
        return Bike.objects

    def get_object(self):
        object = super().get_object()
        if object.user == self.request.user:
            return object
        else:
            raise exceptions.PermissionDenied('수정 할 권한이 없습니다.')

class BikeImageCreate(generics.CreateAPIView):
    serializer_class = BikeImageCreateSerializer

    def perform_create(self, serializer):
        try:
            return serializer.save()
        except IntegrityError:
            raise exceptions.ValidationError("잘못된 형식입니다.")

class BikeImageDelete(generics.DestroyAPIView):
    serializer_class = BikeImageDeleteSerializer

    def get_queryset(self):
        return BikeImage.objects.select_related('bike_image')

    def get_object(self):
        object = super().get_object()
        if object.item.user == self.request.user:
            return object
        else:
            raise exceptions.PermissionDenied('수정 할 권한이 없습니다.')

class RegisteredBikeList(generics.ListAPIView):
    serializer_class = RegisteredBikeListSerializer

    def get_queryset(self):
        return self.request.user.bike_set.order_by('-pk')
