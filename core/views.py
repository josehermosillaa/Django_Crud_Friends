from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required, admin_requerido
from .models import*


@login_required
def index(request):
    friendslist = []
    my_friend = []
    alias_list = []
    user = User.objects.get(id=request.session['usuario']['id'])
    # friends = Friend.objects.all().exclude(user_friend=user)
    friends = user.accepter.all()  
    # print(friends)
    for x in friends:
        friendslist.append(x)
        # print(friendslist)
    nonfriends = User.objects.all().exclude(id=user.id)
    for x in friendslist:
        nonfriends = nonfriends.exclude(id=x.user_friend.id)

    for i in range(0, len(friendslist)):
        alias_list.append(friendslist[i].user_friend_id)
    for u in alias_list:    
        my_friend.append(User.objects.get(id=u ))
        # my_friend.append(u)
        # print(my_friend)

    context={
        'user':user,
        'friends': my_friend,
        'nonfriends': nonfriends,
    }
    return render(request, 'index.html', context)

# @admin_requerido
# def administrador(request):

#     context = {
#         'saludo': 'ADMINISTRADOR'
#     }
#     return render(request, 'admin.html', context)




@ login_required
def addFriend(request, id):
    user=User.objects.get(id=request.session['usuario']['id'])
    friend = User.objects.get(id=id)
    Friend.objects.create(user_friend=user, second_friend=friend)
    Friend.objects.create(user_friend=friend, second_friend=user)
    return redirect('/')

@ login_required
def removeFriend(request, id):
    user=User.objects.get(id=request.session['usuario']['id'])
    friend = User.objects.get(id=id)
    friendship=Friend.objects.get(user_friend=user, second_friend=friend)
    friendship1=Friend.objects.get(user_friend=friend, second_friend=user)
    friendship.delete()
    friendship1.delete()
    return redirect('/')

@login_required
def profile(request,id):
    user = User.objects.get(id=id)
    context = {
        'user':user,
        
    }

    return render(request, 'profile.html',context)