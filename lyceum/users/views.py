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
import users.email

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
        users.models.Profile.objects.create(
            user=user,
        )
        user.profile.save()
        send_mail(
            subject="Signup",
            message=render_to_string("users/signup_email.html"),
            from_email=settings.EMAIL_HOST,
            recipient_list=[form.cleaned_data["email"]],
        )
        username = form.cleaned_data.get("username")
        messages.success(
            request,
            f"Пользователь {username} был успешно создан!",
        )
        return redirect(reverse("users:login"))

    return render(request, template, context)


def activate(request, username):
    user = get_object_or_404(
        get_user_model().objects,
        username=username,
    )
    registration_time_limit = timezone.now() - timezone.timedelta(hours=12)

    if user.date_joined >= registration_time_limit:
        user.is_active = True
        user.save()
        messages.success(request, "Активация прошла успешно")
    else:
        messages.error(request, "Ошибка при активации")

    return redirect(reverse("homepage:main"))


def deactivate(request, username):
    template = "users/user_deactivate.html"
    context = {"attempts": settings.MAX_AUTH_ATTEMPTS}

    user = get_object_or_404(
        get_user_model(),
        username=username,
    )

    users.email.send_user_email(
        username,
        user.email,
        "users/reactivate_email.html",
    )

    return render(request, template, context)


def reactivate(request, username):
    user = get_object_or_404(
        get_user_model().objects,
        username=username,
    )
    reactivate_time_limit = timezone.now() - timezone.timedelta(days=7)

    if user.profile.block_date >= reactivate_time_limit:
        user.is_active = True
        user.profile.auth_attempts = 0
        user.save()
        user.profile.save()
        messages.success(
            request,
            "Ваш аккаунт снова активирован",
        )
    else:
        messages.error(request, "Ошибка при активации")

    return redirect(reverse("users:login"))


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
