from django import forms

class RegisterForm(forms.Form):
    """
        Register form for each user.
        For more information about creating forms and working with them check Django documentation.
    """

    username = forms.CharField(
        label='Enter your username:',
        min_length=8,
        max_length=50,
        required=True,
        help_text='Your username must be at least 8 characters long.'
        )
    password = forms.CharField(
        label='Enter your password:',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=20,
        required=True,
        help_text='Your password must be at least 8 characters long and do not contain !@#$%^&()~`<>?/\\{}[]:;\"\' characters.')
    repeat_pass = forms.CharField(label='Repeat your password', widget=forms.PasswordInput, min_length=8, max_length=20, required=True)
    email = forms.EmailField(label='Your email address', required=True)