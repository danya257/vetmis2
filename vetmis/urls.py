# vetmis/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# vetmis/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('pets/', include('pets.urls')),
    path('clinics/', include('clinics.urls')),
    path('records/', include('medical_records.urls')),
    path('api/', include('api.urls')),
    path('core/', include('core.urls')),
    path('', include('blog.urls')),
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)