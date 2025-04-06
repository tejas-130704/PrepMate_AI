from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

class JobPost(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.title} at {self.company.name}"
    

class Interview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interviews")
    interview_date = models.DateTimeField(default=timezone.now)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="interviews")
    conversation = models.TextField(blank=True, null=True)
    ai_analysis = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview on {self.interview_date} for {self.job.title} at {self.job.company.name}"