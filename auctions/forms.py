# import form class from Django
from django import  forms

#import models
from .models import Auction

# model for for Auction
class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title','description','category','initial_price', 'image']