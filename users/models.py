from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Учень'),
        ('teacher', 'Вчитель'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)

    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        blank=True,
        null=True
    )

    def is_teacher(self):
        return self.role == 'teacher' or self.is_superuser

    def is_student(self):
        return self.role == 'student'

    def __str__(self):
        return self.username