from django.urls import path, include
from .import views


urlpatterns = [
    path('profile/',views.tprofile, name='tprofile'),
    path('technicianBookingList/',views.technicianBookingList, name='technicianBookingList'),
    path('viewLocation/', views.viewLocation, name='viewLocation'),
    path('get_user_locations/', views.get_user_locations, name='get_user_locations'),


]
