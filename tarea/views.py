from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from .forms import TareaForm
from .Validar import validarUsuario
from .models import Tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required
 
# Create your views here.
def home(request):
    return render(request,"Home.html")

def registrar(request):
    if request.method == "GET":
        return render(request,"Registrar.html",{
            "form": UserCreationForm
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            u = User(username=request.POST["username"], password=request.POST["password1"])
            if validarUsuario(u):
                
                try:
                    us=User.objects.create_user(username=u.username, password=u.password)       
                    login(request,us)
                    return redirect("tareas")
                except Exception as e:
                    return render(request,"Registrar.html",{
                        "form": UserCreationForm,
                        "error" : "El usuario ya existe"
                        })
            else:
                return render(request,"Registrar.html",{
                        "form": UserCreationForm,
                        "error" : "Usuario o contraseña no valido"
                    })
        else:
            return render(request,"Registrar.html",{
            "form": UserCreationForm,
            "error" : "Las contraseñas no son iguales"
        })

def abrir_sesion(request):
    if request.method == "GET":      
        return render(request,"Login.html",{
            "form": AuthenticationForm
        })
    else:
       u = authenticate(request, username=request.POST["username"], password = request.POST["password"])
       if u is None:
           return render(request,"Login.html",{
            "form": AuthenticationForm,
            "error": "Usario o contraseña incorrecta"
            })
       else:
           login(request,u)
           return redirect("tareas")

@login_required
def tareas(request):
    tareas = Tarea.objects.filter(user=request.user,fecha_completada__isnull = True)
    return render(request,"Tareas.html",{
        "tareas": tareas,
        "tipo": "pendientes"
    })
    
@login_required
def tareas_completadas(request):
    tareas = Tarea.objects.filter(user=request.user,fecha_completada__isnull = False).order_by("-fecha_completada")
    return render(request,"Tareas.html",{
        "tareas": tareas,
        "tipo": "completadas"
    })

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect("abrir_sesion")

@login_required
def crear_tarea(request):
    if request.method == "GET":
        return render(request,"Crear_tarea.html",{
            "form": TareaForm
            })  
    else:
        try:
            form = TareaForm(request.POST)
            nueva_tarea = form.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()
            return redirect("tareas")
        
        except:
            return render(request,"Crear_tarea.html",{
                "form": TareaForm,
                "error": "El titulo debe tener una longitud de 1 a 50 caracteres"
                })    
            
@login_required
def detalle_tarea(request,id=0):
    if request.method == "GET":
        #Traer por id y id de usuario, asi no puede un usuario entrar a tareas de otro
        t = get_object_or_404(Tarea, id=id,user=request.user)
        form = TareaForm(instance=t)
        return render(request,"Tarea_detalle.html",{
                "tarea":t,
                "form":form,
            })
    else:
        try:
            #Ambas forman estan bien, pero con ! puedo usar tambien el | para un or
            t = get_object_or_404(Tarea, Q(id=id) & Q(user=request.user))
            form = TareaForm(request.POST, instance=t)
            form.save()
            return redirect("tareas")
        except ValueError:
            return render(request,"Tarea_detalle.html",{
                    "tarea":t,
                    "form":form,
                    "error": "Error al actualizar la tarea"
                })

@login_required
def completar_tarea(request,id=0):
    t = get_object_or_404(Tarea, Q(id=id) & Q(user=request.user))
    if request.method == "POST":
        t.fecha_completada = timezone.now()#Ya que la computadora esta 3 horas atras del servidor, este me va a dar un horario 3 horas mayor, osea si son las 5, cuando lo complete, va a guardar que se completo a las 8, para evitarlo deberia restarle 3 horas al timezone.now()
        t.save()
        return redirect(tareas)
    
@login_required
def eliminar_tarea(request,id=0):
    t = get_object_or_404(Tarea, Q(id=id) & Q(user=request.user))
    if request.method == "POST":
        t.delete()
        return redirect(tareas)
    

       
        
    
