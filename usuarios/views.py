from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def acceso_ejecutivo(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        contraseña = request.POST['password']
        user = authenticate(request, username=usuario, password=contraseña)
        if user is not None:
            login(request, user)
            # Redirige al dashboard después de login exitoso
            return redirect('dashboard_home')
        else:
            return render(request, 'usuarios/login.html', {
                'error': 'Credenciales inválidas'
            })
    return render(request, 'usuarios/login.html')
