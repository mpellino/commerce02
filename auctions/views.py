from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ValidationError
from .forms import AuctionForm
from .forms import BidForm
from .models import User, Auction, Watchlist,Bid


def index(request):
    context = {"auctions": Auction.objects.all()}
    return render(request, "auctions/index.html", context)


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


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            valid_form = form.save(commit=False)
            valid_form.seller = request.user
            valid_form.save()
            return HttpResponse('Hurray, saved!')

    else:
        form = AuctionForm()
        print("form created?")
    return render(request, "auctions/create_listing.html", {'form': form})


@login_required
# Listing sends also the Bid Form!
def listing(request, listing_id ):
    listing_object = Auction.objects.get(pk=listing_id)
    # Get the highest bit, if exists.Otherwise, set value to zero
    try:
        auction_highest_bid = Bid.objects.filter(auction=listing_object).filter() \
            .values_list('value', flat=True).latest()
    except Bid.DoesNotExist:
        auction_highest_bid = 0
    # Create contex
    context = {'auction': listing_object, 'form': BidForm(), 'higher_bid': auction_highest_bid}
    # If winner exist, and it is the same as logged-in user, add congratulation message to context
    if listing_object.winner == request.user:
        context['winner_message'] = "Congratulation! You won this auction!"
    return render(request, "auctions/listing.html", context)


@login_required
def close_bid(request, listing_id):
    # close bid
    if request.method == "POST":
        print("post")
        auction_object = Auction.objects.get(pk=listing_id)
        auction_object.active = False
    # assign winner
        # get the winner id starting from the Bid Model, get the auction ordered by value (of the bid) and select the
        # last bidder
        winner = User.objects.filter(bidder__auction_id=listing_id).order_by('bidder__value').last()
        auction_object.winner = winner
        auction_object.save()
    else:
        print("something is wrong")
    return HttpResponse("done")


@login_required
def watchlist(request):
    auction_objects = Auction.objects.filter(auction_watchlist__user_id=request.user.id)
    context = {'watchlist_auctions': auction_objects}
    return render(request, "auctions/watchlist.html", context)


@login_required
def add_remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        listing_object = Auction.objects.get(pk=listing_id)
        new_wishlist_item = Watchlist(user=request.user, auction=listing_object)
        # the constraints are in the Meta class of the Model. The check to see whether the item is already
        # present in the Model is performed by the model method.
        # if Item and user are not in the Watchlist Model, item is added, if exception is raised then item
        # and user are already presents so the item is removed.
        # TODO: test if it works when there are 2 user with the same item. Make sure it does not delete for both
        try:
            new_wishlist_item.validate_constraints()
            new_wishlist_item.save()
            return render(request, "auctions/index.html", {'message': "Item has been added to the Watchlist"})
        except ValidationError:
            current_wishlist_item = Watchlist.objects.get(user=request.user, auction=listing_object)
            current_wishlist_item.delete()
            return render(request, "auctions/index.html", {'message': "Item has been removed from the Watchlist"})
    return HttpResponseRedirect(reverse("index"))


@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing_object = Auction.objects.get(pk=listing_id)
        print(f"the view listing_object: {listing_object}")
        partial_bid = Bid(bidder=request.user, auction=listing_object)
        form = BidForm(request.POST, instance= partial_bid)
        try:
            auction_highest_bid = Bid.objects.filter(auction=listing_object) \
                .values_list('value', flat=True).latest()
        except Bid.DoesNotExist:
            auction_highest_bid = 0
        if form.is_valid():
            form.save()
            context = {'auction': listing_object, 'message': " The Bid was successfully placed! Good luck",
                       'higher_bid': auction_highest_bid}
            return render(request, "auctions/listing.html", context)
        else:
            # if form is not valid according to the Model constrains, return the listing.html passing back the
            # form, The form has all the errors, and they are displayed automagically in the template.
            context = {'auction': listing_object, 'form': form, 'higher_bid': auction_highest_bid}
            return render(request, "auctions/listing.html", context)


def category(request, category_code):
    listing_objects = Auction.objects.filter(category__iexact=category_code).all() or None
    first_object = Auction.objects.filter(category__iexact=category_code).first() or None
    if first_object:
        category = first_object.get_category_display()
    else:
        category = "No Item for the chosen category"
    context = {"auctions": listing_objects, "category": category}
    return render(request, "auctions/index.html", context)
