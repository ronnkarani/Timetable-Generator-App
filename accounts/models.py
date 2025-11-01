from django.contrib.auth.models import AbstractUser
from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')

    def __str__(self):
        return self.username
