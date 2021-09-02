from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index), 
    path('administrador/', views.administrador), 
    path('registro/', auth.registro),
    path('login/', auth.login),
    path('logout/', auth.logout),
    # path()
]
