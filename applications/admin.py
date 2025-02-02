from django.contrib import admin

from .models import Application, ApplicationGroup, ApplicationPeriod


@admin.register(ApplicationGroup, ApplicationPeriod)
class BaseApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
    ]


class ApplicationGroupChoiceInline(admin.TabularInline):
    model = Application.group_choice.through
    ordering = ["priority"]
    extra = 0

    class Media:
        css = {"all": ("applications/css/hide_admin_original.css",)}


@admin.register(Application)
class ApplicationAdmin(BaseApplicationAdmin):
    inlines = [ApplicationGroupChoiceInline]
