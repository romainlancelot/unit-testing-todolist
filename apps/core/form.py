from django import forms


class ItemForm(forms.Form):
    name: forms.CharField = forms.CharField(max_length=100)
    content: forms.CharField = forms.CharField(widget=forms.Textarea)


class UserForm(forms.Form):
    username: forms.CharField = forms.CharField(max_length=100, min_length=5)
    email: forms.CharField = forms.EmailField(max_length=100, required=True)
    password: forms.CharField = forms.CharField(
        max_length=100, widget=forms.PasswordInput, min_length=8
    )
