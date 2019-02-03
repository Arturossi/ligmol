from django import forms
# from complexTable.models import PostHistogram

class HistForm(forms.Form):
    mincutoff = forms.FloatField(label='min cutoff', required=False)
    maxcutoff = forms.FloatField(label='max cutoff', required=False)

class CheckForm(forms.Form):
    choices = forms.MultipleChoiceField(
        widget = forms.CheckboxSelectMultiple(),
        choices = list(map(list, zip(*[list(range(0, 100000)),list(range(0, 100000))])))
    )