from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class TelephoneBackend(ModelBackend):
    def authenticate(self, request, telephone=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(telephone=telephone)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
        return None