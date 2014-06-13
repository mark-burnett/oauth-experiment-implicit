from flask import Flask, redirect, request
from oauthlib.oauth2 import MobileApplicationServer
import oauth_request_validator
import logging
import os
import urllib


LOG = logging.getLogger('resource_server')


AUTH_URI = os.environ['RESOURCE_AUTH_URI']
PORT = int(os.environ['RESOURCE_PORT'])
SECRET_KEY = os.environ['RESOURCE_SECRET_KEY']
CLIENT_ID = os.environ['RESOURCE_CLIENT_ID']


# -- OAuth setup
validator = oauth_request_validator.ImplicitRequestValidator(None)
oauth_endpoint = MobileApplicationServer(validator)


# -- Views
app = Flask('Resource Server')


IAN_REQUIRED_SCOPES = ['ian']
@app.route('/ians_resource', methods=['GET'])
def ians_resource():
    if have_access_token():
        oauth_endpoint.verify_request(uri=request.url, body=request.data,
                headers=request.headers, scopes=IAN_REQUIRED_SCOPES)

        return 'good job!'

    else:
        return redirect_to_auth(IAN_REQUIRED_SCOPES)


def have_access_token():
    return request.headers.get('Authorization')


def redirect_to_auth(scopes):
    return redirect(construct_redirect_url(scopes))


def construct_redirect_url(scopes):
    params = {
        'redirect_uri': request.url,
        'client_id': CLIENT_ID,
        'response_type': 'token',
        'scope': ' '.join(scopes),
    }
    return '%s?%s' % (AUTH_URI, urllib.urlencode(params))


def main():
    app.debug = True
    app.secret_key = SECRET_KEY
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=PORT)


if __name__ == '__main__':
    main()
