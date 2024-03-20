from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm

__all__ = []


def feedback(request):
    feedback_form = FeedbackForm(request.POST or None)
    context = {"form": feedback_form}
    if feedback_form.is_valid() and request.method == "POST":
        text = feedback_form.cleaned_data.get("text")
        email = feedback_form.cleaned_data.get("mail")
        feedback_form.save(commit=True)
        send_mail(
            subject="Django feedback",
            message=text,
            from_email=settings.DJANGO_MAIL,
            recipient_list=[email],
        )
        messages.success(request, "Форма успешно отправлена")
        return redirect("feedback:feedback")

    return render(request, "feedback/feedback.html", context)
