from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from .models import *
from django.contrib import auth
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from account.models import *
from django.contrib.auth import authenticate, login, logout
import datetime
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from account.models import User
from .decorators import role_required
import barcode
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.urls import reverse_lazy
from django.db.models import Q
import shutil
from barcode.writer import ImageWriter
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
from django.utils.decorators import method_decorator
from twilio.rest import Client
from twilio.rest import TwilioRestClient
from account.forms import *



# Create your views here.


@login_required
def Home(request):
    return render(request,'operations/home.html')

    
@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def Scan(request):
    return render(request, 'operations/quagga.html',
        {})


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def ScanError(request):
    return render(request, 'operations/notfound.html',
        {})


@login_required
@role_required(allowed_roles=['Admin'])
def ListCatagory(request):
    return render(request, 'operations/list-catagory.html',
        {})


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
        readable=EbookRequestHistory.objects.filter(
            requested_by=self.request.user, 
            readable=True)
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


@method_decorator(role_required(allowed_roles=['Librarian', 'Admin']), 
    name='dispatch')
class ListStd(LoginRequiredMixin, ListView):
    template_name='operations/liststd.html'
    queryset=User.objects.filter(Role='Student')
    context_object_name='stdrecord'


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
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
            student=self.request.user, notified=False, cancelled=False
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



@method_decorator(role_required(allowed_roles=['Librarian', 'Admin']), 
    name='dispatch')
class DeleteBook(LoginRequiredMixin, DeleteView):
    model = AddBooks
    template_name = 'operations/deletebooks.html'
    
    def get_success_url(self):
        return reverse_lazy("displaybooks")



@method_decorator(role_required(allowed_roles=['Librarian', 'Admin']), 
    name='dispatch')
class EditBook(LoginRequiredMixin, UpdateView):
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



@role_required(allowed_roles=['Librarian', 'Admin'])
def Messagestd(request, id):
    msg_std=User.objects.get(id=id)
    if request.method=='POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            msg=form.save(commit=False)
            msg.posted_to=msg_std
            msg.posted_by=request.user
            msg.save()
            messages.success(request, f'Message sent SuccessFully')
            return redirect("/liststd/{}/detail".format(id))
    else:
        form=MessageForm()
    return render(request, 'operations/addmessage.html', {
        'form':form,
        'msg_std':msg_std,
        })



