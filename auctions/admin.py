from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.

from .models import User, Auction, Watchlist

admin.site.register(User, UserAdmin)
admin.site.register(Auction)
admin.site.register(Watchlist)
