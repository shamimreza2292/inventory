from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    ROLE_ADMIN = 'Admin'
    ROLE_MANAGER = 'Manager'
    ROLE_STAFF = 'Staff'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_STAFF, 'Staff'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_STAFF)

    branch = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.full_name or self.username
