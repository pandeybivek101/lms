from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.conf import settings
from .models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def URegister(request):
	if request.method=="POST":
		form=UserRegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			Role=form.cleaned_data['Role']
			form.save()
			if Role == "Student":
			    return redirect('sinfo')
			else:
				return redirect('login')
	else:
		form=UserRegistrationForm()
	return render(request, 'account/uregistration.html', {'form':form})


def StudentInfo(request):
	if request.method=="POST":
		form1=StudentForm(request.POST)
		if form1.is_valid():
			data=form1.save(commit=False)
			data.student=User.objects.filter().latest('id')
			data.save()
			return redirect('login')
	else:
		form1=StudentForm()
	return render(request, 'account/sinfo.html', {'form1':form1})


def LoginView(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
	return render(request, 'account/login.html', {})

@login_required
def Logout(request):
    logout(request)      
    return redirect('login')