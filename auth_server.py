from flask import Flask, request
from oauthlib.oauth2 import MobileApplicationServer
import auth_models
import oauth_request_validator
import logging
import os
import sqlalchemy


LOG = logging.getLogger('auth_server')


DB_URI = os.environ['AUTH_DB_URI']
PORT = int(os.environ['AUTH_PORT'])
SECRET_KEY = os.environ['AUTH_SECRET_KEY']
VALID_API_KEY = os.environ['AUTH_VALID_API_KEY']


# -- Models
engine = sqlalchemy.create_engine(DB_URI)
auth_models.Base.metadata.create_all(engine)
Session = sqlalchemy.orm.sessionmaker(bind=engine)


# -- OAuth setup
validator = oauth_request_validator.ImplicitRequestValidator(Session())
oauth_endpoint = MobileApplicationServer(validator)


# -- Views
app = Flask('Auth Server')


@app.route('/authorize', methods=['GET'])
def authorize():
    oauth_endpoint.validate_authorization_request(uri=request.url,
            body=request.data, headers=request.headers)
    headers, body, status_code = oauth_endpoint.create_authorization_response(
            uri=request.url,
            body=request.data, headers=request.headers,
            scopes=request.args.get('scope').split(' '),
            credentials=None
            )

    LOG.debug('authorization succeded with headers: %s',
            headers)

    return '', status_code, headers


@app.route('/validate', methods=['POST'])
def validate():
    pass


def main():
    app.debug = True
    app.secret_key = SECRET_KEY
    logging.basicConfig(level=logging.DEBUG)
    app.run('0.0.0.0', port=PORT)


if __name__ == '__main__':
    main()
