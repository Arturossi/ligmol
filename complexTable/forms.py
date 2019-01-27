from django import forms
from complexTable.models import PostHistogram

class HistForm(forms.Form):
    mincutoff = forms.FloatField(label='min cutoff', required=False)
    maxcutoff = forms.FloatField(label='max cutoff', required=False)
