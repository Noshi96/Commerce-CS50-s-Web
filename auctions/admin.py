from django.contrib import admin
from .models import Category, User, Listing, Bid, Comment
# Register your models here.

class CommentInLine(admin.TabularInline):
    model = Comment

class BidInLine(admin.TabularInline):
    model = Bid

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner_user", "categories", "current_price", "created_date", "is_active")

    inlines = [
        CommentInLine,
        BidInLine,
    ]

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "created_date", "listing")

class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "placed_price", "created_date", "listing")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")


admin.site.register(Category, CategoryAdmin)
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)


