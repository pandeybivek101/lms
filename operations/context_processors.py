from .models import *

def my_context_processor(request):
    if request.user.is_authenticated:
        count=Message.objects.filter(posted_to=request.user, read=False).count()
        msgs=Message.objects.filter(posted_to=request.user).order_by('Posted_on')[::-1]
        return {
            'count': count,
            'msgs':msgs,
        }
    return {}


def get_all_catagory(request):
    catagories=Catagory.objects.all()
    return {'catagories':catagories}


def issue_requests(request):
    issue_requests=EbookRequest.objects.all()
    return {'issue_requests':issue_requests}