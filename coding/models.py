from django.db import models

class DSAQuestions(models.Model):
    title = models.CharField(max_length=100)
    domain = models.CharField(max_length=50)
    level_choices = [
        ("Hard", "Hard"),
        ("Medium", "Medium"),
        ("Easy", "Easy")
    ]
    level = models.CharField(max_length=10, choices=level_choices)
    problem_statement = models.TextField()
    test_cases = models.JSONField()
    solution = models.TextField()
    subdomain = models.JSONField()  # Store selected checkboxes as a JSON list

    def __str__(self):
        return f"{self.title} ({self.level}) - {self.domain}"
