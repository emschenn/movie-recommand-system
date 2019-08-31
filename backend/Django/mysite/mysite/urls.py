"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import sys
sys.path.append("..")
from django.contrib import admin
from django.urls import path
from trips.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('post/', img_post),
    path('face_detect/', face_post),
    path('add/', add_to_group),
    path('user/', user_seach),
    path('test/', test_req),
    path('new_user_list/', user_list),
    path('update_rating/', update_rating),
    path('update_favorite/', update_favorite),
    path('get_favorite/', get_favorite),
    path('remove_favorite/', remove_favorite),
    path('get_movie_rating/', get_movie_rating),
    path('post_i2vId/', post_i2vId),
]


