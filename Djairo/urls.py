from django.contrib import admin
from django.urls import path, include
from pymesApp.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    # Prefijo global /api/ para Django REST Framework
    path('api/', include(router.urls)),
    # Rutas de la app base
    path('', include('pymesApp.urls')),
]

handler404 = 'pymesApp.views_errors.pagina_no_encontrada'
