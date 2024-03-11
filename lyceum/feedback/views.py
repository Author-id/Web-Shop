from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from feedback.forms import FeedbackForm


__all__ = []


def feedback(request):
    form = FeedbackForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save(commit=True)
        send_mail(
            subject="Feedback",
            message=form.cleaned_data["text"],
            from_email=settings.EMAIL_HOST,
            recipient_list=[form.cleaned_data["mail"]],
        )
        messages.success(request, _("Форма успешно отправлена!"))
        return redirect(request.path)

    context = {"form": form}
    return render(request, "feedback/feedback.html", context)
