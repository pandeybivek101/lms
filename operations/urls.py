"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from operations import views
from operations.views import *
from django.conf.urls import handler404, handler500


urlpatterns = [
    path('', views.Home, name='home'),
    path('scan/', views.Scan, name='scan'),
    path('scan/error', views.ScanError, name='scanerror'),
    path('my-fine/', views.MYFine, name='my_fine'),
    path('view-message/', 
        views.ViewMessage, name='view-message'),

    path('view-message/<int:id>/detail', 
        views.ViewMessageDetail, name='view-msg-detail'),
    
    path('direct-view/<int:id>/', views.DirectView, name='direct-view'),

    path('search', views.Search, name='search'),

    path('add-librarian/', views.Addmember, name='member-add'),
    path('add-student/', views.AddStudent, name='add-student'),

    path('addcatagory/', views.AddCatagory, name='addcatagory'),
    path('catagory-list/', views.ListCatagory, name='catagory-list'),
    path('catagory-list/<int:pk>/edit', EditCatagory.as_view(), 
        name='catagory-edit'),
    path('catagory-list/<int:pk>/delete', DeleteCatagory.as_view(), 
        name='catagory-delete'),
    #path('sinfo/', views.StudentInfo, name='sinfo'),


    path('issuebooks', views.IssueBook, name='issuebooks'),
    path('issuebooks/confirm',views.IssueBookconfirm, name='issue-confirm'),
    path('issuedbooks/<int:pk>/returnbooks', views.ReturnBooks, 
        name='returnbooks'),
    path('issuedbooks/<int:id>/renew-books', views.RenewBooks, 
        name='renew-books'),
    path('issue-activities/', IssueActivities.as_view(), 
        name='issue-activities'),

    path('issuedbooks',views.IssuedBook, name='issuedbooks'),

    path('addbooks', views.AddBook, name='addbooks'),

    path('liststd', ListStd.as_view(), name='liststd'),
    path('list-librarian', views.LibrarianView, name='listlib'),
    path('list-librarian/<int:id>/edit', views.EditLibrarian, 
        name='editlib'),

    #path('liststd/<int:pk>/delete', DeleteStd.as_view(), name='deletestd'),
    path('liststd/<int:id>/active', views.Activatestd, name='activate'),
    path('liststd/<int:id>/inactive', views.InActivatestd, name='inactivate'),
    path('liststd/<str:id>/std-barcode', views.printBarCode, name='st-barcode'),
    path('liststd/<int:id>/detail', views.StdDetail, name='std-detail'),
    path('liststd/<int:id>/detail/message', views.Messagestd, name='msg_std'),
    path('liststd/<int:id>/edit', views.EditStudent, 
       name='editstd'),
    path('liststd/<int:pk>/delete', DeleteStd.as_view(), 
        name='deletestd'),

    path('displaybooks', DisplayBooks.as_view(), name='displaybooks'),
    path('displaybooks/<str:catagory>', Bookcatagorylist.as_view(), name='book-catagory'),
    path('displaybooks/<str:id>/book-barcode', views.BookprintBarCode, name='book-barcode'),
    path('displaybooks/<int:pk>/delete', DeleteBook.as_view(), name='deletebook'),
    path('displaybooks/<int:pk>/edit', EditBook.as_view(), name='editbook'),
    path('displaybooks/<int:pk>/detail', DetailBook.as_view(), name='detail-book'),
    path('displaybooks/<int:id>/notify', views.NotifyMe, name='notifyme'),

    path('my-issued-books/', views.myissuedbook, name='myissuedbook'),

    path('list-ebooks/', ListEbooks.as_view(), name='list-ebooks'),
    path('list-ebooks/<int:pk>/delete', DeleteEBooks.as_view(), name='delete-ebook'),
    path('list-ebooks/<int:pk>/edit', EditEbooks.as_view(), name='edit-ebook'),
    path('list-ebooks/<int:id>/view-request', views.EBookRequest, name='view-request'),
    path('list-ebooks/<str:catagory>', EBookcatagorylist.as_view(), name='ebook-catagory'),
    path('list-ebooks/<int:pk>/detail', DetailEBook.as_view(), name='detail-ebook'),
    path('list-ebooks/<int:id>/view', views.ViewEbook, name='view'),
    path('ebook-activities/', EbookActivities.as_view(), name='ebook-activities'),


    path('add-ebooks/', views.AddEbooks, name='add-ebooks'),


    path('view-ebook-request/', views.ViewEbookRequest, name='view-ebook-request'),
    path('view-ebook-request/<int:id>/allow', views.View_Ebook_Request_allow, name='allow'),
    path('view-ebook-request/<int:id>/deny', views.View_Ebook_Request_deny, name='deny'),
    path('readable-ebook/', views.View_my_readable_book, name='readable-book'),
  
]
