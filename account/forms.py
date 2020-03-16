from django import forms
from .models import *
from account.models import User
from django.contrib.auth.forms import UserCreationForm
 
	
class UserRegistrationForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['first_name', 
		'last_name', 
		'email', 
		'contact', 
		'profile_pic']

	def clean_email(self):
		return validate_email(self)

	def clean_contact(self):
		return validate_contact(self)

class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 
		'placeholder':'Enter your Username or Email',
		'id':'username'
		}), 
	required=True, max_length=30)
	password=forms.CharField(widget=forms.PasswordInput(
		attrs={"class":"form-control",
		 "placeholder":"Enter Password",
		 'id':'password',
		 }), 
	required=True)
	class Meta:
		model=User
		fields=['username', 'password']


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model=User
		fields=[ 
		'email',
		'first_name',
		'last_name',
		'profile_pic',
		'contact'
		]
	def clean_email(self):
		return validate_email(self)

	def clean_contact(self):
		return validate_contact(self)

class StudentForm(forms.ModelForm):
	class Meta:
		model=Student
		fields=['year', 'faculty', 'course']

class SupUserRegistrationForm(UserCreationForm):
	class Meta:
		model=User
		fields=[
		'username', 
		'email',
		'password1',
		'password2',
		'contact',
		]
		exclude=('password',)

	def clean_contact(self):
		return validate_contact(self)


class StdLibProfileForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['profile_pic', 'username']
		

def validate_contact(self):
	contact=self.cleaned_data['contact']
	str_contact=str(contact)
	usr=User.objects.filter(contact=contact)
	if usr.exists():
		usr_check=usr.first()
		if usr_check.id==self.instance.pk:
			return contact
		else:
		    raise forms.ValidationError('Contact Already Taken')
	elif contact.isalpha():
		raise forms.ValidationError('Contact cannot be Alphabet')
	elif len(str_contact) != 10:
		raise forms.ValidationError('Contact must be of 10 characters')
	elif str_contact[:2] != "98":
		raise forms.ValidationError('Contact numbers must starts with 98')
	else:
		return contact


def validate_email(self):
	email=self.cleaned_data['email']
	usr=User.objects.filter(email=email)
	if usr.exists():
		usr_check=usr.first()
		if usr_check.id==self.instance.pk:
			return email
		else:
		    raise forms.ValidationError('Email Already Taken')
	else:
		return email