from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/add_remove_watchlist", views.add_remove_from_watchlist, name="add_remove_from_watchlist"),
    path("<int:listing_id>/bid", views.bid, name='bid'),
    path("<int:listing_id>/closing_bid", views.close_bid , name="close_bid")
    # TODO: url with listing_id as optional argument. if argument then add/remove, show a list otherwise
]
