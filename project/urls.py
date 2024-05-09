"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', ReactView.as_view(), name="anything"),
    path('user/login', UserView.as_view(), name="anything"),
    path('reader/login', ReaderLoginView.as_view(), name="anything"),
    path('reader/register', ReaderRegisterView.as_view(), name="anything"),
    path('book', BookView.as_view(), name="anything"),
    path('book/content/<int:book_id>', BookContentView, name="anything"),
    path('book/upload/<int:book_id>/<str:fileName>', BookUploading, name='book_upload'),
    path('Path', getPathOS, name='getPathOS'),
]