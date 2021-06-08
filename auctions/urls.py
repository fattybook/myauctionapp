from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("<int:listing_id>/close_listing", views.close_listing, name="close_listing"),
    path("my_winnings", views.my_winnings, name="my_winnings"),
    path("<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
]
