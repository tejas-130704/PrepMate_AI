from django.contrib import admin
from .models import Company, JobPost, Interview

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')  # Display these fields in the list view
    search_fields = ('name',)  # Enable search by company name

class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company')  # Show job title and company in the list view
    list_filter = ('company',)  # Add a filter by company
    search_fields = ('title',)  # Enable search by job title

class InterviewData(admin.ModelAdmin):
    list_display = ('user', 'interview_date', 'job')

    
    
admin.site.register(Interview,InterviewData)
admin.site.register(Company, CompanyAdmin)
admin.site.register(JobPost, JobPostAdmin)