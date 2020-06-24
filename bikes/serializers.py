from rest_framework import serializers, fields

from .models import BikePaymentMethod, Bike, BikeImage

required_false = {'required': False}

class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike

    def to_representation(self, instance):
        return instance.get_info()

class BikePaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikePaymentMethod
        fields = ('card', 'cash', 'loan', 'trade', 'lease',)
        extra_kwargs = {field: required_false for field in fields}

class BikeListSerializer(serializers.ModelSerializer):
    model_year__gte = fields.IntegerField(min_value=1950, max_value=2100, required=False)
    model_year__lte = fields.IntegerField(min_value=1950, max_value=2100, required=False)
    price__gte = fields.IntegerField(min_value=0, max_value=4500, required=False)
    price__lte = fields.IntegerField(min_value=50, required=False)
    distance__gte = fields.IntegerField(min_value=0, max_value=100000, required=False)
    distance__lte = fields.IntegerField(min_value=0, required=False)
    payment_method = BikePaymentMethod()
    payment_method__card = fields.BooleanField(required=False)
    payment_method__lease = fields.BooleanField(required=False)
    page = fields.IntegerField(min_value=0, required=False)

    class Meta:
        model = Bike
        # 쿼리 옵션 https://docs.djangoproject.com/en/3.0/ref/models/querysets/
        fields = (
            'model'
            'deal_area',
            'bike_style'
            'model_year__gte',
            'model_year__lte',
            'price__gte',
            'price__lte',
            'driven_distance__gte',
            'driven_distance__lte',
            'payment_method',
            'payment_method__card',
            'payment_method__lease',
            'page',
        )
        extra_kwargs = {
            'model': required_false,
            'deal_area': required_false,
            'model_year': required_false,
        }

    def to_representation(self, instance):
        return instance.get_info()

class BikeCreateSerializer(serializers.ModelSerializer):
    payment_method = BikePaymentMethodSerializer()

    class Meta:
        model = Bike
        fields = (
            'model',
            'bike_style',
            'price',
            'deal_area',
            'model_year',
            'driven_distance',
            'document_status',
            'repair_history',
            'tuning_history',
            'detail_information',
            'payment_method',
        )
        extra_kwargs = {
            'driven_distance': required_false,
            'document_status': required_false,
            'repair_history': required_false,
            'tuning_history': required_false,
        }
    
    def to_representation(self, instance):
        return instance.get_info()

    def create(self, validated_data):
        payment_method = BikePaymentMethod(**validated_data.pop('payment_method'))
        payment_method.save()
        validated_data['payment_method_id'] = payment_method.pk
        return super().create(validated_data)

class BikeUpdateSerializer(serializers.ModelSerializer):
    payment_method = BikePaymentMethodSerializer()

    class Meta:
        model = Bike
        fields = (
            'price',
            'deal_area',
            'model_year',
            'driven_distance',
            'document_status',
            'repair_history',
            'tuning_history',
            'detail_information',
            'payment_method',
        )
        extra_kwargs = {field: required_false for field in fields}

    def update(self, instance, validated_data):
        if 'payment_method' in validated_data:
            update_data = validated_data.pop('payment_method')
            for attr, value in update_data.items():
                setattr(instance.payment_method, attr, value)
            instance.payment_method.save()
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return instance.get_info()

class BikeDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike

class BikeImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeImage
        fields = (
            'image',
            'bike',
        )

    def to_representation(self, instance):
        return instance.get_info()

class BikeImageDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeImage


