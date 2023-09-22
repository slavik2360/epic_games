from abstracts.views import CRUDView
from games.models import Game, Balance, Comment, Deal, MyUser
from games.forms import CreateForm, AddBalanceForm, AddCommentForm, DealForm


class GameView(CRUDView):
    model = Game
    form = CreateForm
    template_create = 'create_game.html'
    template_list = 'list_game.html'


class UserView(CRUDView):
    model=MyUser
    template_list = 'user_profile.html'


class BalanceView(CRUDView):
    model = Balance
    form = AddBalanceForm
    template_create = 'balance.html'

class CommentView(CRUDView):
    model = Comment
    form = AddCommentForm
    template_create = 'comment.html'

class DealView(CRUDView):
    model = Deal
    form = DealForm
    template_create = 'deal.html'