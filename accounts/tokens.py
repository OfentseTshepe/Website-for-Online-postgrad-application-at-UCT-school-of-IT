from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

# token generator class from django
# https://github.com/django/django/blob/master/django/contrib/auth/tokens.py#L8

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()