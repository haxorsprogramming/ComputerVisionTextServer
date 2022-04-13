from django.contrib import admin
from django.urls import path

from CoreApp import views as CoreApp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core-app', CoreApp.mainApp)
]
