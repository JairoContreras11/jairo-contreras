from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pymesApp.urls")),
]

handler404 = "pymesApp.views_errors.pagina_no_encontrada"
