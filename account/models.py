from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
	CHOICES = (
        ('Librarian', 'Librarian'),
        ('Student', 'Student'),
    )
	Role=models.CharField(max_length=20, choices=CHOICES, default='Student')
	profile_pic=models.ImageField(upload_to='profile-pic')
	barcode=models.ImageField(blank=True, null=True)
	contact=models.CharField(max_length=100)
	


class Student(models.Model):
	C_CHOICES = (
		('Management', 'Management'),
		('Science', 'Science'),
		('Humanities', 'Humanities'),
		('Edcation', 'Education'),

		)
	year = (
		('First', 'First'),
		('Second', 'Second'),
		('Third', 'Third'),
		('Fourth', 'Fourth'),

		)
	Enrollment=models.CharField(max_length=20, choices=C_CHOICES)
	year=models.CharField(max_length=20, choices=year)
	student=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)