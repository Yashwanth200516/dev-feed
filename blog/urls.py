from django.urls import path
from .views import *

urlpatterns=[
    path('',home,name='home'),
    path('post/<int:id>/',post_detail,name='post'),
    path('add-post/',add_post,name='add_post'),
    path('delete/<int:id>/',delete,name='delete'),
    path('edit/<int:id>/',edit,name='edit'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('profile/<str:username>/',user_profile,name='profile'),
    path('like/<int:id>/',like_post, name='like'),
]