import django.views


__all__ = []


class AboutView(django.views.generic.TemplateView):
    template_name = "about/description.html"
