from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from .models import *
from django.utils import timezone
from django.contrib import auth
from .forms import *
from django.core.mail import send_mail
import io
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import os
from account.models import *
from django.contrib.auth import authenticate, login, logout
import datetime
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from account.models import User
from .decorators import role_required
import barcode
from barcode.writer import ImageWriter
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from PIL import Image
import PyPDF2
from django.core.files.base import ContentFile



# Create your views here.

def myissuedbook(request):
    issuedbooks=IssueBooks.objects.filter(student=request.user.id)
    return render(request, 'operations/myissuedbooks.html', {'issuedbooks':issuedbooks})


def ListEbooks(request):
    ebooks=Ebooks.objects.all()
    catagory=Catagory.objects.all()
    return render(request, 'operations/ebook-list.html', {'ebooks':ebooks, 'catagory':catagory})


@login_required
def Home(request):
    count_lst=[]
    cat_lst=[]
    for i in range(1, 13):
        issued_data=IssueBooks.objects.filter(issued_date__month=i)
        count=issued_data.count()
    return render(request,'operations/home.html', {'count_lst':count_lst})


@login_required    
@role_required(allowed_roles=['Librarian'])
def ListStd(request):
	stdrecord=User.objects.filter(Role='Student')
	return render(request, 'operations/liststd.html', {'stdrecord':stdrecord})


@login_required
@role_required(allowed_roles=['Librarian'])
def AddBook(request):
    if request.method=='POST':
        form=AddBooksForm(request.POST, request.FILES)
        if form.is_valid():
            books_quantity=form.cleaned_data['books_quantity']
            data=form.save(commit=False)
            data.available_quantity=books_quantity
            data.added_by=request.user
            data.save()
            return redirect('home')
    else:
        form=AddBooksForm()
    return render(request, 'operations/addbooks.html', {'form':form})
 

@login_required
def DisplayBooks(request):
    books=AddBooks.objects.all()
    catagory=Catagory.objects.all()
    context={
       'books':books,
       'catagory':catagory,
    }
    return render(request, 'operations/displaybooks.html', context)


@login_required
def ListNotices(request):
    notice=Notice.objects.all()
    return render(request, 'operations/notice-list.html',{'notice':notice})


@login_required
@role_required(allowed_roles=['Librarian'])
def LibRegistration(request):
    if request.method=='POST':
        form=LRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('main')
            except:
                pass
    else:
        form=LRegistrationForm()
        return render(request, 'registration.html', {'form':form})


