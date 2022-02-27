from django.urls import path
from .views import rainfall_data


urlpatterns = [
    path('', rainfall_data )
]
