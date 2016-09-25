import logging

from flask import (
    Blueprint,
    request,
    Response,
    session,
)

from meiling import rule_db
from meiling.rule_engine.models import RequestContext

# Header names that Nginx sends with each `auth_request` request
NGINX_HOST = "X-Nginx-Host"
NGINX_REQUEST_METHOD = "X-Nginx-Request-Method"
NGINX_REQUEST_URI = "X-Nginx-Request-Uri"

# The header we provide back to nginx
MEILING_USER = "X-Meiling-User"

log = logging.getLogger(__name__)
nginx_bp = Blueprint('nginx_bp', __name__)


def create_200_response(meiling_user: str):
    return Response("", 200, {MEILING_USER: meiling_user})


def create_401_response():
    return Response("", 401, {'WWW-Authenticate': 'Custom'})


def create_403_response():
    return Response("", 403)


@nginx_bp.route('/auth_request')
def auth_request():
    if 'google_user' not in session:
        return create_401_response()

    user = session['google_user']

    if not user.get('verified_email') or not user.get('email'):
        log.info(
            "Google user info present in session, but email not verified (%s) or email not present (%s)",
            user.get('verified_email'),
            user.get('email'),
        )
        return create_403_response()

    # We require all of the Nginx headers to be present, even if they aren't all used
    required_headers = [
        NGINX_HOST,
        NGINX_REQUEST_METHOD,
        NGINX_REQUEST_URI,
    ]
    for header in required_headers:
        if header not in request.headers:
            log.warn("Nginx did not send the following header: %s", header)
            return create_401_response()

    context = RequestContext(
        user_email=user['email'],
        host=request.headers[NGINX_HOST],
        request_method=request.headers[NGINX_REQUEST_METHOD],
        request_uri=request.headers[NGINX_REQUEST_URI],
    )

    if rule_db.has_access(context):
        return create_200_response(user['email'])

    log.warn("Request deemed unauthorized: %s", context)
    return create_403_response()
