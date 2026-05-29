from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            form.add_error("username", "Bu kullanıcı adı zaten kullanılıyor.")
            return render(request, "register.html", {"form": form})

        login(request, user)
        messages.info(request, "Başarıyla kayıt oldunuz.")
        return redirect("index")

    return render(request, "register.html", {"form": form})


def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request, "Kullanıcı adı veya parola hatalı.")
            return render(request, "login.html", context)
        messages.success(request, "Başarıyla giriş yaptınız.")
        login(request, user)
        return redirect("index")
    return render(request, "login.html", context)


@require_POST
def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")
    return redirect("index")
