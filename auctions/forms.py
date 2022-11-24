# import form class from Django
from django import forms
from django.forms import models

from .models import Auction
from .models import Bid
from .models import Comment

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

# model form for Comment.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']