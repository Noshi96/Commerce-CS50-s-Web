from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField


class Category(models.Model):
    category_name = models.CharField(max_length=32, default="")

    def __str__(self):
        return f"{self.id}: {self.category_name}"

class Listing(models.Model):
    owner_user = models.IntegerField(default="", blank=True, null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories", default="")
    title = models.CharField(max_length=64, default="")
    description = models.CharField(max_length=300, default="")
    current_price = models.FloatField(default="")
    is_active = models.BooleanField(default="True", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    url_image = models.CharField(max_length=1024, default="https://www.weddingsbylomastravel.com/images/paquetes/default.jpg", blank=True, null=True)

    def __str__(self):
        return f"Id:{self.id}, Owner_id: {self.owner_user}, Title: {self.title}, Current price: {self.current_price}, Is active: {self.is_active}, Date: {self.created_date}"

class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, related_name="watchlist_set", default="", blank=True, null=True)

    def __str__(self):
        return f"{self.username}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment", default="")
    content = models.CharField(max_length=300, default="")
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default="", blank=True, null=True)

    def __str__(self):
        return f"{self.id}, {self.user.username}, {self.content}, {self.created_date}, {self.listing.title}, {self.listing.id}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid", default="")
    placed_price = models.FloatField(default="")
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default="", blank=True, null=True)

    def __str__(self):
        return f"{self.id}, {self.user.username}, {self.placed_price}, {self.created_date}, Listing id: {self.listing.id}, Title: {self.listing.title}"