class DeleteBook(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AddBooks
    template_name = 'operations/deletebooks.html'
    
    def get_success_url(self):
        return reverse_lazy("displaybooks")

    def test_func(self):
        if self.request.user.Role=='Librarian':
            return True
        else:
            return False


class EditBook(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AddBooks
    template_name = 'operations/updatebooks.html'
    form_class=AddBooksForm
    
    def get_success_url(self):
        return reverse_lazy("displaybooks")

    def test_func(self):
        if self.request.user.Role=='Librarian':
            return True
        else:
            return False


@login_required
@role_required(allowed_roles=['Librarian'])
def Notices(request):
    notices=Notice.objects.all().order_by('-pub_date')
    return render(request, 'operations/notice-list.html', {'notices':notices})


@login_required
@role_required(allowed_roles=['Librarian'])
def AddNotice(request):
    if request.method=='POST':
        form=NoticeForm(request.POST)
        if form.is_valid():
            try:
                data=form.save(commit=False)
                data.posted_by=request.user
                data.save()
                return redirect('home')
            except:
                pass
    else:
        form=NoticeForm()
        return render(request, 'operations/addnotice.html', {'form':form})


@login_required
@role_required(allowed_roles=['Librarian'])
def EditNotice(request, id):
    notice=Notice.objects.get(id=id)
    form=NoticeForm(request.POST or None, instance=notice)
    if form.is_valid():
        form.save()
        return redirect("listnotices")
    else:
        return render(request, 'operations/editnotice.html', {'form':form, 'notice':notice})


@login_required
@role_required(allowed_roles=['Librarian'])                
def DeleteNotice(request,id):
    notice=Notice.objects.get(id=id)
    notice.delete()
    return redirect("listnotices")


class DeleteStd(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'operations/deletestd.html'
    
    def get_success_url(self):
        return reverse_lazy("liststd")

    def test_func(self):
        if self.request.user.Role=='Librarian':
            return True
        else:
            return False



@login_required
@role_required(allowed_roles=['Librarian'])
def EditStudent(request, id):
    student=SRegistration.objects.get(id=id)
    form=form1(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect("liststd")
    else:
        return render(request,'SRegistration.html', {'student':student, 'form':form})


'''@login_required
@role_required(allowed_roles=['Librarian'])
def IssueBook(request):
    if request.method=="POST":
        stdid=request.POST['stdid']
        bkid=request.POST['bkid']
        studentinfo=User.objects.get(id=stdid)
        bookinfo=AddBooks.objects.get(id=bkid)
        return_date=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC) + datetime.timedelta(days=30)
        mdl=IssueBooks.objects.create(
                student=studentinfo,
                book=bookinfo,
                return_date=return_date,
                issued_by=request.user,
            )
        if bookinfo.available_quantity > 1:
            bookinfo.available_quantity=bookinfo.available_quantity-1
        else:
            bookinfo.available_quantity = 0
        mdl.save()
        bookinfo.save()
        return redirect('issuedbooks')
    return render(request, 'operations/issue_book.html', {})'''

@login_required
@role_required(allowed_roles=['Librarian'])
def IssueBook(request):
    if request.method=="POST":
        form=IssuebookForm(request.POST)
        if form.is_valid():
            stdid=form.cleaned_data['student']
            bkid=form.cleaned_data['book']
            studentinfo=User.objects.get(id=stdid)
            bookinfo=AddBooks.objects.get(id=bkid)
            return_date=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC) + datetime.timedelta(days=30)
            mdl=IssueBooks.objects.create(
                student=studentinfo,
                book=bookinfo,
                return_date=return_date,
                issued_by=request.user,
            )
            if bookinfo.available_quantity > 0:
                bookinfo.available_quantity=bookinfo.available_quantity-1
            else:
                bookinfo.available_quantity = 0
            mdl.save()
            bookinfo.save()
            return redirect('issuedbooks')
    else:
        form=IssuebookForm()
    return render(request, 'operations/issue_book.html', {
        'form':form,
        })



@login_required
@role_required(allowed_roles=['Librarian'])
def ReturnBooks(request, pk):
    rtnbook=IssueBooks.objects.get(pk=pk)
    rtnbook.returned=True
    rtnbook.returned_date=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    rtnbook.save()
    bookitem=AddBooks.objects.get(id=rtnbook.book.id)
    if bookitem.available_quantity < bookitem.books_quantity:
        bookitem.available_quantity=bookitem.available_quantity+1
        notify=NotifyMeModel.objects.filter(book=bookitem).first()
        '''if notify:
            send_mail(
                'for your request',
                'you have requested for book'+' '+notify.book.books_name+' '+'which is now available',
                'pandeyvivak25@gmail.com',
                [notify.student.email],
                fail_silently=False,
            )
            account_sid='AC53c1f5d6d5d4f8df9264e52dd8e951dd'
            account_token='29a8e10f4e096543a1f2517c0a3b1ad3'
            client=Client(account_sid, account_token)
            client.messages.create(
                to='9844700852',
                from_='+19252593370',
                body='hy'

                )
            notify.delete()'''
    else:
        bookitem.available_quantity=bookitem.books_quantity
    bookitem.save()
    return redirect('issuedbooks')
    return render(request, 'operations/return_book.html', 
        {'rtnbook':rtnbook}
        )




def IssuedBook(request):
    issueditems=IssueBooks.objects.filter(returned=False)
    return render(request, 
        'operations/issued_list.html', 
        {'issueditems':issueditems}
        )


def AddEbooks(request):
    if request.method == 'POST':
        form = EbooksForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list-ebooks')
    else:
        form = EbooksForm()
    return render(request, 'operations/addfiles.html', {
        'form': form,
    })


@login_required
@role_required(allowed_roles=['Librarian'])
def printBarCode(request, id):
    std=User.objects.get(id=id)
    if not std.barcode:
        ean = barcode.get('code128', id, writer=ImageWriter())
        filename = ean.save('std'+id)
        #new
        #f = open(settings.BASE_DIR+'\\'+"std"+id+".png", 'r')
        #filename = File(f)
        #print(filename)
        initial_path=settings.BASE_DIR+'\\'+"std"+id+".png"
        new_path=settings.BASE_DIR+'\\'+'media'+"\\"+"std"+id+".png"
        os.rename(initial_path, new_path)
        std.barcode=filename
        std.save()
    return redirect('liststd')



@login_required
def SearchBooks(request):
    query=request.GET.get('q')
    if query:
        result=Ebooks.objects.filter(Q(name__icontains = query) 
            | Q(author_name__icontains = query))
    else:
        result=[]
    print(query)
    return render(request, 'operations/ebooksearch.html', {'result':result})


@login_required
def EBookRequest(request, id):
    req=Ebooks.objects.get(id=id)
    data=EbookRequest.objects.get_or_create(ebook=req, requested_by=request.user)
    return redirect('list-ebooks')


@login_required
def ViewEbookRequest(request):
    requests=EbookRequest.objects.all()
    return render(request, 'operations/ebook-request.html', {'requests':requests})


@login_required
def View_Ebook_Request_allow(request, id):
    req=EbookRequest.objects.get(id=id)
    ebook_record=Ebooks.objects.get(id=req.ebook.id)
    history=EbookRequestHistory.objects.create(
        ebook=ebook_record, 
        action='Allowed', 
        requested_by=req.requested_by,
        requested_date=req.requested_date,
        action_date=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC),
        readable_upto=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC) + datetime.timedelta(days=7),
        readable=True
        )
    history.save()
    req.delete()
    return redirect('view-ebook-request')


@login_required
def View_Ebook_Request_deny(request, id):
    req=EbookRequest.objects.get(id=id)
    ebook_record=Ebooks.objects.get(id=req.ebook.id)
    history=EbookRequestHistory.objects.create(
        ebook=ebook_record, 
        action='Denied',
        requested_by=req.requested_by,
        requested_date=req.requested_date, 
        action_date=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC),
        readable_upto=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC) + datetime.timedelta(days=7),
        readable=False
        )
    history.save()
    req.delete()
    return redirect('view-ebook-request')



