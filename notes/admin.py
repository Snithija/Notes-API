from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "created_at", "updated_at")
    search_fields = ("title", "content", "user__username", "user__email")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)


admin.site.register(Note, NoteAdmin)