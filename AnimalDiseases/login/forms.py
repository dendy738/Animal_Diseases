from django import forms

class LoginForm(forms.Form):
    """
        Login form.
        For more information about creating forms and working with them check Django documentation.
    """
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=20)