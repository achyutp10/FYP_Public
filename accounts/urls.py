from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerTechnician/', views.registerTechnician, name='registerTechnician'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name="myAccount"),
    path('custDashboard/', views.custDashboard, name="custDashboard"),
    path('technicianDashboard/', views.technicianDashboard, name="technicianDashboard"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),

    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name="reset_password_validate"),
    path('reset_password/', views.reset_password, name="reset_password"),

    path('updateTechnicianInfo/', views.updateTechnicianInfo, name="updateTechnicianInfo"),
    path('updateCustomerInfo/', views.updateCustomerInfo, name="updateCustomerInfo"),
    path('changePassTech/', views.changePassTech, name="changePassTech"),
    path('changePassCust/', views.changePassCust, name="changePassCust"),
    path('updateStatus/', views.update_status, name='update_status'),
    path('cprofile/',views.cprofile, name='cprofile'),

    path('technician/', include('technician.urls')),
    path('booking/', include('booking.urls')),
    path('rating/', include('rating.urls')),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
