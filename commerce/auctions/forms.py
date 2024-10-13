from django import forms
from auctions.models import Auction
from django.forms import ModelForm
from django.forms.utils import ErrorList

"""
class AuctionCreationForm(forms.Form):
    title = forms.CharField(label="Auction Title", max_length=64)
    description = forms.CharField(label="Desription", max_length=1000)

    # update with attr?
    start_bit = forms.FloatField(label="starting bit", min_value=1) 
    img_link = forms.URLField(label="image_url", required=False)

"""

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="error alert alert-danger mt-1">%s</div>' % e for e in self])

class AuctionCreationForm(ModelForm):
    class Meta:
        model = Auction
        fields = ["owner", "title", "description", "bit", "img_link"]
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
        error_class = DivErrorList

