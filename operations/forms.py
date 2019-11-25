from django import forms
from .models import *
from django.http import HttpResponseRedirect
from account.models import User


class MessageForm(forms.ModelForm):
	title=forms.CharField(widget=forms.TextInput(
		attrs={
		'class':'form-control', 
		'placeholder':'Enter Title',
		}), required=True, max_length=30)
	Description=forms.CharField(widget=forms.Textarea(
		attrs={
		"class":"form-control", 
		'rows':3,
		'placeholder':"Post a new message"

		}), required=True)
	class Meta:
		model=Message
		fields=['title', 'Description']



class AddBooksForm(forms.ModelForm):

	class Meta:
		model=AddBooks
		fields=[
			'books_name',
			'books_image',
			'books_author_name',
			'books_publication_name',
			'books_price',
			'books_quantity',
			'catagory'
			]

	def clean_books_price(self):
		books_price=self.cleaned_data['books_price']
		if books_price <= 0:
			raise forms.ValidationError('price cannot be smaller then 0')
		else:
			return books_price

	def clean_books_quantity(self):
		books_quantity=self.cleaned_data['books_quantity']
		if books_quantity <= 0:
			raise forms.ValidationError('Quantity cannot be smaller then 0')
		else:
			return books_quantity
	

class IssuebookForm(forms.ModelForm):
	student=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Student Id','autofocus':'autofocus'}), required=True, max_length=20)
	book=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control' ,'placeholder':'Enter Book Id', 'autofocus':'autofocus'}), required=True, max_length=20)

	class Meta:
		model=Ebooks
		fields=['student', 'book']

	def clean(self):
		cleaned_data = super().clean()
		std_id = cleaned_data.get('student')
		bk_id = cleaned_data.get('book')
		iss=IssueBooks.objects.filter(student=std_id, 
			returned=False,
			book=bk_id)
		if iss.exists():
			raise forms.ValidationError('This book is already assigned to designated student')
		return cleaned_data

	def clean_student(self):
		std_id=self.cleaned_data['student']
		std_qs=User.objects.filter(id=std_id)
		if not std_qs.exists():
			raise forms.ValidationError('Student with this Id doesnot exists')
		else:
			iss_record=IssueBooks.objects.filter(student=std_qs.first(), returned=False)
			iss_fine=IssueBooks.objects.filter(student=std_qs.first(), returned=False, fine__gt=0)
			if iss_record.exists():
				if iss_record.count()>=2:
					raise forms.ValidationError("Already Issued Two books")
				if iss_fine.exists():
					raise forms.ValidationError('Student Has a Fine Amount to pay')
				else:
					return std_id
			else:
			    return std_id

	def clean_book(self):
		book_id=self.cleaned_data['book']
		book_obj=AddBooks.objects.filter(id=book_id)
		if not book_obj.exists():
			raise forms.ValidationError('Book with this id doesnot exists')
		elif book_obj.first().available_quantity<1:
			raise forms.ValidationError('This Book is currently unavailable')
		else:
			return book_id

	
class EbooksForm(forms.ModelForm):
	class Meta:
		model=Ebooks
		fields=['name', 'book', 'cover_image', 'author_name', 'catagory']
