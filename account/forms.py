from django import forms
from .models import *
from account.models import User
from django.contrib.auth.forms import UserCreationForm

'''class UserRegistrationForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['username', 
		'email',
		'password',
		'first_name',
		'last_name',
		'Role',
		'profile_pic',
		'contact'
		]'''

class UserRegistrationForm(UserCreationForm):
	class Meta:
		model=User
		fields=[
		'username', 
		'email',
		'password',
		'first_name',
		'last_name',
		'Role',
		'profile_pic',
		'contact'
		]
		exclude=('password',)
		

class StudentForm(forms.ModelForm):
	class Meta:
		model=Student
		fields=['Enrollment', 'year']