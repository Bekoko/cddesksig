from django.contrib import admin
from django.urls import path

from scan.views import scan

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', scan, name='scan'),
]
