from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index), 
    path('registro/', auth.registro),
    path('login/', auth.login),
    path('logout/', auth.logout),
    path('addfriend/<int:id>', views.addFriend),
    path('removefriend/<int:id>',views.removeFriend),
    path('user/<int:id>',views.profile),
    
    # path()
]
