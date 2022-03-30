from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .forms import AuctionForm, BidForm, CommentForm
from django.contrib.auth.decorators import login_required

from auctions.models import Listing
from auctions.models import Category
from auctions.models import User

from .models import User


def index(request):
    wachlist_items_count = 0
    if request.user.is_authenticated:
        wachlist_items_count = User.objects.get(pk=request.user.id).watchlist.all().count()
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all(),
        'wachlist_items_count': wachlist_items_count
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = AuctionForm(request.POST)
            if form.is_valid():
                category = Category.objects.get(category_name=dict(form.fields["category"].choices)[form.data["category"]])
                price = form.cleaned_data.get('price')
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                url = form.cleaned_data.get('url')
                if not url:
                    url = "https://www.weddingsbylomastravel.com/images/paquetes/default.jpg"
                listing = Listing(categories=category, current_price=price, title=title, description=description, url_image=url, owner_user=int(request.user.id))
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        form = AuctionForm()
    return render(request, "auctions/create-listing.html", {
        "form": form
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all(),
    })

def choosen_category(request, category_id):
    
    filtered_categories = Listing.objects.filter(categories_id__exact = category_id)
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all(),
        'filtered_categories': filtered_categories
    })
    #return HttpResponseRedirect(reverse("categories", args=(category_name)))

def watchlist(request):
    wachlist_items_count = 0     
    if request.user.is_authenticated:
        wachlist_items_count = User.objects.get(pk=request.user.id).watchlist.all().count()
        user = User.objects.get(pk=request.user.id)
        return render(request, "auctions/watchlist.html", {
            'watchlist': user.watchlist.all(),
            'wachlist_items_count':wachlist_items_count
        })

@login_required
def add_to_watchlist(request, listing_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            listing = Listing.objects.get(pk=listing_id)
            user = User.objects.get(pk=request.user.id)
            user.watchlist.add(listing)
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required
def delete_from_watchlist(request, listing_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(pk=request.user.id)
            listing = Listing.objects.get(pk=listing_id)
            user.watchlist.remove(listing)
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))    

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid_form = BidForm()
    comment_form = CommentForm()
    is_on_watchlist = False
    wachlist_items_count = 0

    if request.user.is_authenticated:
        wachlist_items_count = User.objects.get(pk=request.user.id).watchlist.all().count()
        user = User.objects.get(pk=request.user.id)
        watchlist = Listing.objects.filter(pk=listing_id)
        if user.watchlist.filter(id__in=watchlist):
            is_on_watchlist = True

    return render(request, "auctions/listing.html", {
        'listing': listing,
        'bids': listing.bid_set.all(),
        'comments': listing.comment_set.all(),
        'bid_form': bid_form,
        'comment_form': comment_form,
        'is_on_watchlist': is_on_watchlist,
        'wachlist_items_count': wachlist_items_count,
    })

@login_required
def bid(request, listing_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            listing = Listing.objects.get(pk=listing_id)
            form = BidForm(request.POST)
            if form.is_valid():
                if float(form.cleaned_data.get('placed_price')) <= float(listing.current_price):
                    messages.info(request, 'Bid must be greater than current price!')
                else:
                    listing.current_price = float(form.cleaned_data.get('placed_price'))
                    listing.save(update_fields=['current_price'])
                    listing.bid_set.create(user=request.user, placed_price=form.cleaned_data.get('placed_price'))
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required
def comment(request, listing_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            listing = Listing.objects.get(pk=listing_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = listing.comment_set.create(user=request.user, content=form.cleaned_data.get('cotnent'))
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save(update_fields=['is_active'])
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))