"""
URL configuration for DjangoCRUD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tarea import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('Iniciar_sesion', views.abrir_sesion, name="abrir_sesion"),
    path('Registrar/', views.registrar, name="registrar"),
    path('Tareas/', views.tareas, name="tareas"),
    path('TareasCompletadas/', views.tareas_completadas, name="tareas_completadas"),
    path('Tareas/CrearTarea/', views.crear_tarea, name="crear_tarea"),
    path('Tareas/<int:id>', views.detalle_tarea, name="detalle_tarea"),
    path('Tareas/<int:id>/CompletarTarea', views.completar_tarea, name="completar_tarea"),
    path('Tareas/<int:id>/EliminarTarea', views.eliminar_tarea, name="eliminar_tarea"),
    path('Salir/', views.cerrar_sesion, name="cerrar_sesion"),
]
