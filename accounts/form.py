from django import forms
from .models import Image
from django.utils.translation import gettext_lazy as _

class ImageForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=("caption","image")

class CouponApplyForm(forms.Form):
    code = forms.CharField(label=_('Coupon'))