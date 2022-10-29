"""Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# Import the core libraries and functions
from django.contrib import admin
from django.urls import include, path


# Base URL patterns that allow access to different server Apps
urlpatterns = [
    # Provides server path / access to the `accounts` URLS
    path('accounts/', include('accounts.urls')),
    # Built-in Django admin site.
    # Accessed via: http://localhost:8000/admin (development)
    path('admin/', admin.site.urls),
]
