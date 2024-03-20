import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

import users.forms
import users.models


__all__ = []


def signup(request):
    form = users.forms.SignUpForm(request.POST or None)
    template = "users/signup.html"
    context = {
        "form": form,
    }
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=True)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        send_mail(
            subject="User",
            message=render_to_string("users/signup_email.html"),
            from_email=settings.EMAIL_HOST,
            recipient_list=[form.cleaned_data["email"]],
        )
        username = form.cleaned_data.get("username")
        messages.success(
            request,
            f"Пользователь {username} был успешно создан!",
        )
        return redirect(reverse("homepage:main"))

    return render(request, template, context)


def activate(request, username):
    user = get_object_or_404(
        get_user_model().objects,
        username=username,
    )
    if timezone.now() > user.date_joined + datetime.timedelta(hours=12):
        messages.success(request, "Сообщение успешно отправлено!")
    else:
        messages.error(request, "Сообщение не отправлено!")

    return redirect(reverse("homepage:main"))


@login_required
def profile(request):
    profile_form = users.forms.ProfileForm(
        request.POST or None,
        instance=request.user.profile,
    )
    user_form = users.forms.CustomUserChangeForm(
        request.POST or None,
        instance=request.user,
    )
    if request.method == "POST":
        if all((profile_form.is_valid(), user_form.is_valid())):
            profile_form.save()
            user_form.save()

    return render(
        request,
        "users/profile.html",
        {
            "profile_form": profile_form,
            "user_form": user_form,
            "user": request.user,
        },
    )


def user_list(request):
    users = get_user_model().objects.filter(is_active=True)
    return render(
        request,
        "users/user_list.html",
        {"users": users},
    )


def user_detail(request, ide):
    user = get_object_or_404(
        get_user_model(),
        pk=ide,
    )
    try:
        profile = user.profile
    except users.models.Profile.DoesNotExist:
        profile = None

    return render(
        request,
        "users/user_detail.html",
        {"user": user, "profile": profile},
    )
