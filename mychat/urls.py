from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from PrepMate import urls as PM
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('PrepMate/',include(PM)),
    path('',views.home)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)