from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import RegisterForm,LoginForm


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        if User.objects.filter(username=username).exists():
            form.add_error("username", "Bu kullanıcı adı zaten kullanılıyor.")
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            messages.info(request,"basariylakayitoldunuz")
            return redirect("index")

    return render(request, "register.html", {"form": form})


def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username,password = password)
        if user is None:
            messages.info(request,"kullaniciadiveyaparolahatali")
            return render(request,"login.html",context)
        messages.success(request,"basariylagirisyaptiniz")
        login(request,user)
        return redirect("index")
    return render(request, "login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"basariylacikisyaptiniz")
    return redirect("index")