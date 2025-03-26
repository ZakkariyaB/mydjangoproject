from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group

class AddUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["group"] = forms.ChoiceField(choices=Group.objects.values_list('id','name'),widget=forms.Select(attrs={'class':'co-twelve'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )
    
    def save(self,*args,**kwargs):
        user = super(AddUserForm,self).save(*args,**kwargs)
        if 'group' in self.cleaned_data and self.cleaned_data['group']:
            user_group = Group.objects.filter(id=self.cleaned_data['group']).first()
            if user_group:
                user.groups.add(user_group)