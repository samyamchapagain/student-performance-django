from django.conf import settings
from django.db import models


class Prediction(models.Model):
    """Stores a single student performance prediction made by a user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="predictions",
    )
    gender = models.CharField(max_length=20)
    ethnicity = models.CharField(max_length=20)
    parental_education = models.CharField(max_length=100)
    lunch = models.CharField(max_length=30)
    test_prep_course = models.CharField(max_length=30)
    math_score = models.IntegerField()
    reading_score = models.IntegerField()
    writing_score = models.IntegerField()
    predicted_grade = models.CharField(max_length=5)
    predicted_level = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.username} | math={self.math_score} reading={self.reading_score} "
            f"writing={self.writing_score} -> {self.predicted_grade} "
            f"({self.predicted_level})"
        )
