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
urlpatterns = [
    path('', views.Home, name='home'),
    path('issuebooks', views.IssueBook, name='issuebooks'),
    path('issuedbooks/<int:pk>/returnbooks', views.ReturnBooks, name='returnbooks'),
    #path('issuedbooks/<int:pk>/returnbooks', ReturnBooks.as_view(), name='returnbooks'),
    path('issuedbooks',views.IssuedBook, name='issuedbooks'),

    path('addbooks', views.AddBook, name='addbooks'),

    path('liststd', views.ListStd, name='liststd'),
    path('liststd/<int:pk>/delete', DeleteStd.as_view(), name='deletestd'),
    path('liststd/<str:id>/std-barcode', views.printBarCode, name='st-barcode'),
    path('liststd/<int:pk>/detail', StdDetail.as_view(), name='std-detail'),

    path('displaybooks', views.DisplayBooks, name='displaybooks'),
    path('displaybooks/<str:catagory>', Bookcatagorylist.as_view(), name='book-catagory'),
    path('displaybooks/<str:id>/book-barcode', views.BookprintBarCode, name='book-barcode'),
    path('displaybooks/<int:pk>/delete', DeleteBook.as_view(), name='deletebook'),
    path('displaybooks/<int:pk>/edit', EditBook.as_view(), name='editbook'),
    path('displaybooks/<int:pk>/detail', DetailBook.as_view(), name='detail-book'),
    path('displaybooks/<int:id>/notify', views.NotifyMe, name='notifyme'),

    path('notices', views.Notices, name='notices'),
    path('addnotice', views.AddNotice, name='addnotice'),
    path('listnotices', views.ListNotices, name='listnotices'),
    path('deletenotice/<int:id>', views.DeleteNotice, name='deletenotice'),
    path('editnotice/<int:id>', views.EditNotice, name='editnotice'),

    path('my-issued-books/', views.myissuedbook, name='myissuedbook'),

    path('list-ebooks/', views.ListEbooks, name='list-ebooks'),
    path('list-ebooks/<int:pk>/delete', DeleteEBooks.as_view(), name='delete-ebook'),
    path('list-ebooks/<int:pk>/edit', EditEbooks.as_view(), name='edit-ebook'),
    #path('list-ebooks/<int:pk>/read', views.ReadEbook, name='read-ebook'),
    path('list-ebooks/<int:id>/view-request', views.EBookRequest, name='view-request'),
    path('list-ebooks/<str:catagory>', EBookcatagorylist.as_view(), name='ebook-catagory'),
    path('list-ebooks/<int:pk>/detail', DetailEBook.as_view(), name='detail-ebook'),

    path('add-ebooks/', views.AddEbooks, name='add-ebooks'),

    path('search-book/', views.SearchBooks, name='search-books'),

    path('view-ebook-request/', views.ViewEbookRequest, name='view-ebook-request'),
    path('view-ebook-request/<int:id>/allow', views.View_Ebook_Request_allow, name='allow'),
    path('view-ebook-request/<int:id>/deny', views.View_Ebook_Request_deny, name='deny'),
    path('readable-ebook/', views.View_my_readable_book, name='readable-book'),
]
