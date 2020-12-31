from django import forms
from .models import Owner, Company, Share

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class ShareForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Share
        fields = '__all__'