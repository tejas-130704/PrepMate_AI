from django.contrib import admin
from .models import DSAQuestions

@admin.register(DSAQuestions)
class DSAQuestionsAdmin(admin.ModelAdmin):
    list_display = ("title", "domain", "level")  # Fields to display in the admin list view
    list_filter = ("domain", "level")  # Sidebar filters
    search_fields = ("title", "domain")  # Search bar for title and domain
    ordering = ("level",)  # Orders by difficulty level

