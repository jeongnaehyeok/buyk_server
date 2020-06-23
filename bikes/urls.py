from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    BikeList,
    BikeCreate,
    BikeUpdate,
    BikeDelete,
    BikeImageCreate,
    BikeImageDelete,
    RegisteredBikeList
    )

urlpatterns = [
    path('list/', BikeList.as_view()),
    path('list/register/', RegisteredBikeList.as_view()),
    path('create', BikeCreate.as_view()),
    path('<int:pk>/update', BikeUpdate.as_view()),
    path('<int:pk>/delete', BikeDelete.as_view()),
    path('image/create', BikeImageCreate.as_view()),
    path('image/<int:pk>/delete', BikeImageDelete.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
