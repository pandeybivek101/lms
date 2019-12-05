from django.http import HttpResponse, HttpResponseRedirect
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
from django.db.models import Q
from django.core.files.base import ContentFile
from account.models import Student
from django.core.paginator import Paginator
from django.views import View
import shutil
from django.core.exceptions import ObjectDoesNotExist
from twilio.rest import Client
from twilio.rest import TwilioRestClient



# Create your views here.


@login_required
def Home(request):
    return render(request,'operations/home.html')

    
@login_required
@role_required(allowed_roles=['Librarian'])
def Scan(request):
    return render(request, 'operations/quagga.html',{})

@login_required
@role_required(allowed_roles=['Student'])
def myissuedbook(request):
    issuedbooks=IssueBooks.objects.filter(student=request.user.id,
        returned=False)
    return render(request, 
        'operations/myissuedbooks.html', 
        {'issuedbooks':issuedbooks})


@login_required
@role_required(allowed_roles=['Student'])
def DirectView(request, id):
    msg_detail=Message.objects.get(id=id)
    msg_detail.read=True
    msg_detail.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ListEbooks(LoginRequiredMixin, ListView):
    template_name='operations/ebook-list.html'
    queryset=Ebooks.objects.all()

    def get_context_data(self, *args, **kwargs):
        context=super(ListEbooks,self).get_context_data(*args, **kwargs)
        ebooks=self.queryset
        catagory=Catagory.objects.all()
        req_list=[]
        ebook_req=EbookRequest.objects.filter(requested_by=self.request.user)
        readable=EbookRequestHistory.objects.filter(requested_by=self.request.user, readable=True)
        for i in readable:
            req_list.append(i.ebook.id)
        for i in ebook_req:
            req_list.append(i.ebook.id)
        context.update({
            'ebooks':ebooks,
            'catagory':catagory,
            'req_list':req_list,
            })
        return context



