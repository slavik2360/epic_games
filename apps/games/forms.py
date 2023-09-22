from django.forms import ModelForm

from games.models import Game, Balance, Comment, Deal


class CreateForm(ModelForm):
    class Meta:
        model = Game
        fields = (
            'name',
            'price',
            'poster',
            'rate'
        )

class AddBalanceForm(ModelForm):
    class Meta:
        model = Balance
        fields = (
            'user',
            'wallet'
        )

class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = (
            'user',
            'text',
            'game'
        )

class DealForm(ModelForm):
    class Meta:
        model = Deal
        fields = (
            'user',
            'game',
            'amount'
        )