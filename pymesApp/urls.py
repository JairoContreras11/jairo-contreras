from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router de Django REST Framework
router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')
router.register(r'productos', views.ProductoViewSet, basename='producto')

app_name = "pymesApp"

urlpatterns = [
    # Vista HTML original de bienvenida
    path("", views.bienvenida, name="bienvenida"),
    # Endpoints REST
    path("api/", include(router.urls)),
]