'''@login_required
def BookprintBarCode(request, id):
    ean = barcode.get('code128', id, writer=ImageWriter())
    filename = ean.save('book'+id)
    return redirect('displaybooks')'''


@login_required
def BookprintBarCode(request, id):
    book=AddBooks.objects.get(id=id)
    if not book.barcode:
        ean = barcode.get('code128', id, writer=ImageWriter())
        filename = ean.save('book'+id)
        #new
        #f = open(settings.BASE_DIR+'\\'+"std"+id+".png", 'r')
        #filename = File(f)
        #print(filename)
        initial_path=settings.BASE_DIR+'\\'+"book"+id+".png"
        new_path=settings.BASE_DIR+'\\'+'media'+"\\"+'book'+id+".png"
        os.rename(initial_path, new_path)
        book.barcode=filename
        book.save()
    return redirect('displaybooks')


@login_required
def View_my_readable_book(request):
    change=EbookRequestHistory.objects.filter(requested_by=request.user)
    for i in change:
        if i.readable_upto<datetime.datetime.utcnow().replace(tzinfo=pytz.UTC):
            i.readable=False
            i.save()
    readable_book=EbookRequestHistory.objects.filter(requested_by=request.user, readable=True)
    return render(request, 'operations/my-readable-book.html', {'readable_book':readable_book})


class EBookcatagorylist(ListView):
    model = Ebooks
    template_name = 'operations/ebook-list.html'
    context_object_name = 'ebooks'

    def get_queryset(self):
        catagory = get_object_or_404(Catagory, catagory=self.kwargs.get('catagory'))
        return Ebooks.objects.filter(catagory = catagory)


class Bookcatagorylist(ListView):
    model = AddBooks
    template_name = 'operations/displaybooks.html'
    context_object_name = 'books'

    def get_queryset(self):
        catagory = get_object_or_404(Catagory, catagory=self.kwargs.get('catagory'))
        return AddBooks.objects.filter(catagory = catagory)


class DeleteEBooks(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ebooks
    template_name = 'operations/delete-ebooks.html'
    
    def get_success_url(self):
        return reverse_lazy("list-ebooks")

    def test_func(self):
        if self.request.user.Role=='Librarian':
            return True
        else:
            return False


class EditEbooks(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ebooks
    form_class = EbooksForm
    template_name = "operations/ebook-update.html"

    def get_success_url(self):
        return reverse_lazy("list-ebooks")

    def test_func(self):
        if self.request.user.Role=='Librarian':
            return True
        else:
            return False


"""def ReadEbook(request, pk):
    ebook=Ebooks.objects.get(id=pk)
    pdfFileObj = open(ebook.book.path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    for page in range(pdfReader.numPages):
       pageObj = pdfReader.getPage(page) 
       pageObj.extractText()
       

    pdfWriter = PyPDF2.PdfFileWriter() 
        for page in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(page) 
            pageObj.rotateClockwise(270)
            pdfWriter.addPage(pageObj)

            pdfWriter.write('rotated_example.pdf')
            pdfFileObj.close() 
            newFile.close()"""

@login_required
def NotifyMe(request, id):
    book=AddBooks.objects.get(id=id)
    NotifyMeModel.objects.get_or_create(student=request.user,
        book=book)
    return redirect('displaybooks')

class StdDetail(LoginRequiredMixin, DetailView):
    template_name='operations/std-detail.html'
    model=User
    context_object_name='std'

class DetailBook(LoginRequiredMixin, DetailView):
    template_name='operations/book-detail.html'
    model=AddBooks
    context_object_name='book'

class DetailEBook(LoginRequiredMixin, DetailView):
    template_name='operations/ebook-detail.html'
    model=Ebooks
    context_object_name='ebook'










