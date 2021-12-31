import json
import os
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIENCE = os.getenv('API_AUDIENCE')


class AuthError(Exception):
    def __init__(self, error, status_code):
        '''
        Common error method
        '''
        self.error = error
        self.status_code = status_code


def logout():
    urlopen(f'https://{AUTH0_DOMAIN}/logout')
    return "logged out"

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    authorisationHeader = request.headers.get('Authorization', None)
    if authorisationHeader is None:
        raise AuthError({
            'code': 'no authorization header',
            'description': 'Authorization header is expected'
        }, 401)
    splitHeaders = authorisationHeader.split()
    if splitHeaders[0].lower() != 'bearer':
        raise AuthError({
            'code': 'Invalid authorization header',
            'description': 'Authorization Header should start with bearer'
        }, 401)
    elif len(splitHeaders) == 1:
        raise AuthError({
            'code': 'Invalid authorization header',
            'description': 'Authorization Header is not having the token'
        }, 401)
    elif len(splitHeaders) > 2:
        raise AuthError({
            'code': 'Invalid authorization header',
            'description': 'Authorization Header should be a bearer token'
        }, 401)
    auth_token = splitHeaders[1]
    return auth_token


def check_permissions(permission, payload):
    '''Checks for the permission in the payload.
    If permissions are not passed in the jwt payload exception is raised.
    If the user invoking the api does not have the relevant access
    an exception is raised.
    '''
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'unauthorized api call',
            'description': 'Insufficient permission'
        }, 401)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized api call',
            'description': 'Persmission is not in payload'
        }, 401)


def verify_decode_jwt(token):
    '''Method to decode the JWT token
    '''
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. check the audience & issuer'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(permission=''):
    '''A decorator used to check the authorization of user to access an api
    '''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