class ListStd(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name='operations/liststd.html'
    queryset=User.objects.filter(Role='Student')
    context_object_name='stdrecord'

    def test_func(self):
        if  self.request.user.Role=='Librarian':
            return True
        else:
            return False


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
            return redirect('displaybooks')
    else:
        form=AddBooksForm()
    return render(request, 'operations/addbooks.html', {'form':form})
 

class DisplayBooks(LoginRequiredMixin, ListView):
    template_name='operations/displaybooks.html'
    queryset=AddBooks.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(DisplayBooks, self).get_context_data(*args, 
            **kwargs)
        books=self.queryset
        noti_lst=[]
        noti_req=NotifyMeModel.objects.filter(
            student=self.request.user
            )
        iss_qs=IssueBooks.objects.filter(
            student=self.request.user, returned=False
            )
        for i in noti_req:
            noti_lst.append(i.book.id)
        for i in iss_qs:
            noti_lst.append(i.book.id)
        catagory=Catagory.objects.all()
        context.update({
            'books':books,
            'catagory':catagory,
            'noti_lst':noti_lst
            })
        return context



class DeleteBook(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AddBooks
    template_name = 'operations/deletebooks.html'
    
    def get_success_url(self):
        return reverse_lazy("displaybooks")

    def test_func(self):
        if  self.request.user.Role=='Librarian':
            return True
        else:
            return False


class EditBook(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AddBooks
    template_name = 'operations/updatebooks.html'
    form_class=AddBooksForm


    def form_valid(self, form):
        book=AddBooks.objects.get(pk=self.kwargs.get('pk'))
        issued=IssueBooks.objects.filter(book=book, 
            returned=False).count()
        form.instance.added_by = self.request.user
        form.instance.available_quantity=form.instance.books_quantity-issued
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("displaybooks")

    def test_func(self):
        if  self.request.user.Role=='Librarian':
            return True
        else:
            return False



def Messagestd(request, id):
    msg_std=User.objects.get(id=id)
    if request.method=='POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            msg=form.save(commit=False)
            msg.posted_to=msg_std
            msg.posted_by=request.user
            msg.save()
            return redirect("/liststd/{}/detail".format(id))
    else:
        form=MessageForm()
    return render(request, 'operations/addmessage.html', {
        'form':form,
        'msg_std':msg_std,
        })




class DeleteStd(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'operations/deletestd.html'
    
    def get_success_url(self):
        return reverse_lazy("liststd")

    def test_func(self):
        if  self.request.user.Role=='Librarian':
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
        return render(request,'SRegistration.html', 
            {'student':student,
             'form':form})


from django.contrib import messages
@login_required
@role_required(allowed_roles=['Librarian'])
def IssueBook(request):
    if request.method=="POST":
        form=IssuebookForm(request.POST)
        if form.is_valid():
            try:
                stdid=form.cleaned_data['student']
                bkid=form.cleaned_data['book']
            except ValueError:
                print('cannot issue')
            request.session['issue_std_id']=stdid
            request.session['issue_book_id']=bkid
            return redirect('issue-confirm')
            
    else:
        form=IssuebookForm()
    return render(request, 'operations/issue_book.html', {
        'form':form,
        })



@login_required
@role_required(allowed_roles=['Librarian'])
def IssueBookconfirm(request):
    studentinfo=User.objects.get(id=request.session['issue_std_id'])
    bookinfo=AddBooks.objects.get(id=request.session['issue_book_id'])
    if request.method=="POST":
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
        del request.session['issue_std_id']
        del request.session['issue_book_id']
        return redirect('issuedbooks')
    return render(request, 'operations/confirm_issue_book.html', {
        'studentinfo':studentinfo,
        'bookinfo':bookinfo,
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
        if notify:
            send_mail(
                'for your request',
                'you have requested for book'+' '+notify.book.books_name+' '+'which is now available',
                'pandeyvivak25@gmail.com',
                [notify.student.email],
                fail_silently=False,
            )
            notify.delete()

            """account_sid=settings.TWILIO_ACCOUNT_SID
            auth_token=settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                     body='you have requested for book ('+' '+notify.book.books_name+' '+') which is now available',
                     from_=settings.phone_num,
                     to='+9779844700852',
                 )"""

    else:
        bookitem.available_quantity=bookitem.books_quantity
    bookitem.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'operations/return_book.html', 
        {'rtnbook':rtnbook}
        )

@login_required
@role_required(allowed_roles=['Librarian'])
def IssuedBook(request):
    issueditems=IssueBooks.objects.filter(returned=False)
    return render(request, 
        'operations/issued_list.html', 
        {'issueditems':issueditems}
        )


@login_required
@role_required(allowed_roles=['Librarian'])
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
        initial_path=settings.BASE_DIR+'\\'+"std"+id+".png"
        new_path=settings.BASE_DIR+'\\'+'media'+"\\"+"std"+id+".png"
        shutil.move(initial_path, new_path)
        std.barcode=filename
        std.save()
    return redirect('liststd')



@login_required
def SearchBooks(request):
    query=request.POST['book']
    print(query)
    if query:
        books=AddBooks.objects.filter(
            Q(books_name__icontains = query) 
            | Q(books_author_name__icontains = query) | 
            Q(books_publication_name__icontains = query)|
            Q(catagory__catagory__icontains= query)|
            Q(id__iexact= query)
            ) 
    else:
        books=[]
    return render(request, 'operations/displaybooks.html', 
        {'books':books}
        )


@login_required
def EBookRequest(request, id):
    req=Ebooks.objects.get(id=id)
    EbookRequest.objects.get_or_create(ebook=req, 
        requested_by=request.user)
    return redirect('list-ebooks')


@login_required
@role_required(allowed_roles=['Librarian'])
def ViewEbookRequest(request):
    requests=EbookRequest.objects.all()
    return render(request, 'operations/ebook-request.html', 
        {'requests':requests})


@login_required
@role_required(allowed_roles=['Librarian'])
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
@role_required(allowed_roles=['Librarian'])
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



@login_required
@role_required(allowed_roles=['Librarian'])
def BookprintBarCode(request, id):
    book=AddBooks.objects.get(id=id)
    if not book.barcode:
        ean = barcode.get('code128', id, writer=ImageWriter())
        filename = ean.save('book'+id)
        initial_path=settings.BASE_DIR+'\\'+"book"+id+".png"
        new_path=settings.BASE_DIR+'\\'+'media'+"\\"+'book'+id+".png"
        shutil.move(initial_path, new_path)
        book.barcode=filename
        book.save()
    return redirect('displaybooks')


@login_required
@role_required(allowed_roles=['Student'])
def View_my_readable_book(request):
    change=EbookRequestHistory.objects.filter(requested_by=request.user)
    for i in change:
        if i.readable_upto<datetime.datetime.utcnow().replace(tzinfo=pytz.UTC):
            i.readable=False
            i.save()
    readable_book=EbookRequestHistory.objects.filter(requested_by=request.user, readable=True)
    return render(request, 'operations/my-readable-book.html', {'readable_book':readable_book})


class EBookcatagorylist(LoginRequiredMixin, ListView):
    model = Ebooks
    template_name = 'operations/ebook-list.html'
    context_object_name = 'ebooks'

    def get_queryset(self):
        catagory = get_object_or_404(Catagory, catagory=self.kwargs.get('catagory'))
        return Ebooks.objects.filter(catagory = catagory)


class Bookcatagorylist(LoginRequiredMixin, ListView):
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
        if  self.request.user.Role=='Librarian':
            return True
        else:
            return False



class EditEbooks(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ebooks
    form_class = EbooksForm
    template_name = "operations/ebook-update.html"

    def form_valid(self, form):
        form.instance.book=self.request.FILES['book'] or None
        form.instance.cover_image=self.request.FILES['cimage'] or None
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list-ebooks")

    def test_func(self):
        if  self.request.user.Role=='Librarian':
            return True
        else:
            return False

@login_required
def NotifyMe(request, id):
    book=AddBooks.objects.get(id=id)
    NotifyMeModel.objects.get_or_create(student=request.user,
        book=book)
    return redirect('displaybooks')


@login_required
@role_required(allowed_roles=['Librarian'])
def StdDetail(request, id):
    total=0
    std=User.objects.get(id=id)
    course=Student.objects.filter(student=std).first()
    book_issued=IssueBooks.objects.filter(student=std, 
        returned=False)
    issue_rec=IssueBooks.objects.filter(student=std, returned=False)
    notify=NotifyMeModel.objects.filter(student=std)
    message=Message.objects.filter(posted_to=std).order_by('Posted_on')[::-1]
    for item in issue_rec:
        total=total+item.fine
    return render(request, 'operations/std-detail.html', 
        {
        'std':std,
        'course':course,
        'book_issued':book_issued,
        'notify':notify,
        'message':message,
        'issue_rec':issue_rec,
        'total':total,
        })


class DetailBook(LoginRequiredMixin, DetailView):
    template_name='operations/book-detail.html'
    model=AddBooks

    def get_context_data(self, *args, **kwargs):
        context = super(DetailBook, self).get_context_data(*args, 
            **kwargs)
        book=AddBooks.objects.get(pk=self.kwargs.get('pk'))
        issued=IssueBooks.objects.filter(book=book, 
            returned=False)
        notifyme=NotifyMeModel.objects.filter(book=book)
        context.update({
            'book':book,
            'issued':issued,
            'notifyme':notifyme
            })
        return context


class DetailEBook(LoginRequiredMixin, DetailView):
    template_name='operations/ebook-detail.html'
    model=Ebooks

    def get_context_data(self, *args, **kwargs):
        context = super(DetailEBook, self).get_context_data(*args, 
            **kwargs)
        ebook=Ebooks.objects.get(pk=self.kwargs.get('pk'))
        allowed=EbookRequestHistory.objects.filter(ebook=ebook, 
            readable=True)
        context.update({
            'ebook':ebook,
            'allowed':allowed
            })
        return context


@login_required
def ViewEbook(request, id):
    if request.method != "POST":
        return redirect('home')
    else:
        read=Ebooks.objects.get(id=id)
    return render(request, 'operations/pdf.html', 
        {'read':read})


@login_required
@role_required(allowed_roles=['Librarian'])
def SearchStudent(request):
    query=request.POST['qs']
    if query:
        stdrecord=User.objects.filter(
            Q(username__icontains = query) 
            | Q(first_name__icontains = query) | 
            Q(id__icontains = query)
            ) 
    else:
        stdrecord=[]
    return render(request, 'operations/liststd.html', 
        {'stdrecord':stdrecord}
       )

@login_required
@role_required(allowed_roles=['Librarian'])
def SearchIssued(request):
    query=request.POST['issued']
    if query:
        returned_item=IssueBooks.objects.filter(returned=True)
        issueditems=IssueBooks.objects.filter(
            Q(student__first_name__icontains = query) 
            | Q(student__id__iexact = query) |
            Q(student__username__iexact = query)
            ).exclude(id__in=returned_item)
    else:
        stdrecord=[]
    return render(request, 'operations/issued_list.html', 
        {'issueditems':issueditems}
       )


@login_required
def SearchEBooks(request):
    query=request.POST['ebk']
    if query:
        ebooks=Ebooks.objects.filter(
            Q(name__icontains = query) 
            | Q(id__iexact = query) |
            Q(author_name__iexact = query)
            )
    else:
        ebooks=[]
    return render(request, 'operations/ebook-list.html', 
        {'ebooks':ebooks}
       )


@login_required
@role_required(allowed_roles=['Student'])
def ViewMessage(request):
    msgs=Message.objects.filter(
        posted_to=request.user
        ).order_by('Posted_on')[::-1]
    return render(request, 'operations/list-msg.html', {
        'msgs':msgs,

        })


@login_required
@role_required(allowed_roles=['Student'])
def ViewMessageDetail(request, id):
    msg_detail=Message.objects.get(id=id)
    msg_detail.read=True
    msg_detail.save()
    return render(request, 'operations/msg-detail.html',
        {'msg_detail':msg_detail}
        )



class IssueActivities(ListView, LoginRequiredMixin, UserPassesTestMixin):
    template_name='operations/issue-activities.html'
    queryset=IssueBooks.objects.all().order_by('-issued_date')

    def get_context_data(self, *args, **kwargs):
        context=super(IssueActivities,self).get_context_data(*args, 
            **kwargs)
        activities=self.get_queryset()
        context.update({
            'activities':activities,
            })
        return context

    def test_func(self):
        if  self.request.user.Role=='Librarian':
            return True
        else:
            return False



class EbookActivities(ListView, LoginRequiredMixin, UserPassesTestMixin):
    template_name='operations/ebook-activities.html'
    queryset=EbookRequestHistory.objects.all().order_by('-requested_date')

    def get_context_data(self, *args, **kwargs):
        context=super(EbookActivities,self).get_context_data(*args, **kwargs)
        activities=self.get_queryset()
        context.update({
            'activities':activities,
            })
        return context

    def test_func(self):
        if  self.request.user.Role=='Librarian':
            return True
        else:
            return False


def error_404(request):
        data = {}
        return render(request,'operations/400.html', data)


def error_500(request):
        data = {}
        return render(request,'myapp/error_500.html', data)


@login_required
@role_required(allowed_roles=['Student'])
def MYFine(request):
    sum=0
    issue_rec=IssueBooks.objects.filter(student=request.user, returned=False)
    for i in issue_rec:
        sum=sum+i.fine
    return render(request,'operations/my_fine.html', {'issue_rec':issue_rec, 'sum':sum})



        















