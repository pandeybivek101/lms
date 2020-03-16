from django import forms
from .models import *
from django.http import HttpResponseRedirect
from account.models import User
from django.core.validators import FileExtensionValidator


class MessageForm(forms.ModelForm):
	title=forms.CharField(widget=forms.TextInput(
		attrs={
		'class':'form-control', 
		'placeholder':'Enter Title',
		}), required=True, max_length=120)
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

	def clean_books_name(self):
		books_name=self.cleaned_data['books_name']
		bookname=AddBooks.objects.filter(books_name=books_name)
		if bookname.exists():
			bk_name=bookname.first()
			if bk_name.id==self.instance.pk:
				return books_name.title()
			else:
			    raise forms.ValidationError('Book Name already exists')
		else:
			return books_name.title()

	def clean_books_price(self):
		return validate_quantity(self.cleaned_data['books_price'])

	def clean_books_quantity(self):
		return validate_quantity(self.cleaned_data['books_quantity'])

	def clean_cover_image(self):
		img=self.cleaned_data['books_image']
		if img.name.endswith('.png') or img.name.endswith('.jpeg') or img.name.endswith('.jpeg'):
			return img
		else:
			raise forms.ValidationError('only png, jpeg, gif format supported')

	

class IssuebookForm(forms.ModelForm):
	student=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control',
		 'placeholder':'Enter Student Id',
		 'autofocus':'autofocus',
		 'id':'std'
		 }), 
	required=True, max_length=20)
	book=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control' ,
		'placeholder':'Enter Book Id', 
		'autofocus':'autofocus',
		'id':'bk'
		}), required=True, max_length=20)

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

		try:
		    std_qs=User.objects.filter(id=std_id)
		except(ValueError):
			raise forms.ValidationError('Student Id arenot in alphabets')

		if not std_qs.exists():
			raise forms.ValidationError('Student with this Id doesnot exists')
		else:
			sets=AdminSettings.objects.first()
			iss_record=IssueBooks.objects.filter(student=std_qs.first(), 
				returned=False)
			iss_fine=IssueBooks.objects.filter(student=std_qs.first(), 
				returned=False, fine__gt=0)
			if iss_record.exists():
				if sets:
					available_quota=sets.book_allowed
				else:
					available_quota=2
				if iss_record.count()>=available_quota:
					raise forms.ValidationError("Maximum issue quota exceeded")
				if iss_fine.exists():
					raise forms.ValidationError('Student Has a Fine Amount to pay')
				else:
					return std_id
			else:
			    return std_id


	def clean_book(self):
		book_id=self.cleaned_data['book']

		try:
		    book_obj=AddBooks.objects.filter(id=book_id)
		except(ValueError):
			raise forms.ValidationError('Book Id arenot in alphabets')

		if book_id.isalpha():
			raise forms.ValidationError('Id arenot in alphabets')
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


	def clean_name(self):
		name=self.cleaned_data['name']
		name_query=Ebooks.objects.filter(name=name)
		if name==None:
			raise forms.ValidationError('Cannot be empty')
		if name_query.exists():
			name_check=name_query.first()
			if name_check.id==self.instance.pk:
				return name
			else:
			    raise forms.ValidationError("Name of Ebook already Exists")
		else:
			return name



	def clean_book(self):
		book=self.cleaned_data['book']
		if book.name.endswith('.pdf') or book.name.endswith('.pdf'):
			return book
		else:
			raise forms.ValidationError('only pdf or epub format supported')


class AddCatagoryForm(forms.ModelForm):
	class Meta:
		model=Catagory
		fields=['catagory']
		

	def clean_catagory(self):
		catagory=self.cleaned_data['catagory']
		catagory_query=Catagory.objects.filter(catagory=catagory)
		if catagory_query.exists():
			catagory_check=catagory_query.first()
			if catagory_check.id==self.instance.pk:
				return catagory.title()
			else:
			    raise forms.ValidationError('Catagory name aalready exists')
		else:
			return catagory.title()


class ReserveForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['email', 'contact']

def validate_quantity(data):
		if data<=0:
			raise forms.ValidationError('Cannot be smaller then 1')
		else:
			return data

class SettingForm(forms.ModelForm):
	class Meta:
		model=AdminSettings
		fields=['book_allowed', 'issue_days', 'ebook_allowed_days', 'fine_amount']


	def clean_book_allowed(self):
		return validate_quantity(self.cleaned_data['book_allowed'])	

	def clean_issue_days(self):
		return validate_quantity(self.cleaned_data['issue_days'])

	def clean_ebook_allowed_days(self):
		return validate_quantity(self.cleaned_data['ebook_allowed_days'])

	def clean_fine_amount(self):
		return validate_quantity(self.cleaned_data['fine_amount'])


			

		



			








		
