from django import forms
from .models import *
from django.http import HttpResponseRedirect
from account.models import User


class NoticeForm(forms.ModelForm):
	title=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Title'}), required=True, max_length=30)
	Description=forms.CharField(widget=forms.Textarea(
		attrs={"class":"form-control", "placeholder":"Enter Description"}), required=True)
	class Meta:
		model=Notice
		fields=['title', 'Description']

	
	def summary(self):
		return self.Description[:100]

	
	def clean_title(self):
		title=self.cleaned_data['title']
		if not title[0].isupper() and title[0].isdigit():
			raise forms.ValidationError('First character must be capital')
		elif len(title)>20:
			raise forms.ValidationError('Only 20 characters are alloweded')
		else:
			return title



class AddBooksForm(forms.ModelForm):
	books_name=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Bookname'}), required=True, max_length=20)
	books_image=forms.ImageField(widget=forms.FileInput(
		attrs={'class':'form-control'}), required=True)
	books_author_name=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Authorname'}), required=True, max_length=20)
	books_publication_name=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Authorname'}), required=True, max_length=20)
	books_price=forms.CharField(widget=forms.NumberInput(
		attrs={'class':'form-control', 'placeholder':'Enter Price'}), required=True)
	books_quantity=forms.IntegerField(widget=forms.NumberInput(
		attrs={'class':'form-control', 'placeholder':'Enter quantity'}), required=True)

	class Meta:
		model=AddBooks
		fields=[
			'books_name',
			'books_image',
			'books_author_name',
			'books_publication_name',
			'books_price',
			'books_quantity',
			]

	def clean_books_price(self):
		books_price=self.cleaned_data['books_price']
		if books_price.isalpha():
			raise forms.ValidationError('Price cannot be alphabet')
		elif int(books_price) <= 0:
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


	def clean_student(self):
		std_id=self.cleaned_data['student']
		std_qs=User.objects.filter(id=std_id)
		if std_qs.exists():
			return std_id
		else:
		    raise forms.ValidationError('Student with this id doesnot exists')

	def clean_book(self):
		book_id=self.cleaned_data['book']
		book_obj=AddBooks.objects.filter(id=book_id) 
		if book_obj.exists():
			return book_id	
		else:
			raise forms.ValidationError('Book with this id doesnot exists')
			



class EbooksForm(forms.ModelForm):
	name=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Book Name', 'autofocus':'autofocus'}), required=True, max_length=20)
	book=forms.CharField(widget=forms.FileInput(
		attrs={'name':'myfile' ,'class':'form-control'}), required=True, max_length=20)
	author_name=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'placeholder':'Enter Author Name', 'autofocus':'autofocus'}), required=True, max_length=20)
	cover_image=forms.ImageField(widget=forms.FileInput(
		attrs={'class':'form-control'}), required=False)
	class Meta:
		model=Ebooks
		fields=['name', 'book', 'cover_image', 'author_name']