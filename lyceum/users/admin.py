from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

import users.models


class ProfileInLine(admin.StackedInline):
    model = users.models.Profile
    can_delete = False
    fields = [
        users.models.Profile.birthday.field.name,
        users.models.Profile.bio.field.name,
        users.models.Profile.image.field.name,
    ]
    readonly_fields = (users.models.Profile.coffe_count.field.name,)


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)



