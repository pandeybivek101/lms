from django.contrib import admin
from .models import *
# Register your models here.

class IssueBookAdmin(admin.ModelAdmin):
	list_display=['student', 'book' ,'issued_by']
admin.site.register(IssueBooks, IssueBookAdmin)


class AddBooksAdmin(admin.ModelAdmin):
	list_display=['books_name', 'books_author_name', 'books_publication_name', 'catagory']
admin.site.register(AddBooks, AddBooksAdmin)


admin.site.register(Notice)
admin.site.register(NotifyMeModel)


class EbooksAdmin(admin.ModelAdmin):
	list_display=['name','author_name','catagory']
admin.site.register(Ebooks, EbooksAdmin)

class EbooksRequestAdmin(admin.ModelAdmin):
	list_display=['ebook', 'requested_by']
admin.site.register(EbookRequest, EbooksRequestAdmin)

class EBRHAdmin:
	list_display=['ebook', 'action', 'requested_by']
admin.site.register(EbookRequestHistory)

admin.site.register(Catagory)

