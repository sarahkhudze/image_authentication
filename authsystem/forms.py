from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.validators import RegexValidator
from .models import UserImage
from django.core.exceptions import ValidationError
from .validators import SpecialCharacterValidator
from .utils import calculate_hash

class CustomUserCreationForm(UserCreationForm):
    telephone = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        help_text="Format: +999999999. Up to 15 digits allowed."
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=SpecialCharacterValidator().get_help_text()
    )
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validator = SpecialCharacterValidator()
        validator.validate(password1)
        return password1
    
    id_number = forms.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'telephone', 'id_number', 'password1', 'password2')

class LoginForm(forms.Form):
    telephone = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    password = forms.CharField(widget=forms.PasswordInput)

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['image']
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            image_hash = calculate_hash(image)
            if UserImage.objects.filter(image_hash=image_hash).exists():
                raise forms.ValidationError("This image has already been uploaded by another user")
        return image