from django.urls import path
from . import views
from .views import *

app_name = 'users'

urlpatterns = [
    path('profile/', profile,name='profile'),
    path('signup/', signup,name='signup'),
    path('login/', login,name='login'),
    path('logout/', logout,name='logout'),
    path('profile/<int:user_id>/', view_profile, name='profile'),
] 