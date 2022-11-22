# import form class from Django
from django import forms
from django.forms import models

from .models import Auction
from .models import Bid


# model for for Auction
class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title','description','category','initial_price', 'image']


# model form for Bid.
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['value']