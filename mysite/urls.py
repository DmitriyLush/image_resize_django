"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include
from pill import views
from django.conf import settings
from django.conf.urls.static import static

from pill.views import serve_static

urlpatterns = [
    path('', lambda request: redirect('home/', permanent=False)),
    path('pill/', include('pill.urls')),
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('home/', views.home),
    path('resize/<filename>', views.resize),
]
urlpatterns += static(f'{settings.MEDIA_URL}', view=serve_static,
                      document_root=settings.MEDIA_ROOT)
