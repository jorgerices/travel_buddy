from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import User


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    
    return redirect("/login")
    

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "name": f"{log_user}",
                    "firstname": log_user.firstname,
                    "lastname": log_user.firstname,
                    "email": log_user.email,
                    "role": log_user.role
                }

                request.session['user'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/")
            else:
                messages.error(request, "Password o Email incorrectos.")
        else:
            messages.error(request, "Email o password incorrectos.")



        return redirect("/login")
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            
            request.session['register_name'] =  request.POST['name']
            request.session['register_firstname'] =  request.POST['firstname']
            request.session['register_lastname'] =  request.POST['lastname']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_name'] = ""
            request.session['register_firstname'] = ""
            request.session['register_lastname'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                name = request.POST['name'],
                firstname = request.POST['firstname'],
                lastname = request.POST['lastname'],
                email=request.POST['email'],
                password=password_encryp,
                role=request.POST['role']
            )

            messages.success(request, f"El usuario {usuario_nuevo.name} fue agregado con éxito")
            

            request.session['user'] = {
                "id" : usuario_nuevo.id,
                "name": f"{usuario_nuevo.name}",
                "firstname": usuario_nuevo.firstname,
                "lastname": usuario_nuevo.firstname,
                "email": usuario_nuevo.email
            }
            return redirect("/")

        return redirect("/register")
    else:
        return render(request, 'register.html')
