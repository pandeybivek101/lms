from django.contrib import admin
from .models import *
# Register your models here.
#jjj
class IssueBookAdmin(admin.ModelAdmin):
	list_display=['student', 'book' , 'returned', 'issued_by']
admin.site.register(IssueBooks, IssueBookAdmin)


class AddBooksAdmin(admin.ModelAdmin):
	list_display=['books_name', 'books_author_name', 'books_publication_name', 'catagory']
admin.site.register(AddBooks, AddBooksAdmin)


class MessageAdmin(admin.ModelAdmin):
	list_display=['title', 'Posted_on', 'posted_to', 'read', ]
admin.site.register(Message, MessageAdmin)

class NotifyAdmin(admin.ModelAdmin):
	list_display=['student', 'book', 'req_date', 'notified', 'cancelled']
admin.site.register(NotifyMeModel, NotifyAdmin)


class EbooksAdmin(admin.ModelAdmin):
	list_display=['name','author_name','catagory']
admin.site.register(Ebooks, EbooksAdmin)


class EbooksRequestAdmin(admin.ModelAdmin):
	list_display=['ebook', 'requested_by']
admin.site.register(EbookRequest, EbooksRequestAdmin)


class EBRHAdmin(admin.ModelAdmin):
	list_display=['ebook', 'action', 'requested_by', 'readable']
admin.site.register(EbookRequestHistory, EBRHAdmin)

admin.site.register(Catagory)

