from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver 
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
	CHOICES = (
        ('Librarian', 'Librarian'),
        ('Student', 'Student'),
        ('Admin', 'Admin'),
    )
	Role=models.CharField(max_length=20, 
		choices=CHOICES, 
		default='Student')
	profile_pic=models.ImageField(upload_to='profile-pic',
		default='profile-pic/user.jpg')
	barcode=models.ImageField(blank=True, null=True)
	contact=models.CharField(max_length=100)
	is_active=models.BooleanField(default=False)

	#def __str__(self):
		#return self.username
	


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

	#def __str__(self):
		#return self.student



@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Student.objects.create(student = instance)


'''@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
	instance.student.save()'''









