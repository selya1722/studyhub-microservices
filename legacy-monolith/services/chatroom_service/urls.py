from django.urls import path
from . views import *

urlpatterns = [
    path('', home, name = 'home'),

    path('room/<int:pk>/', room, name = 'room'),
    path('create-room/', createRoom, name = 'create-room'),
    path('update-room/<int:pk>/', updateRoom, name = 'update-room'),
    path('delete-room/<int:pk>/', deleteRoom, name = 'delete-room'),

    path('delete-message/<int:pk>/', deleteMessage, name = 'delete-message'),

    path('topics/', topicView, name = 'topic-view'),
    path('activities/', activityView, name = 'activity-view'),

    path('start/', start, name='start'),
    path('ready/', ready, name='ready'),
    path('live/', live, name='live'),
]
