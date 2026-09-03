from django.shortcuts import render


def pagina_no_encontrada(request, exception):
    """Vista personalizada para el error 404 (criterio 4.3)."""
    return render(request, "pymesApp/404.html", status=404)
