"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from home.views import home, contact, about, index
from vege.views import (
    receipes, students, delete_receipe, update_receipe,
    login_page, register, logout_page, see_marks, student_report
)
from mruandsru.views import mruandsru, bscaboutus
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),
    path('receipes/', receipes, name='receipes'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('delete_receipe/<id>/', delete_receipe, name='delete_receipe'),
    path('update_receipe/<id>/', update_receipe, name='update_receipe'),
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_page, name='logout'),
    path('mruandsru/', mruandsru, name='mruandsru'),
    path('bscaboutus/', bscaboutus, name='bscaboutus'),
    path('index/', index, name='index'),
    path('see_marks/<student_id>/', see_marks, name='see_marks'),
    path('students/', students, name='students'),
    path('check-the-marks/<str:student_id>/', student_report, name='check_marks'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()