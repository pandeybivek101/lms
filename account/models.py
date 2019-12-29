from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
	CHOICES = (
        ('Librarian', 'Librarian'),
        ('Student', 'Student'),
    )
	Role=models.CharField(max_length=20, 
		choices=CHOICES, 
		default='Student')
	profile_pic=models.ImageField(upload_to='profile-pic',
		default='profile-pic/user.jpg')
	barcode=models.ImageField(blank=True, null=True)
	contact=models.CharField(max_length=100)
	is_active=models.BooleanField(default=False)


class StudentModel(models.Model):
	first_name=models.CharField(max_length=100)
	middle_name=models.CharField(max_length=100, blank=True, null=True)
	last_name=models.CharField(max_length=100)
	email=models.EmailField()
	contact=models.CharField(max_length=15)
	gender=(
		('Male', 'Male'),
		('Female', 'Female'),
		)
	gender=models.CharField(max_length=100, choices=gender)
	DOB=models.DateField()
	Faculty=models.CharField(max_length=100)
	year=models.CharField(max_length=100)
	Course=models.CharField(max_length=100)
	section=models.CharField(max_length=100)
	barcode=models.ImageField(blank=True, null=True)
	student=models.OneToOneField(settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		blank=True,
		null=True)

	def __str__(self):
		return self.first_name
	


class Student(models.Model):
	C_CHOICES = (
		('Management', 'Management'),
		('Science', 'Science'),
		('Humanities', 'Humanities'),
		('Edcation', 'Education'),)
	year = (
		('First', 'First'),
		('Second', 'Second'),
		('Third', 'Third'),
		('Fourth', 'Fourth'),)
	Enrollment=models.CharField(max_length=20, choices=C_CHOICES)
	year=models.CharField(max_length=20, choices=year)
	student=models.OneToOneField(settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, null=True)
	