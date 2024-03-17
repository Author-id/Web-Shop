from django.shortcuts import render, redirect
from users.forms import UserRegisterForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Пользователь {username} был успешно создан!')
            return redirect("http://127.0.0.1:8000/")
    else:
        form = UserRegisterForm()

    return render(
        request,
        "users/signup.html",
        {
            "title": "Страница регистрации",
            "form": form,
        }
    )


