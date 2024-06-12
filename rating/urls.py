from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    path('giveRating/<int:technician_id>/<int:booking_id>/', views.giveRating, name='giveRating'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


