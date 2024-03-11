from django.contrib import admin

import feedback.models

__all__ = []


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.status.field.name,
    )
    readonly_fields = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.text.field.name,
    )
    list_editable = (feedback.models.Feedback.status.field.name,)

    def save_model(self, request, obj, form, change):
        field = feedback.models.Feedback.status.field.name
        if field in form.changed_data:
            feedback.models.StatusLog(
                user=request.user,
                feedback=obj,
                _from=form.initial["status"],
                to=form.cleaned_data["status"],
            ).save()

        super().save_model(request, obj, form, change)


@admin.register(feedback.models.StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog._from.field.name,
        feedback.models.StatusLog.to.field.name,
    )
    readonly_fields = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog._from.field.name,
        feedback.models.StatusLog.to.field.name,
        feedback.models.StatusLog.feedback.field.name,
    )
