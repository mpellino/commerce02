from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    # model is inherited from Django
    pass


'''
Model Category

'''


class Category(models.Model):
    ELECTRONICS = 'ELE'
    COLLECTIBLES_ART = 'COA'
    HOME_GARDEN = 'HOG'
    CLOTHING_SHOES_ACCESSORIES = 'CSA'
    TOYS_HOBBIES = 'TOH'
    SPORTING_GOODS = 'SPO'
    BOOKS_MOVIES_MUSIC = 'BMM'
    HEALTH_BEAUTY = 'HEB'
    BUSINESS_INDUSTRIAL = 'BUI'
    BABY_ESSENTIALS = 'BAB'
    PET_SUPPLY = 'PET'
    OTHER = 'OTH'

    CATEGORY_CHOICES = [
        (ELECTRONICS, 'Electronics'),
        (COLLECTIBLES_ART, 'Collectibles & Art'),
        (HOME_GARDEN, 'Home & Garden'),
        (CLOTHING_SHOES_ACCESSORIES, 'Clothing, Shoes & Accessories'),
        (TOYS_HOBBIES, 'Toys & Hobbies'),
        (SPORTING_GOODS, 'Sporting Goods'),
        (BOOKS_MOVIES_MUSIC, 'Books, Movies & Music'),
        (HEALTH_BEAUTY, 'Health & Beauty'),
        (BUSINESS_INDUSTRIAL, 'Business & Industrial'),
        (BABY_ESSENTIALS, 'Baby Essentials'),
        (PET_SUPPLY, 'Pet Supply'),
        (OTHER, 'Other')
    ]
    Category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default=OTHER)

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        pass
        # return reverse('view_name', )  # TODO:maybe not be necessary If no need to display a page with the categories


''' 
Model Auction: 
seller --> User related_name="seller"
title
description
initial price (default 0)
image (optional)
category >--< Category (many to many) related_name="category"
posting_date (automatic)
active (boolean)
'''


class Auction(models.Model):
    ELECTRONICS = 'ELE'
    COLLECTIBLES_ART = 'COA'
    HOME_GARDEN = 'HOG'
    CLOTHING_SHOES_ACCESSORIES = 'CSA'
    TOYS_HOBBIES = 'TOH'
    SPORTING_GOODS = 'SPO'
    BOOKS_MOVIES_MUSIC = 'BMM'
    HEALTH_BEAUTY = 'HEB'
    BUSINESS_INDUSTRIAL = 'BUI'
    BABY_ESSENTIALS = 'BAB'
    PET_SUPPLY = 'PET'
    OTHER = 'OTH'

    CATEGORY_CHOICES = [
        (ELECTRONICS, 'Electronics'),
        (COLLECTIBLES_ART, 'Collectibles & Art'),
        (HOME_GARDEN, 'Home & Garden'),
        (CLOTHING_SHOES_ACCESSORIES, 'Clothing, Shoes & Accessories'),
        (TOYS_HOBBIES, 'Toys & Hobbies'),
        (SPORTING_GOODS, 'Sporting Goods'),
        (BOOKS_MOVIES_MUSIC, 'Books, Movies & Music'),
        (HEALTH_BEAUTY, 'Health & Beauty'),
        (BUSINESS_INDUSTRIAL, 'Business & Industrial'),
        (BABY_ESSENTIALS, 'Baby Essentials'),
        (PET_SUPPLY, 'Pet Supply'),
        (OTHER, 'Other')
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")  # from a user i can access all
    # the auction that user is a seller of
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512, blank=True)  # description is optional
    initial_price = models.DecimalField(max_digits=6, decimal_places=2,
                                        default=0,
                                        validators=[MinValueValidator(0.1)])

    image = models.ImageField(blank=True)  # image is optional
    category = models.CharField(choices=CATEGORY_CHOICES, default=OTHER, max_length= 3)  # if I have a
    # category I can access all the auctions that category is a category of.
    posting_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # TODO make this field invisible.

    def __str__(self):
        return f"{self.title}. Seller: {self.seller}, posted on {self.posting_date}"

    def get_absolute_url(self):
        return reverse('view_name', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Auction"
        verbose_name_plural = "Auctions"


'''
Model Bid:
bidder --> User related_name="bidder"
auction --> Auction related_name="auction"
value
bidding date
'''


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid_auction")
    value = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0.1)])
    bidding_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of {self.value}, made by: {self.bidder} in date: {self.bidding_date}"

    class Meta:
        get_latest_by = "value"
        verbose_name = "Bid"
        verbose_name_plural = "Bids"


'''
Model Comment:
commenter --> User related_name="commenter"
auction --> auction related_name="comment_auction"
content
'''


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment_auction")
    content = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.commenter} commented on {self.auction}: {self.content}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


'''
Model Watchlist:
user --> User related_name='user_watchlist'
auction --> Auction related_name='auction_watchlist'
'''


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_watchlist')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='auction_watchlist')

    def __str__(self):
        return f"{self.auction} in {self.user} watchlist"

    def get_absolute_url(self):
        return reverse('view name', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Watchlist'
        verbose_name_plural = 'Watchlist'
        constraints = [models.UniqueConstraint(fields=['user', 'auction'], name="no_doubles")]
