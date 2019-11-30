from .models import *
import calendar
import datetime
import numpy as np

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
    issue_requests=EbookRequest.objects.all().count()
    return {'issue_requests':issue_requests}


def chart(request):
    if request.user.is_authenticated:
        count_lst=[]
        cat_lst=[]
        erh_lst=[]
        curr_date=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        year=curr_date.year
        mnth=curr_date.month
        mnth_bk=mnth-4
        my_iss=[]
        my_ret=[]
        my_mnth=[]
        for i in range(mnth_bk, mnth+1):
            issued_data=IssueBooks.objects.filter(
                student=request.user,
                issued_date__year=year,
                issued_date__month=i,
            )
            my_mnth.append(calendar.month_name[i])
            my_iss.append(issued_data.count())
            returned_data=IssueBooks.objects.filter(
                student=request.user,
                issued_date__year=year,
                issued_date__month=i,
                returned=True,
            )
            my_ret.append(returned_data.count())
        for i in range(1, 13):
            issued_data=IssueBooks.objects.filter(
                issued_date__year=year, 
                issued_date__month=i
                )
            count=issued_data.count()
            count_lst.append(count)
            erh=EbookRequestHistory.objects.filter(
                action_date__year=year,
                action_date__month=i, 
                action='Allowed').count()
            erh_lst.append(erh)
        tot_issue=IssueBooks.objects.all().count()
        non_fined=IssueBooks.objects.filter(fine=0, returned=True).count()
        fined=IssueBooks.objects.filter(fine__gt=0).count()
        self_user=IssueBooks.objects.filter(student=request.user)
        msg_count=Message.objects.filter(posted_to=request.user, 
            read=False).count()
        issued_today=IssueBooks.objects.filter(
            issued_date__day=curr_date.day).count()
        returned_today=IssueBooks.objects.filter(returned=True, 
            returned_date__day=curr_date.day).count()
        issued_monthly=IssueBooks.objects.filter(
            issued_date__month=curr_date.month).count()
        returned_monthly=IssueBooks.objects.filter(returned=True, 
        returned_date__month=curr_date.month).count()
        total_allowed=EbookRequestHistory.objects.filter(
            action='Allowed').count()
        total_denied=EbookRequestHistory.objects.filter(
            action='Denied').count()
        total_pending=EbookRequest.objects.all().count()
        return {
        'count_lst':count_lst,
        'erh_lst':erh_lst,
        'curr_date':curr_date,
        'my_iss':my_iss,
        'my_ret':my_ret,
        'my_mnth':my_mnth,
        'msg_count':msg_count,
        'issued_today':issued_today,
        'returned_today':returned_today,
        'issued_monthly':issued_monthly,
        'returned_monthly':returned_monthly,
        'non_fined':non_fined,
        'fined':fined,
        'total_allowed':total_allowed,
        'total_denied':total_denied,
        'total_pending':total_pending,
        }
    return {}


