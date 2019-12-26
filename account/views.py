from django.shortcuts import render, redirect, HttpResponseRedirect,HttpResponse
from .forms import *
from .models import *
from operations.models import *
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from account.models import User
from django.core.mail import EmailMessage


# Create your views here.

def URegister(request):
	if request.method=="POST":
		form=UserRegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			Role=form.cleaned_data['Role']
			email=form.cleaned_data['email']
			user=form.save(commit=False)
			user.is_active = False
			user.save()
			sendemail(request, user, email)
			if Role == "Student":
			    return redirect('sinfo')
			return render(request, 'account/user_confirmation.html')
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
			elif not request.user.is_active:
			    return render(request, 'account/user_confirmation.html')
			else:
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
			if user is not None and user.is_active==True:
				login(request, user)
				if not request.POST.get('rememberme'):
					request.session.set_expiry(0)
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
    issued_by=IssueBooks.objects.filter(issued_by=profile, returned=False)
    my_book=IssueBooks.objects.filter(student=profile, returned=False)
    notify=NotifyMeModel.objects.filter(student=profile)
    ebook_pending=EbookRequest.objects.filter(requested_by=request.user)
    ebook_rec=EbookRequestHistory.objects.filter(requested_by=request.user, 
    	readable=False)
    ebook_read=EbookRequestHistory.objects.filter(requested_by=request.user, 
    	readable=True)
    return render(request, 'account/profile.html', 
        {'profile':profile,
        'std':std,
        'issued_by':issued_by,
        'my_book':my_book,
        'notify':notify,
        'ebook_pending':ebook_pending,
        'ebook_rec':ebook_rec,
        'ebook_read':ebook_read,
        }
)


@login_required
def ChangeProfile(request):
	if request.user.Role=='Student':
		if request.method == 'POST':
			form1 = UserUpdateForm(request.POST, request.FILES, 
				instance=request.user)
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
			form1 = UserUpdateForm(request.POST, 
				request.FILES, instance=request.user)
			if form1.is_valid():
				form1.save()
				return redirect('profile')
		else:
			form1 = UserUpdateForm(instance=request.user)
		return render(request, 'account/change-profile.html', 
			{'form1': form1,
			})


@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			return redirect('profile')

	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'account/change_password.html', 
		{
		'form': form,
		})


def Supuser(request):
	if request.method=="POST":
		form=SupUserRegistrationForm(request.POST)
		if form.is_valid():
			email=form.cleaned_data['email']
			user=form.save(commit=False)
			user.Role='Librarian'
			user.is_active=False
			user.is_superuser=True
			user.is_staff=True
			user.save()
			sendemail(request, user, email)
			return render(request, 'account/user_confirmation.html')
	else:
		form=SupUserRegistrationForm()
	context={"form":form}
	return render(request, 
		'account/superusercreation.html', 
		context)


def sendemail(request, user, email):
	current_site = get_current_site(request)
	mail_subject = 'Activate your blog account.'
	message = render_to_string('account/acc_active_email.html', {
		'user': user,
		'domain': current_site.domain,
		'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
		'token':account_activation_token.make_token(user),
		})
	to_email = email
	email = EmailMessage(
		mail_subject, message, to=[to_email]
		)
	email.send()



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'account/activation_success.html')
    else:
        return render(request, 'account/invalid.html')
