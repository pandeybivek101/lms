from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.conf import settings
from account.models import User
from django.shortcuts import redirect

def role_required(allowed_roles=[]):
	def decorator(func):
		def wrap(request, *args, **kwargs):
			if request.user.Role in allowed_roles:
				return func(request, *args, **kwargs)
			else:
				raise PermissionDenied
		return wrap
	return decorator
