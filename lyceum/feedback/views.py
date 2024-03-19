from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import (
    FeedbackAuthorForm,
    FeedbackFileForm,
    FeedbackForm,
)
from feedback.models import FeedbackFile

__all__ = ["feedback"]


def feedback(request):
    author_form = FeedbackAuthorForm(request.POST or None)
    form = FeedbackForm(request.POST or None)
    files_form = FeedbackFileForm(request.POST or None, request.FILES or None)

    if (
        request.method == "POST"
        and author_form.is_valid()
        and form.is_valid()
        and files_form.is_valid()
    ):
        feedback_instance = form.save(commit=True)
        author_form.instance.feedback = feedback_instance
        author_form.save(commit=True)

        files = files_form.cleaned_data["files"]
        for file in files:
            FeedbackFile(file=file, feedback=feedback_instance).save()

        send_mail(
            subject="Feedback",
            message=form.cleaned_data["text"],
            from_email=settings.EMAIL_HOST,
            recipient_list=[author_form.cleaned_data["mail"]],
        )
        messages.success(request, "Форма успешно отправлена!")
        return redirect(request.path)

    context = {
        "author": author_form,
        "form": form,
        "files": files_form,
    }
    return render(request, "feedback/feedback.html", context)
