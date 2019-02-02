from django import forms
from complexTable.models import PostHistogram

class HistForm(forms.Form):
    mincutoff = forms.FloatField(label='min cutoff', required=False)
    maxcutoff = forms.FloatField(label='max cutoff', required=False)

class CheckForm(forms.Form):
    choices = forms.MultipleChoiceField(
        # choices = LIST_OF_VALID_CHOICES, # this is optional
        widget  = forms.CheckboxSelectMultiple,
    )