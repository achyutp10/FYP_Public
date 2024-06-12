from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.messages_page, name='messages_page'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
