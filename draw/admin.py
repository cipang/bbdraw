from django.contrib import admin
from .models import Team, Slot


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "flag", "seq"]


def reset_chosen(model_admin, request, queryset):
    queryset.update(chosen=None)
reset_chosen.short_description = "Reset Selected Slots"


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ["key", "chosen"]
    actions = [reset_chosen]


admin.site.site_header = "Draw Control Panel"
admin.site.site_title = "Draw Control Panel"
