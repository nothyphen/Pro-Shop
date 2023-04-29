from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Permission

# Create your views here.
def account(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return redirect('/login')

def login_web(request):
    try:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            if request.method ==  "POST":
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    return redirect('/account/login')
            template_name = 'login.html'
            return render(request, template_name)
    except:
        return render(request, 'error_login2.html')

def logout_web(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return render(request, 'error_login.html')

def register(request):
    if request.user.is_authenticated:
        return render(request, 'error_login.html')
    else:
        try:
            if request.method == "POST":
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                user.save()
                return redirect('/account/login')
        except :
            template_name = 'error_login.html'
            return render(request, template_name)
    template_name = 'register.html'
    return render(request, template_name)