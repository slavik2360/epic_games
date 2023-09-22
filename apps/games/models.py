"""MODELS AUTHS"""
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class MyUserManager(BaseUserManager):
    """ClientManager."""

    def create_user(
        self,
        email: str,
        password: str
    ) -> 'MyUser':

        if not email:
            raise ValidationError('Email required')
        
        if self.model.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')

        custom_user: 'MyUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return custom_user

    def create_superuser(
        self,
        email: str,
        password: str
    ) -> 'MyUser':

        custom_user: 'MyUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        custom_user.is_superuser = True
        custom_user.is_active = True
        custom_user.is_staff = True
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return custom_user
    


class MyUser(AbstractBaseUser, PermissionsMixin):

    class Currencies(models.TextChoices):
        TENGE = 'KZT', 'Tenge'
        RUBLI = 'RUB', 'Rubli'
        EURO = 'EUR', 'Euro'
        DOLLAR = 'USD', 'Dollar'

    email = models.EmailField(
        verbose_name='почта/логин',
        unique=True,
        max_length=200
    )
    nickname = models.CharField(
        verbose_name='ник',
        max_length=120
    )
    currency = models.CharField(
        verbose_name='валюта',
        max_length=4,
        choices=Currencies.choices,
        default=Currencies.TENGE
    )
    is_staff = models.BooleanField(
        default=False
    )

    objects = MyUserManager()

    @property
    def balance(self) -> float:
        transactions: QuerySet[Deal] = \
            Deal.objects.filter(user=self.pk)
        result: float = 0
        for trans in transactions:
            if trans.is_filled:
                result += trans.amount
            else:
                result -= trans.amount
        return result

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Game(models.Model):
    """MY GAME!"""

    name: str = models.CharField(
        verbose_name='игра',
        max_length=200
    )
    price: float = models.DecimalField(
        verbose_name='цена',
        max_digits=11,
        decimal_places=2,
        validators=[
            MinValueValidator(0, message='Мы деньги за игры не даём!')
        ]
    )
    poster: str = models.ImageField(
        verbose_name='постер',
        upload_to='posters'
    )
    rate: float = models.FloatField(
        verbose_name='рейтинг',
        max_length=5
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'игра'
        verbose_name_plural = 'игры'


class Balance(models.Model):
    """USER BALANCE"""

    user = models.ForeignKey(
        verbose_name='чей счет',
        to=MyUser,
        related_name='who',
        on_delete=models.PROTECT
    )
    wallet: float = models.DecimalField(
        verbose_name='баланс',
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'баланс'
        verbose_name_plural = 'баланс'


class Comment(models.Model):
    """COMMENT to GAME"""
    
    user = models.ForeignKey(
        verbose_name='кто оставил',
        to=MyUser,
        on_delete=models.PROTECT,
        related_name='user_comment'
    )
    text = models.CharField(
        verbose_name='текст',
        max_length=254
    )
    game = models.ForeignKey(
        verbose_name='игра',
        related_name='game_comment',
        to=Game,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
    

class Deal(models.Model):

    user = models.ForeignKey(
        verbose_name='пользователь',
        related_name='deals',
        to=MyUser, 
        on_delete=models.PROTECT
    )
    game = models.ForeignKey(
        verbose_name='игра',
        to=Game, 
        on_delete=models.CASCADE,
        related_name='game_order'
    )
    datetime_buy = models.DateTimeField(
        verbose_name='время совершения покупки',
        auto_now_add=True
    )
    amount = models.DecimalField(
        verbose_name='сумма',
        decimal_places=2,
        max_digits=12
    )
    
    class Meta:
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'
