from datetime import datetime, timedelta
from oauthlib.oauth2 import RequestValidator
from werkzeug.security import gen_salt
import auth_models


class ImplicitRequestValidator(RequestValidator):
    def __init__(self, session):
        self.session = session

    # Pre- and post-authorization.

    def validate_client_id(self, client_id, request, *args, **kwargs):
        # XXX Needed
        # Simple validity check, does client exist? Not banned?
        return True

    def validate_redirect_uri(self, client_id, redirect_uri, request, *args, **kwargs):
        # XXX Needed
        # Is the client allowed to use the supplied redirect_uri? i.e. has
        # the client previously registered this EXACT redirect uri.
        return True

    def get_default_redirect_uri(self, client_id, request, *args, **kwargs):
        # XXX Needed
        # The redirect used if none has been supplied.
        # Prefer your clients to pre register a redirect uri rather than
        # supplying one on each authorization request.
        return 'http://localhost:2700/lol'

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        # XXX Needed
        # Is the client allowed to access the requested scopes?
        return True

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        # XXX Needed
        # Scopes a client will authorize for if none are supplied in the
        # authorization request.
        return "foo bar"

    def validate_response_type(self, client_id, response_type, client, request, *args, **kwargs):
        # XXX Needed
        # Clients should only be allowed to use one type of response type, the
        # one associated with their one allowed grant type.
        # In this case it must be "code".
        return response_type == 'token'

    # Token request

    def save_bearer_token(self, token, request, *args, **kwargs):
        # XXX Needed
        # Remember to associate it with request.scopes, request.user and
        # request.client. The two former will be set when you validate
        # the authorization code. Don't forget to save both the
        # access_token and the refresh_token and set expiration for the
        # access_token to now + expires_in seconds.
        params = dict(request.uri_query_params)
        stored_token = auth_models.Token(
            access_token=gen_salt(32),
            refresh_token=gen_salt(32),
            expires=datetime.now() + timedelta(
                seconds=token.get('expires_in', 3600)),
            scope=[params.get('scope', 'bobodefaultscope')],
        )
        self.session.add(stored_token)
        self.session.commit()
        # XXX return a redirect uri..maybe we don't want this for implicit?

    # Protected resource request

    def validate_bearer_token(self, token, scopes, request):
        # XXX Needed
        # Remember to check expiration and scope membership
        True
