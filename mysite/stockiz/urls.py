from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', index, name="dashboard"),
    path('features/', feature, name="features"),
    path('data/<str:symbol>/', get_stock_data, name='stock_data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
