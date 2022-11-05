from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # model is inherited from Django
    pass


class Category(models.Model):
    Category = models.CharField() # TODO: make a list of few categories

    def __str__(self):
        return self.category


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE(), related_name="seller")  # from a user i can access all
    # the listing that user is a seller of
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512, blank=True)  # description is optional
    initial_price = models.PositiveIntegerField(default=0)
    image = models.ImageField(blank=True)  # image is optional
    category = models.ManyToManyField(Category, on_delete=models.CASCADE(), related_name="category")  # if I have a
    # category I can access all the listings that category is a category of.
    posting_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title}. Seller: {self.seller}, posted on {self.date_of_posting}"


class Bid(models.Model): # TODO
    bidder = models.ForeignKey(User, on_delete=models.CASCADE(), related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE(), related_name="listing")
    value = models.PositiveIntegerField()
    bidding_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of {self.value}, made by: {self.bidder} in date: {self.date_of_bid}"


class Comment(models.Model): # TODO
    commenter = models.ForeignKey(User, on_delete=models.CASCADE(), related_name="commenter")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE(), related_name="listing")
    content = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.commenter} commented on {self.listing}: {self.content}"

