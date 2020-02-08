from .models import *
import calendar
import datetime

def my_context_processor(request):
    if request.user.is_authenticated:
        count=Message.objects.filter(posted_to=request.user, read=False).count()
        msgs=Message.objects.filter(posted_to=request.user).order_by('Posted_on')[::-1]
        sent_msgs=Message.objects.filter(
            posted_by=request.user).order_by('Posted_on')[::-1]
        return {
            'count': count,
            'msgs':msgs,
            'sent_msgs':sent_msgs
        }
    return {}


def get_all_catagory(request):
    catagories=Catagory.objects.all().order_by('catagory')
    return {'catagories':catagories}


def issue_requests(request):
    issue_requests=EbookRequest.objects.all().count()
    return {'issue_requests':issue_requests}


def chart(request):
    if request.user.is_authenticated:
        issued_yearly=[]
        returned_yearly=[]
        allowed_std=[]
        denied_std=[]
        my_issued=[]
        my_returned=[]
        curr_date=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        for i in range(1, 13):

            returned_result=IssueBooks.objects.filter(
                returned_date__year=curr_date.year,
                returned=True,
                returned_date__month=i).count()
            returned_yearly.append(returned_result)

            issued_result=IssueBooks.objects.filter(
                issued_date__year=curr_date.year,
                issued_date__month=i).count()
            issued_yearly.append(issued_result)


            my_return=IssueBooks.objects.filter(
                returned_date__year=curr_date.year,
                returned=True,
                student=request.user,
                returned_date__month=i).count()
            my_returned.append(my_return)

            my_issue=IssueBooks.objects.filter(
                issued_date__year=curr_date.year,
                student=request.user,
                issued_date__month=i).count()
            my_issued.append(my_issue)

            my_total_allowed=EbookRequestHistory.objects.filter(
                requested_by=request.user,
                action='Allowed', 
                action_date__year=curr_date.year, 
                action_date__month=i).count()
            allowed_std.append(my_total_allowed)

            my_total_denied=EbookRequestHistory.objects.filter(
                requested_by=request.user,
                action='Denied', 
                action_date__year=curr_date.year, 
                action_date__month=i).count()
            denied_std.append(my_total_denied)


        std_nonfined=IssueBooks.objects.filter(fine=0,
            returned=True, student=request.user).count()
        std_fined=IssueBooks.objects.filter(fine__gt=0,
            student=request.user).count()


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
        'issued_today':issued_today,
        'returned_today':returned_today,
        'issued_monthly':issued_monthly,
        'returned_monthly':returned_monthly,
        'non_fined':non_fined,
        'fined':fined,
        'total_allowed':total_allowed,
        'total_denied':total_denied,
        'total_pending':total_pending,
        'issued_yearly':issued_yearly,
        'returned_yearly':returned_yearly,
        'allowed_std':allowed_std,
        'denied_std':denied_std,
        'std_nonfined':std_nonfined,
        'std_fined':std_fined,
        'my_returned':my_returned,
        'my_issued':my_issued,
        }
    return {}

