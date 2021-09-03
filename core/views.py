from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required, admin_requerido
from .models import*


@login_required
def index(request):
    user = User.objects.get(id=request.session['usuario']['id'])
    friends = Friend.objects.all().exclude(user_friend=user.id)
    friendslist = []
    for x in friends:
        friendslist.append(x)
    nonfriends = User.objects.all().exclude(id=user.id)
    for x in friendslist:
        nonfriends = nonfriends.exclude(id=x.user_friend.id)
    # alias_list=[]
    # u= friends['alias']
    # for friend in u:
    #     print(f'{friend.user_friend_id}')
    alias_list = []
    my_friend = []
    for i in range(0, len(friendslist)):
        alias_list.append(friendslist[i].user_friend_id)
    for u in alias_list:
        my_friend.append(User.objects.get(id =u ).alias)
    context={
        'user': request.session['usuario']['id'],
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

def add_Friend(user_id, friend_id):
    user=User.objects.get(id=user_id)
    friend=User.objects.get(id=friend_id)
    Friend.objects.create(user_friend=user, second_friend=friend)
    Friend.objects.create(user_friend=friend, second_friend=user)

def remove_Friend(user_id, friend_id):
    user=Friend.objects.get(id=user_id)
    friend=Friend.objects.get(id=friend_id)
    friendship=Friend.objects.get(user_friend=user, second_friend=friend)
    friendship1=Friend.objects.get(user_friend=friend, second_friend=user)
    friendship.delete()
    friendship1.delete()



@ login_required
def addFriend(request, id):
    user_id=request.session['usuario']['id']
    friend_id=id
    add_Friend(user_id, friend_id)
    return redirect('/')

@ login_required
def removeFriend(request, id):
    user_id=request.session['usuario']['id']
    friend_id=id
    remove_Friend(user_id, friend_id)
    return redirect('/')
