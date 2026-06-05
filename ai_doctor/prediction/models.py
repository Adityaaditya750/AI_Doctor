from django.db import models
from django.contrib.auth.models import User


class Prediction(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    disease = models.CharField(
        max_length=200
    )

    confidence = models.IntegerField()

    symptoms = models.TextField()

    report = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.disease