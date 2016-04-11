from django.db.models import BooleanField, Model

from simple_app.utils import SecureUrlField


class Domain(Model):

    name = SecureUrlField(max_length=255)
    is_private = BooleanField(default=False)
