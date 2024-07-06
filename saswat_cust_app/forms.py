# forms.py
from django import forms
from django.forms import ModelChoiceField
from .models import QueryModel, ShortenedQueries


class QueryModelForm(forms.ModelForm):
    description = forms.ModelChoiceField(
        queryset=ShortenedQueries.objects.exclude(description__isnull=True).exclude(description=''),
        label="Description",
        required=False
    )
    additional_info = forms.ModelChoiceField(
        queryset=ShortenedQueries.objects.exclude(additional_info__isnull=True).exclude(additional_info=''),
        label="Additional Info",
        required=False
    )

    class Meta:
        model = QueryModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize label for each dropdown
        self.fields['description'].label_from_instance = lambda obj: obj.description
        self.fields['additional_info'].label_from_instance = lambda obj: obj.additional_info