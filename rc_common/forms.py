from django import forms

from .utilitties import CommonUtility

class CommonConfigurationForm(forms.Form):
    record_sections = forms.CharField(help_text='Please Enter Each Section Seperated by Comma',widget=forms.Textarea(attrs={'class' : 'co-twelve','rows':'4'}))
    record_categories = forms.CharField(help_text='Please Enter Each Category Seperated by Comma',widget=forms.Textarea(attrs={'class' : 'co-twelve','rows':'4'}))

    def save(self):
        CommonUtility().save_config(self.cleaned_data)

class CommonResetForm(forms.Form):
    bundle = forms.BooleanField(label='Reset Bundles',required=False)
    issues = forms.BooleanField(label='Reset Issue Details',required=False)
    allrecords = forms.BooleanField(label='Reset All Tables',required=False)