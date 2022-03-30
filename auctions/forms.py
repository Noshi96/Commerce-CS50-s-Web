from django import forms
from auctions.models import Category
from auctions.utils import categories

class AuctionForm(forms.Form):
    category = forms.ChoiceField(label="Category", widget=forms.Select, choices=categories())
    price = forms.FloatField(label="Price", widget=forms.NumberInput(attrs={'placeholder': 'Price'}))
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(label="Description", max_length=300, widget=forms.Textarea)
    url = forms.CharField(label="Image URL address ", max_length=1024, required = False)

class BidForm(forms.Form):
    placed_price = forms.FloatField(label="Bid", widget=forms.NumberInput(attrs={'placeholder': 'Bid', 'class': 'form-control'}))

class CommentForm(forms.Form):
    cotnent = forms.CharField(label="Add comment", max_length=300, widget=forms.Textarea(attrs={'placeholder': 'Write comment','class': 'form-control'}))