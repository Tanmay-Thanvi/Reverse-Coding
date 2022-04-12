"""rcr1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
urlpatterns = [
    path('start/',views.start,name='start'),
    path('addtime/',views.addtime,name='addtime'),
    path('panel/',views.home,name='home'),
    path('activatelifeline1/',views.zoneactivate,name='activatelifeline1'),
    path('activatelifeline2/',views.activatelifeline2,name='activatelifeline2'),
    path('riddle/',views.riddleque,name='riddle'),
    path('instructions/',views.instructions,name='instructions'),
    path('finish/',views.finish,name='finish'),
]
