from django import forms
from .models import *
from account.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
	'''username=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Username'}), 
	required=True, max_length=30)
	Email=forms.CharField(widget=forms.EmailInput(
		attrs={"class":"form-control", "placeholder":"Enter Email"}), 
	required=True)
	password=forms.CharField(widget=forms.PasswordInput(
		attrs={"class":"form-control", "placeholder":"Enter Password"}), 
	required=True)
	First_Name=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter First Name'}), 
	required=True, max_length=30)
	Last_Name=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Last Name'}), 
	required=True, max_length=30)
	#Role=forms.CharField(widget=forms.ChoiceInput(
		#attrs={'class':'form-control'}), 
	#required=True, max_length=30)
	Profile_Pic=forms.ImageField(widget=forms.FileInput(
		attrs={'class':'form-control'}), 
	required=True, max_length=30)
	Contact=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Contact Number'}), 
	required=True, max_length=30)'''

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

class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Username'}), 
	required=True, max_length=30)
	password=forms.CharField(widget=forms.PasswordInput(
		attrs={"class":"form-control", "placeholder":"Enter Password"}), 
	required=True)
	class Meta:
		model=User
		fields=['username', 'password']