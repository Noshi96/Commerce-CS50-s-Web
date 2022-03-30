from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>", views.choosen_category, name="choosen_category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path('add_to_watchlist/<int:listing_id>', views.add_to_watchlist, name="add_to_watchlist"),
    path('delete_from_watchlist/<int:listing_id>', views.delete_from_watchlist, name="delete_from_watchlist"),
    path('create_listing', views.create_listing, name="create_listing"),
    path('listings/<int:listing_id>', views.listing, name="listing"),
    path('<int:listing_id>', views.bid, name="bid"),
    path('comment/<int:listing_id>', views.comment, name="comment"),
    path('accounts/login/', views.login_view, name="permission"),
    path('close_auction/<int:listing_id>', views.close_auction, name="close_auction")
]
