from django import forms
from auctions.models import Auction
from django.forms import ModelForm

"""
class AuctionCreationForm(forms.Form):
    title = forms.CharField(label="Auction Title", max_length=64)
    description = forms.CharField(label="Desription", max_length=1000)

    # update with attr?
    start_bit = forms.FloatField(label="starting bit", min_value=1) 
    img_link = forms.URLField(label="image_url", required=False)

"""

class AuctionCreationForm(ModelForm):
    class Meta:
        model = Auction
        fields = ["owner", "title", "description", "starting_bit", "img_link"]
        exclude = ["owner"]
        labels = {
                "title": ("Title"),
                "description": ("Description"),
                "starting_bit": ("Starting Bit"),
                "img_link": ("Link to Image")
            }

        error_messages = {
            "name": {
                "max_length": ("This Title is too long."),
            },
            "description": {
                "max_length": ("Description too long (512 chars)")
            }
        }
    