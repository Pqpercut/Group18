"""
URL configuration for hatsforcats project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from ecommerceapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("tempVarients", views.basketAdd, name="basketAdd"),
    path("tempBasket.html", views.basketRem, name="basketRem"),
    path("", views.productDisplay, name="productDisplay"),
    path("tempVarients.html", views.variantDisplay, name="variantDisplay"),
    path("tempBasket.html", views.viewBasket, name="basketview"),
    path("tempCheckout.html", views.checkout, name="checkout")
]
