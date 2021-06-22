from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({'placeholder': 'username'})
        self.fields["email"].widget.attrs.update({'placeholder': 'example@email.com'})
        self.fields["password1"].widget.attrs.update({'placeholder': 'password'})
        self.fields["password2"].widget.attrs.update({'placeholder': 'confirm password'})

        self.fields["username"].label = ""
        self.fields["email"].label = ""
        self.fields["password1"].label = ""
        self.fields["password2"].label = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""
