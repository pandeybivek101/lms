from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_init
from django.utils import timezone
import datetime
import pytz

class Catagory(models.Model):
	catagory = models.CharField(max_length=100)

	def __str__(self):
		return self.catagory

class AddBooks(models.Model):
	books_name=models.CharField(max_length=100)
	books_image=models.ImageField(upload_to='image')
	books_author_name=models.CharField(max_length=100)
	books_publication_name=models.CharField(max_length=100)
	books_purchase_date=models.DateTimeField(auto_now_add=True)
	books_price=models.PositiveIntegerField()
	books_quantity=models.PositiveIntegerField()
	available_quantity=models.PositiveIntegerField()
	barcode=models.ImageField(blank=True, null=True)
	catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE, null=True)
	added_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return self.books_name
	


class IssueBooks(models.Model):
	student=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	book=models.ForeignKey(AddBooks, on_delete=models.CASCADE)
	issued_date=models.DateTimeField(auto_now_add=True)
	return_date=models.DateTimeField()
	fine=models.IntegerField(default=0)
	issued_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='User', null=True)

	def __init__(self, *args ,**kwargs):
		super(IssueBooks ,self).__init__(*args, **kwargs)
		current_time=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
		if self.return_date:
		    if self.return_date < current_time:
		    	diff= current_time - self.return_date
		    	int_diff=int(diff.days)
		    	ratio=int_diff//30
		    	self.fine=ratio*200


class Ebooks(models.Model):
	name=models.CharField(max_length=100)
	book=models.FileField(upload_to='files')
	author_name=models.CharField(max_length=100)
	cover_image=models.ImageField(upload_to='image', blank=True, null=True)
	added_date=models.DateTimeField(auto_now_add=True, null=True)
	catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE, null=True)
	

class EbookRequest(models.Model):
	ebook=models.ForeignKey(Ebooks, on_delete=models.CASCADE)
	requested_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	requested_date=models.DateTimeField(auto_now_add=True)



class EbookRequestHistory(models.Model):
	ebook=models.ForeignKey(Ebooks, on_delete=models.CASCADE,blank=True, null=True)
	action=models.CharField(max_length=100)
	requested_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	requested_date=models.DateTimeField(auto_now_add=True, null=True)
	action_date=models.DateTimeField()
	readable_upto=models.DateTimeField(null=True)
	readable=models.BooleanField()
				

class Notice(models.Model):
	title=models.CharField(max_length=20)
	Description=models.TextField()
	Postedon=models.DateField(auto_now=True)

	def Summary(self):
		return self.Description[:10]

class NotifyMeModel(models.Model):
	student=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	book=models.ForeignKey(AddBooks, on_delete=models.CASCADE)
	req_date=models.DateTimeField(auto_now_add=True)