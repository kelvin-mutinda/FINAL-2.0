from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, role=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username, role=role)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None