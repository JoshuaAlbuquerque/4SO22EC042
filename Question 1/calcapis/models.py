from django.db import models

class NumberStorage(models.Model):
    number = models.IntegerField(unique=True)  # Ensure uniqueness
    created_at = models.DateTimeField(auto_now_add=True)  # Track insertion time

    def __str__(self):
        return str(self.number)