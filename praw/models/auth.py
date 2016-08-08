"""Provide the Auth class."""
from prawcore import ImplicitAuthorizer, UntrustedAuthenticator, session

from .base import PRAWBase
from ..exceptions import ClientException


class Auth(PRAWBase):
    """Auth provides an interface to Reddit's authorization."""

    def implicit(self, access_token, expires_in, scope):
        """Set the active authorization to be an implicit authorization.

        :param access_token: The access_token obtained from Reddit's callback.
        :param expires_in: The number of seconds the ``access_token`` is valid
            for. The origin of this value was returned from Reddit's callback.
            You may need to subtract an offset before passing in this number to
            account for a delay between when Reddit prepared the response, and
            when you make this function call.
        :param scope: A space-delimited string of Reddit OAuth2 scope names as
            returned from Reddit's callback.

        Raise ``ClientException`` if ``Reddit`` was initialized for a
        non-installed application type.

        """
        authenticator = self._reddit._read_only_core._authorizer._authenticator
        if not isinstance(authenticator, UntrustedAuthenticator):
            raise ClientException('implicit can only be used with installed '
                                  'apps.')
        implicit_session = session(ImplicitAuthorizer(
            authenticator, access_token, expires_in, scope))
        self._reddit._core = self._reddit._authorized_core = implicit_session
