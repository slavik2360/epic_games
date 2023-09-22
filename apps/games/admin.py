from django.contrib import admin

from games.models import (
    MyUser,
    Game,
    Balance,
    Comment,
    Deal
)

admin.site.register(MyUser)
admin.site.register(Game)
admin.site.register(Balance)
admin.site.register(Comment)
admin.site.register(Deal)

