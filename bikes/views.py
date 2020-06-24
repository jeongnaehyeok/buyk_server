from django.db import IntegrityError
from django.db import models
from rest_framework import exceptions
from rest_framework import generics
from .utills import serialize_query_params
from rest_framework.filters import SearchFilter
from .models import Bike, BikeImage
from .serializers import (
    BikePaymentMethodSerializer,
    BikeSerializer,
    BikeListSerializer,
    BikeCreateSerializer,
    BikeUpdateSerializer,
    BikeDeleteSerializer,
    BikeImageCreateSerializer,
    BikeImageDeleteSerializer,
)

class BikeList(generics.ListAPIView):
    serializer_class = BikeListSerializer
    filter_backends = [SearchFilter]
    search_fields = ('model')
    default_limit = 6

    def get_queryset(self):
        query_params = serialize_query_params(self.request.query_params)
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
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)
        else:
            raise exceptions.PermissionDenied('로그인이 필요합니다.')

class BikeDetail(generics.RetrieveAPIView):
    serializer_class = BikeSerializer
    queryset = Bike.objects.all()

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

class BikeDelete(generics.DestroyAPIView):
    serializer_class = BikeDeleteSerializer

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
        if not self.request.user.is_authenticated:
            raise exceptions.PermissionDenied('로그인이 필요합니다.')
        if not bool(self.request.user.bike_set.all().filter(id=self.request.data['bike'])):
            raise exceptions.PermissionDenied('해당 매물을 수정 할 권한이 없습니다.')
        try:
            return serializer.save()
        except IntegrityError:
            raise exceptions.ValidationError("잘못된 형식입니다.")

class BikeImageDelete(generics.DestroyAPIView):
    serializer_class = BikeImageDeleteSerializer

    def get_queryset(self):
        return BikeImage.objects.select_related('bike__user')

    def get_object(self):
        object = super().get_object()
        if object.bike.user == self.request.user:
            return object
        else:
            raise exceptions.PermissionDenied('해당 매물을 수정 할 권한이 없습니다.')

class RegisteredBikeList(generics.ListAPIView):
    serializer_class = BikeSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.bike_set.order_by('-pk')
        else:
            raise exceptions.PermissionDenied('로그인이 필요합니다.')
