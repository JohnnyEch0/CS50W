from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("error/<str:message>", views.error, name="error"),
    path("create_auction", views.create_auction, name="create_auction"),
    path("listing/<int:auction_id>", views.listing, name="listing"),
    path("listing/place_bid/<int:auction_id>", views.place_bid, name="place_bid"),
    path("add_to_wishlist/<int:auction_id>", views.add_to_wishlist, name="add_to_wishlist"),
    path("remove_from_wishlist/<int:auction_id>", views.remove_from_wishlist, name="remove_from_wishlist")
]
