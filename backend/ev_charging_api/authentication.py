# pylint: disable= R1720
from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import TokenAuthentication

AUTHORIZATION_HEADER = "HTTP_X_OBSERVATORY_AUTH"


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get(AUTHORIZATION_HEADER, b"")
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    print(auth * 100)
    return auth


class CustomTokenAuthentication(TokenAuthentication):
    """DRF TokenAuthentication that uses X-OBSERVATORY-AUTH Authorization header."""

    def authenticate(self, request):
        """Authenticate request.

        Identical to DRF's implementation except we use a different
        `get_authorization_header` function
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                "Invalid token header. Token string should not contain invalid characters."
            )  # noqa: E501
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
