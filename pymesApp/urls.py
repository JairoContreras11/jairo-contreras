from django.urls import path
from . import views

app_name = "pymesApp"

urlpatterns = [
    path("", views.bienvenida, name="bienvenida"),
]
