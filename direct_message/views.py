from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from direct_message.models import Message


@login_required
def index(request):
    user=request.user
    messages=Message.get_message(user=user)
    active_direct=None
    directs=None

    if messages:
        message=messages[0]
        active_direct=message['user'].username
        directs=Message.objects.filter(user=user,reciever=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread']=0
        context={
            'directs':directs,
            'messages':messages,
            'active_direct':active_direct,
        }
        return render(request,'directs/index.html',context)
    
@login_required
def Directs(request,username):
    user=request.user
    # messages=Message.get_message(user=user)
    active_direct=username
    directs=Message.objects.filter(user=user,reciever__username=active_direct)
    directs.update(is_read=True)
    indirect=Message.objects.filter(reciever=user)
    messages=directs.union(indirect).order_by('date')

    for message in messages:
        if message.user.username==username:
            message.is_read=True
            message.save()
    context={
        'directs':directs,
        'active_direct':active_direct,
        'messages':messages,
        'indirect':indirect
    }
    return render(request,'directs/directs.html',context)
