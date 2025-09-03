from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------
# Custom User Model
# -----------------------------
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.full_name if self.full_name else self.username


# -----------------------------
# Student Model
# -----------------------------
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
   # age = models.IntegerField(blank=True, null=True)  # optional field
    station = models.CharField(max_length=150, blank=True)
    def __str__(self):
        return self.full_name


# -----------------------------
# Travel / Concession Application
# -----------------------------
class ConcessionApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_type = models.CharField(max_length=50)
    period = models.CharField(max_length=50)
    line = models.CharField(max_length=50)
    from_station = models.CharField(max_length=100)
    to_station = models.CharField(max_length=100)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.class_type} ({self.from_station} to {self.to_station})"
