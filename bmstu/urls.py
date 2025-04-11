from django.urls import path
from bmstu.views import *

app_name = 'bmstu'

urlpatterns = [
    path('', home, name='home'),
    path('homework/', homeworks, name='homework'),
    path('lecture/', lecture, name='lecture'),
    path('stat/', stata, name='stats'),
    path('balance/', balance, name='balance'),
    path('homework/<int:homework_id>/vote/', vote_homework, name='vote_homework'),
    path('lecture/<int:lecture_id>/vote/', vote_lecture, name='vote_lecture'),
] 