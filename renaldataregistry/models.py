from django.db import models

# Create your models here.
class HealthInstitution(models.Model):
    TYPE_CHOICES = (
        ("A", "Public"),
        ("P", "Private"),
        ("", "Select..."),
    )
    id = models.IntegerField(editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="",
        verbose_name="Institution type",
    )

    def __str__(self):
        return self.name