@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def Activatestd(request, id):
    std=User.objects.get(id=id)
    std.is_active=True
    std.save()
    messages.success(request, f'Account activation success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def InActivatestd(request, id):
    std=User.objects.get(id=id)
    std.is_active=False
    std.save()
    messages.success(request, f'Account Deactivation Success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def EditStudent(request, id):
    student=SRegistration.objects.get(id=id)
    form=form1(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, f'Successfully edited Student Record')
        return redirect("liststd")
    else:
        return render(request,'SRegistration.html', 
            {'student':student,
             'form':form})



from django.contrib import messages
@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def IssueBook(request):
    if request.method=="POST":
        form=IssuebookForm(request.POST)
        if form.is_valid():
            stdid=form.cleaned_data['student']
            bkid=form.cleaned_data['book']
            request.session['issue_std_id']=stdid
            request.session['issue_book_id']=bkid
            return redirect('issue-confirm')
            
    else:
        form=IssuebookForm()
    return render(request, 'operations/issue_book.html', {
        'form':form,
        })



@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def IssueBookconfirm(request):
    studentinfo=User.objects.get(id=request.session['issue_std_id'])
    bookinfo=AddBooks.objects.get(id=request.session['issue_book_id'])
    if request.method=="POST":
        return_date=datetime.datetime.utcnow().replace(
            tzinfo=pytz.UTC) + datetime.timedelta(days=30)
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
        messages.success(request, f'Book Issued Successfully')
        return redirect('issuedbooks')
    return render(request, 'operations/confirm_issue_book.html', {
        'studentinfo':studentinfo,
        'bookinfo':bookinfo,
        })


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def ReturnBooks(request, pk):
    rtnbook=IssueBooks.objects.get(pk=pk)
    rtnbook.returned=True
    rtnbook.returned_date=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    rtnbook.returned_by=request.user
    rtnbook.save()
    bookitem=AddBooks.objects.get(id=rtnbook.book.id)
    if bookitem.available_quantity < bookitem.books_quantity:
        bookitem.available_quantity=bookitem.available_quantity+1
        notify=NotifyMeModel.objects.filter(book=bookitem, 
            cancelled=False, notified=False).first()
        if notify:
            send_mail(
                'for your request',
                'you have requested for book'+' '+notify.book.books_name+' '+'which is now available',
                'pandeyvivak25@gmail.com',
                [notify.student.email],
                fail_silently=False,
            )
            notify.notified_at=datetime.datetime.utcnow().replace(
                tzinfo=pytz.UTC)
            notify.notified=True
            notify.save()

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
@role_required(allowed_roles=['Librarian', 'Admin'])
def IssuedBook(request):
    issueditems=IssueBooks.objects.filter(returned=False)
    return render(request, 
        'operations/issued_list.html', 
        {'issueditems':issueditems}
        )


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def AddEbooks(request):
    if request.method == 'POST':
        form = EbooksForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'EBook Added Successfully')
            return redirect('list-ebooks')
    else:
        form = EbooksForm()
    return render(request, 'operations/addfiles.html', {
        'form': form,
    })


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
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
@role_required(allowed_roles=['Librarian', 'Admin'])
def ViewEbookRequest(request):
    requests=EbookRequest.objects.all()
    return render(request, 'operations/ebook-request.html', 
        {'requests':requests})


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
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
@role_required(allowed_roles=['Librarian', 'Admin'])
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
@role_required(allowed_roles=['Librarian', 'Admin'])
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
    readable_book=EbookRequestHistory.objects.filter(requested_by=request.user, 
        readable=True)
    print(readable_book)
    return render(request, 'operations/my-readable-book.html', {
        'readable_book':readable_book
        })


class EBookcatagorylist(LoginRequiredMixin, ListView):
    model = Ebooks
    template_name = 'operations/ebook-list.html'
    context_object_name = 'ebooks'

    def get_queryset(self):
        catagory = get_object_or_404(Catagory, 
            catagory=self.kwargs.get('catagory'))
        return Ebooks.objects.filter(catagory = catagory)


class Bookcatagorylist(LoginRequiredMixin, ListView):
    model = AddBooks
    template_name = 'operations/displaybooks.html'
    context_object_name = 'books'

    def get_queryset(self):
        catagory = get_object_or_404(Catagory, 
            catagory=self.kwargs.get('catagory'))
        return AddBooks.objects.filter(catagory = catagory)



@method_decorator(role_required(allowed_roles=['Librarian', 'Admin']), 
    name='dispatch')
class DeleteEBooks(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Ebooks
    template_name = 'operations/delete-ebooks.html'
    success_message = 'Ebooks deleted successfully!!!!'
    
    def get_success_url(self):
        return reverse_lazy("list-ebooks")



@method_decorator(role_required(allowed_roles=['Librarian', 'Admin']), 
    name='dispatch')
class EditEbooks(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ebooks
    form_class = EbooksForm
    template_name = "operations/ebook-update.html"
    success_message = 'Ebooks Updated successfully!!!!'


    def get_success_url(self):
        return reverse_lazy("list-ebooks")

    
@login_required
def NotifyMe(request, id):
    book=AddBooks.objects.get(id=id)
    NotifyMeModel.objects.get_or_create(student=request.user,
        book=book)
    return redirect('displaybooks')


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def StdDetail(request, id):
    total=0
    try:
        std=User.objects.get(id=id)
        course=Student.objects.filter(student=std).first()
        book_issued=IssueBooks.objects.filter(student=std, 
                returned=False)
        issue_rec=IssueBooks.objects.filter(student=std, 
            returned=False)
        notify=NotifyMeModel.objects.filter(student=std, 
            notified=False, cancelled=False)
        message=Message.objects.filter(posted_to=std).order_by('Posted_on')[::-1]
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return redirect('scanerror')

    if issue_rec is not None :
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
        notifyme=NotifyMeModel.objects.filter(book=book, 
            notified=False, cancelled=False)
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
        return redirect('list-ebooks')
    else:
        read=Ebooks.objects.get(id=id)
    return render(request, 'operations/pdf.html', 
        {'read':read})



@login_required
def Search(request):
    query=request.POST.get('qs')
    if query:
        if request.user.Role=='Librarian' or request.user.Role=='Admin':
            stdrecord=User.objects.filter((
                Q(username__icontains = query) 
                | Q(first_name__icontains = query) | 
                Q(id__icontains = query)
                ), Role="Student"
                
                )
        else:
            stdrecord=[]
        ebookrecords=Ebooks.objects.filter(
            Q(name__icontains = query) 
            | Q(id__iexact = query) |
            Q(author_name__iexact = query)
            )
        bookrecords=AddBooks.objects.filter(
            Q(books_name__icontains = query) 
            | Q(books_author_name__icontains = query) | 
            Q(books_publication_name__icontains = query)|
            Q(catagory__catagory__icontains= query)|
            Q(id__iexact= query)
            )
    else:
        stdrecord=[]
        ebookrecords=[]
        bookrecords=[]
        query=[]
    return render(request, 'operations/search.html', 
        {'stdrecord':stdrecord,
        'ebookrecords':ebookrecords,
        'bookrecords':bookrecords,
        'query':query,
        }
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


@method_decorator(role_required(allowed_roles=['Librarian', 'Admin']), 
    name='dispatch')
class IssueActivities(ListView, LoginRequiredMixin):
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



@method_decorator(role_required(allowed_roles=['Librarian', 'Admin']), 
    name='dispatch')
class EbookActivities(ListView, LoginRequiredMixin):
    template_name='operations/ebook-activities.html'
    queryset=EbookRequestHistory.objects.all().order_by('-requested_date')

    def get_context_data(self, *args, **kwargs):
        context=super(EbookActivities, self).get_context_data(*args, **kwargs)
        activities=self.get_queryset()
        context.update({
            'activities':activities,
            })
        return context



@login_required
@role_required(allowed_roles=['Student'])
def MYFine(request):
    sum=0
    issue_rec=IssueBooks.objects.filter(student=request.user, 
        returned=False)
    for i in issue_rec:
        sum=sum+i.fine
    return render(request,'operations/my_fine.html', {
        'issue_rec':issue_rec, 
        'sum':sum})


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def RenewBooks(request, id):
    renew_item=IssueBooks.objects.get(id=id)
    if renew_item.renewed==False:
        renew_item.renewed=True
        renew_item.renewed_date=datetime.datetime.utcnow().replace(
            tzinfo=pytz.UTC)
        renew_item.return_date=renew_item.return_date+datetime.timedelta(
            days=30)
        renew_item.renewed_by=request.user
        renew_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
@role_required(allowed_roles=['Admin'])
def Addmember(request):
    if request.method=="POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            data=form.save(commit=False)
            data.username=email.split('@')[0]
            data.Role="Librarian"
            data.is_active=True
            data.save()
            messages.success(request, f'Librarian Added Successfully')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request,'operations/addmember.html', {'form':form})

@login_required
@role_required(allowed_roles=['Admin'])
def AddCatagory(request):
    if request.method=="POST":
        form=AddCatagoryForm(request.POST)
        if form.is_valid():
            catg=form.save(commit=False)
            catg.catagory_added_by=request.user
            catg.save()
            #return redirect('home')
    else:
        form=AddCatagoryForm()
    return render(request, 'operations/addcatagory.html',{'form':form})


@login_required
@role_required(allowed_roles=['Admin'])
def AddStudent(request):
    if request.method=="POST":
        form1=UserRegistrationForm(request.POST)
        form2=StudentForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            email=form1.cleaned_data['email']
            year= form2.cleaned_data['year']
            faculty=form2.cleaned_data['faculty']
            course=form2.cleaned_data['course']
            data=form1.save(commit=False)
            splitted_email=email.split('@')[0]
            data.username=splitted_email
            data.Role="Student"
            data.is_active=True
            data.save()
            instance=User.objects.filter(username=splitted_email).first()
            std_rec=Student.objects.filter(student=instance).first()
            std_rec.year=year
            std_rec.faculty=faculty
            std_rec.course=course
            std_rec.save()
            messages.success(request, f'Student Added Successfully')
            return redirect('home')
    else:
        form1=UserRegistrationForm()
        form2=StudentForm()
    return render(request, 'operations/addstudent.html', {'form1':form1,
        'form2':form2,})


@login_required
@role_required(allowed_roles=['Admin'])
def LibrarianView(request):
    librarians=User.objects.filter(Role="Librarian")
    return render(request, 'operations/librarian-list.html', 
        {'librarians':librarians})


@method_decorator(role_required(allowed_roles=['Admin']), 
    name='dispatch')
class EditCatagory(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Catagory
    form_class = AddCatagoryForm
    template_name = 'operations/editcatagory.html'
    context_object_name = 'catagory'
    success_message = 'Catagory updated successfully!!!!'
    success_url = reverse_lazy("catagory-list")


@method_decorator(role_required(allowed_roles=['Admin']), 
    name='dispatch')
class DeleteCatagory(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Catagory
    template_name = 'operations/delete-catagory.html'
    context_object_name = 'catagory'
    SuccessMessageMixin='Catagory deleted successfully!!!!'
    success_url = reverse_lazy("catagory-list")


@method_decorator(role_required(allowed_roles=['Admin']), 
    name='dispatch')
class DeleteStd(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'operations/deletestd.html'
    
    def get_success_url(self):
        return reverse_lazy("home")


@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def EditLibrarian(request, id):
    librarian=User.objects.get(id=id)
    form=UserRegistrationForm(request.POST or None, instance=librarian)
    if form.is_valid():
        form.save()
        messages.success(request, f'Updated Successfully')
        return redirect("listlib")
    else:
        return render(request,'operations/edit-librarian.html', 
            {'librarian':librarian,
             'form':form})

@login_required
@role_required(allowed_roles=['Librarian', 'Admin'])
def EditStudent(request, id):
    usr=User.objects.get(id=id)
    std=Student.objects.filter(student=usr).first()
    form1=UserRegistrationForm(request.POST or None, instance=usr)
    form2=StudentForm(request.POST or None, instance=std)
    if form1.is_valid() and form2.is_valid():
        form1.save()
        form2.save()
        messages.success(request, f'Updated Successfully')
        return redirect("liststd")
    else:
        return render(request,'operations/edit-std.html', 
            {'usr':usr,
            'std':std,
            'form2':form2,
             'form1':form1})


def load_courses(request):
    faculty_id = request.GET.get('faculty')
    courses = Course.objects.filter(
        belonged_faculty=faculty_id).order_by('name')
    return render(request, 'operations/course_dropdown.html', 
        {'courses': courses})















