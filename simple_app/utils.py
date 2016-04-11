import urllib.request

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import CharField


class ReliableUrlValidator(URLValidator):
    schemes = ['https']

    def __call__(self, value):
        super().__call__(value)
        if not self.available_on_the_internet(value):
            raise ValidationError("The response from domain doesn't seems to be positive.")

    @staticmethod
    def available_on_the_internet(url):
        try:
            with urllib.request.urlopen(url, timeout=3) as conn:
                return conn.getcode() == 200
        except Exception:
            return False


class SecureUrlField(CharField):
    default_validators = [ReliableUrlValidator()]
