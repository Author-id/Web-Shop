from django import forms

from rating.models import Rating


__all__ = []


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [
            model.rating.field.name,
        ]

        widgets = {
            model.rating.field.name: forms.NumberInput(
                attrs={"class": "rating-input"}
            )
        }


class BaseForm(forms.Form):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if isinstance(field.field.widget, forms.CheckboxInput):
                field.field.widget.attrs["class"] = "form-check-input"
            else:
                field.field.widget.attrs["class"] = "form-control"


class DeleteRatingForm(BaseForm):
    delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)
