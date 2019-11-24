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
    path('my-fine/', views.MYFine, name='my_fine'),
    path('view-message/', views.ViewMessage, name='view-message'),
    path('view-message/<int:id>/detail', views.ViewMessageDetail, name='view-msg-detail'),


    path('issuebooks', views.IssueBook, name='issuebooks'),
    path('issuebooks/confirm',views.IssueBookconfirm, name='issue-confirm'),
    path('issuedbooks/<int:pk>/returnbooks', views.ReturnBooks, name='returnbooks'),
    path('issuedbooks/search-issued/', views.SearchIssued, name='search-issued'),
    path('issue-activities/', IssueActivities.as_view(), name='issue-activities'),


    #path('issuedbooks/<int:pk>/returnbooks', ReturnBooks.as_view(), name='returnbooks'),
    path('issuedbooks',views.IssuedBook, name='issuedbooks'),

    path('addbooks', views.AddBook, name='addbooks'),

    path('liststd', ListStd.as_view(), name='liststd'),
    path('liststd/<int:pk>/delete', DeleteStd.as_view(), name='deletestd'),
    path('liststd/<str:id>/std-barcode', views.printBarCode, name='st-barcode'),
    path('liststd/<int:id>/detail', views.StdDetail, name='std-detail'),
    path('liststd/search-student/', views.SearchStudent, name='search-student'),
    path('liststd/<int:id>/detail/message', views.Messagestd, name='msg_std'),

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
    #path('list-ebooks/<int:pk>/read', views.ReadEbook, name='read-ebook'),
    path('list-ebooks/<int:id>/view-request', views.EBookRequest, name='view-request'),
    path('list-ebooks/<str:catagory>', EBookcatagorylist.as_view(), name='ebook-catagory'),
    path('list-ebooks/<int:pk>/detail', DetailEBook.as_view(), name='detail-ebook'),
    path('list-ebooks/<int:id>/view', views.ViewEbook, name='view'),
    path('list-ebooks/search-ebook/', views.SearchEBooks, name='search-ebooks'),
    path('ebook-activities/', EbookActivities.as_view(), name='ebook-activities'),


    path('add-ebooks/', views.AddEbooks, name='add-ebooks'),

    path('displaybooks/search-book/', views.SearchBooks, name='search-books'),

    path('view-ebook-request/', views.ViewEbookRequest, name='view-ebook-request'),
    path('view-ebook-request/<int:id>/allow', views.View_Ebook_Request_allow, name='allow'),
    path('view-ebook-request/<int:id>/deny', views.View_Ebook_Request_deny, name='deny'),
    path('readable-ebook/', views.View_my_readable_book, name='readable-book'),
]

handler404 = views.error_404
handler500 = views.error_500
