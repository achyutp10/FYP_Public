"""
URL configuration for fixit_main project.

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
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', views.admin, name='admin'),
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('adminTechnician/', views.adminTechnician, name='adminTechnician'),
    path('adminCustomer/', views.adminCustomer, name='adminCustomer'),
    path('adminBooking/', views.adminBooking, name='adminBooking'),
    path('assignStatus/<int:technician_id>/', views.assignStatus, name='assignStatus'),
    path('deleteUser/<int:customer_id>/', views.deleteUser, name='deleteUser'),
    path('deleteTechnician/<int:technician_id>/', views.deleteTechnician, name='deleteTechnician'),
    path('deletebooking/<int:booking_id>/', views.deletebooking, name='deletebooking'),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
