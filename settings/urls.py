from django.contrib import admin
from django.urls import path

from apps.games.views import (
    GameView, 
    UserView,
    BalanceView,
    CommentView,
    DealView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    *GameView.as_my_view('game/'),
    *UserView.as_my_view('profile/'),
    *BalanceView.as_my_view('balance'),
    *CommentView.as_my_view('comment'),
    *DealView.as_my_view('deal'),
]
