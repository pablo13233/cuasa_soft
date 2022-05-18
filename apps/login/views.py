from django.shortcuts import render,redirect

from apps.usuarios.models import User
from django.contrib.auth import login as auth_login, logout, authenticate
# Create your views here.
 

#view login con validaciones

def login(request):
    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        contrasena  = request.POST.get('pass')
        user = authenticate(username=username, password=contrasena)
        #verifica si exite cuenta 
        if user is not None:
            if user.is_active:#si esta activo
                auth_login(request, user)
                return redirect('home_app:home')
            else:
                mensaje = 'USUARIO INACTIVO'
                ctx = {'mensaje':mensaje}
                return render(request, 'login/login.html', ctx)
        else:
            mensaje = 'USUARIO O CONTRASEÑA INCORRECTOS'
            ctx = {'mensaje':mensaje, 'username':username}
            return render(request, 'login/login.html', ctx)
    return render(request, 'login/login.html')

#view cierre sesion
def logout_view(request):
    logout(request)
    return redirect('login_app:login')