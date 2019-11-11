from .models import *

def my_context_processor(request):
    if request.user.is_authenticated:
        msgs=Message.objects.filter(posted_to=request.user, read=False)
        count=msgs.count()
        return {
            'count': count
        }
    return {}


def get_all_catagory(request):
    catagories=Catagory.objects.all()
    return {'catagories':catagories}