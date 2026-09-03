from django.shortcuts import render
from datetime import datetime


def bienvenida(request):
    """
    Vista principal del proyecto 'Sistema de Inventario para PYMEs'.
    Etapa: Evaluación 1 (nucleo Django + rutas + bienvenida).
    Sin modelo de datos ni base de datos todavia (siguiente evaluacion).
    """
    nombre_proyecto = "Sistema de Inventario para PYMEs"
    hora_actual = datetime.now().hour

    if hora_actual < 12:
        saludo = "Buenos dias"
    elif hora_actual < 19:
        saludo = "Buenas tardes"
    else:
        saludo = "Buenas noches"

    modulos_planificados = ["Autenticacion", "Productos", "Stock", "Reportes"]
    total_modulos = len(modulos_planificados)
    modulos_completados = 1
    avance_porcentual = round((modulos_completados / total_modulos) * 100)

    contexto = {
        "nombre_proyecto": nombre_proyecto,
        "saludo": saludo,
        "modulos_planificados": modulos_planificados,
        "total_modulos": total_modulos,
        "avance_porcentual": avance_porcentual,
    }

    return render(request, "pymesApp/bienvenida.html", contexto)
