from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.contrib.auth.models import User


class BikePaymentMethod(models.Model):
    card = models.BooleanField(default=False)
    cash = models.BooleanField(default=False)
    loan = models.BooleanField(default=False)
    trade = models.BooleanField(default=False)
    lease = models.BooleanField(default=False)

    def get_info(self):
        return {
            'card': self.card,
            'cash': self.cash,
            'loan': self.loan,
            'trade': self.trade,
            'lease': self.lease,
        }


class Bike(models.Model):
    DEAL_AREA_CHOICES = (
        ('SU', '서울'),
        ('BS', '부산'),
        ('IC', '인천'),
        ('GJ', '광주'),
        ('US', '울산'),
        ('DJ', '대전'),
        ('SJ', '세종'),
        ('DG', '대구'),
        ('GG', '경기'),
        ('GW', '강원'),
        ('GN', '경남'),
        ('GB', '경북'),
        ('CB', '충북'),
        ('CN', '충남'),
        ('JB', '전북'),
        ('JN', '전남'),
        ('JJ', '제주'),
    )
    DOCUMENT_STATUS_CHOICES = (
        ('U', '준비되지않음'),
        ('R', '준비됨'),
        ('N', '없음'),
    )
    BIKE_STYLE_CHOICES = (
        ('NK', '네이키드'),
        ('RL', '레플리카'),
        ('AM', '아메리칸'),
        ('SC', '스쿠터'),
        ('TL', '투어링'),
        ('EL', '전기'),
        ('CM', '상업용'),
        ('AT', 'ATV'),
        ('OL', '오프로드'),
        ('MI', '포켓/미니'),
    )

    model = models.CharField(max_length=127)
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='bike_set',
    )
    price = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(200000),
        ]
    )
    bike_style = models.CharField(
        max_length=2,
        choices=BIKE_STYLE_CHOICES,
    )
    payment_method = models.OneToOneField(
        BikePaymentMethod,
        models.CASCADE,
    )
    deal_area = models.CharField(
        max_length=2,
        choices=DEAL_AREA_CHOICES,
    )
    model_year = models.IntegerField(
        validators=[
            MinValueValidator(1950),
            MaxValueValidator(2100),
        ]
    )
    driven_distance = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(2000000),
        ]
    )
    document_status = models.CharField(
        max_length=1,
        choices=DOCUMENT_STATUS_CHOICES,
        default=None,
        null=True,
    )
    repair_history = models.TextField(
        max_length=2047,
        null=True,
    )
    tuning_history = models.TextField(
        max_length=2047,
        null=True,
    )
    detail_information = models.TextField(
        max_length=2047,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_info(self):
        return {
            'id': self.pk,
            'model': self.model,
            'user': self.user.get_username(),
            'price': self.price,
            'bike_style': self.get_bike_style_display(),
            'payment_method': self.payment_method.get_info(),
            'images': [
                image.get_info()
                for image
                in self.bike_image.order_by('id').all()
            ],
            'deal_area': self.get_deal_area_display(),
            'model_year': self.model_year,
            'driven_distance': self.driven_distance,
            'document_status': self.get_document_status_display(),
            'repair_history': self.repair_history,
            'tuning_history': self.tuning_history,
            'detail_information': self.detail_information,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class BikeImage(models.Model):
    bike = models.ForeignKey(
        Bike,
        models.CASCADE,
        related_name='bike_image',
    )
    image = models.ImageField(upload_to='buyk/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_info(self):
        return {
            'id': self.pk,
            'image': self.image.url,
        }

    # 자동 삭제
    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(BikeImage, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)