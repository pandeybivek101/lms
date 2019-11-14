from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.conf import settings
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


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
			if request.user.is_authenticated:
				return redirect('home')
			return redirect('login')
	else:
		form1=StudentForm()
	return render(request, 'account/sinfo.html', {'form1':form1})


def LoginView(request):
	if request.method=="POST":
		form=LoginForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user=authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				if request.user.Role == "Student":
					if not Student.objects.filter(student=request.user).exists():
						return redirect('sinfo')
				return redirect('home')
			else:
				messages.error(request, 'Invalid Username or password')
	else:
		form=LoginForm()
	return render(request, 'account/login.html', {'form':form})


@login_required
def Logout(request):
    logout(request)     
    return redirect('login')

@login_required
def Profile(request):
    profile=User.objects.get(id=request.user.id)
    std=Student.objects.filter(student=profile).first()
    return render(request, 'account/profile.html', 
        {'profile':profile,
        'std':std
        }
)


@login_required
def ChangeProfile(request):
	if request.user.Role=='Student':
		if request.method == 'POST':
			form1 = UserUpdateForm(request.POST, request.FILES, instance=request.user)
			form2=StudentForm(request.POST, instance=request.user.student)
			if form1.is_valid() and form2.is_valid():
				form1.save()
				form2.save()
				return redirect('profile')

		else:
			form1 = UserUpdateForm(instance=request.user)
			form2=StudentForm(instance=request.user.student)
		return render(request, 'account/change-profile.html', 
			{'form1': form1,
			'form2':form2
			})
	else:
		if request.method == 'POST':
			form1 = UserUpdateForm(request.POST, request.FILES, instance=request.user)
			if form1.is_valid():
				form1.save()
				return redirect('profile')
		else:
			form1 = UserUpdateForm(instance=request.user)
		return render(request, 'account/change-profile.html', 
			{'form1': form1,
			})



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })
