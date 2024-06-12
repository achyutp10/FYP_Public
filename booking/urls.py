from django.urls import path
from .import views


urlpatterns = [
    path('bookTechnician/', views.bookTechnician, name='bookTechnician'),
    path('bookNow/<int:technician_id>/', views.bookNow, name='bookNow'),
    path('changeStatus/<int:booking_id>/', views.changeStatus, name='changeStatus'),
    path('giveStatus/<int:booking_id>/', views.giveStatus, name='giveStatus'),
    path('customerBookingList/',views.customerBookingList, name='customerBookingList'),
    path('checkout/<int:booking_id>/',views.checkout, name='checkout'),
    path('checkout_session/<int:booking_id>/',views.checkout_session, name='checkout_session'),
    path('pay_success/',views.pay_success, name='pay_success'),
    path('pay_cancel/',views.pay_cancel, name='pay_cancel'),

    # SEARCH
    path('search/', views.search, name='search'),


]
