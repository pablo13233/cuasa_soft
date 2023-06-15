
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
    path('', include('apps.tickets.urls')),
    path('', include('apps.usuarios.urls')),
    path('', include('apps.login.urls')),
    path('', include('apps.inventario.urls')),
    path('', include('apps.asignaciones.urls')),
    path('', include('apps.historico.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
