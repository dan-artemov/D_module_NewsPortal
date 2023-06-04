"""
URL configuration for NewsPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('news.urls')),
    # # D5.2 добавим urls приложения, с которым ранее работали в этом модуле — “django.contrib.auth”
    # path('accounts/', include('django.contrib.auth.urls')),

    # Изменим способ регистрации и   оставим только allauth
    path("accounts/", include("allauth.urls")),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("accounts/login/", LoginView.as_view(), name="login"),
]
