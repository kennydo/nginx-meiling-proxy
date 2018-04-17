import logging

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_oauthlib.client import (
    OAuth,
    OAuthException,
)

from meiling.utils import URL


log = logging.getLogger(__name__)
oauth_bp = Blueprint('oauth_bp', __name__)


@oauth_bp.record
def initialize_google_oauth(setup_state):
    oauth = OAuth()
    oauth_bp.google = oauth.remote_app(
        'google',
        app_key='GOOGLE',
        request_token_params={
            'scope': 'email',
            'prompt': 'select_account',
        },
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        consumer_key=setup_state.app.config['GOOGLE_OAUTH_CONSUMER_KEY'],
        consumer_secret=setup_state.app.config['GOOGLE_OAUTH_CONSUMER_SECRET'],
    )

    @oauth_bp.google.tokengetter
    def get_google_oauth_token():
        return session.get('google_token')


@oauth_bp.route('/')
def index():
    if 'google_user' in session:
        user = session['google_user']

        is_logged_in = True
        user_name = user['name']
        user_email = user['email']
    else:
        is_logged_in = False
        user_name = None
        user_email = None

    next_url_string = request.args.get('next_url')
    next_url = URL.from_string(next_url_string) if next_url_string else None

    return render_template(
        'oauth/index.html',
        is_logged_in=is_logged_in,
        user_name=user_name,
        user_email=user_email,
        next_url=next_url,
    )


@oauth_bp.route('/login')
def login():
    next_url = URL.from_string(request.args.get('next_url'))
    if next_url:
        # Since passing along the "next" URL as a GET param requires
        # a different callback for each page, and Google requires us to
        # whitelist each allowed callback page, we can't pass it as a GET
        # param. Instead, we sanitize and put into the session.
        session['next_url'] = next_url.to_string()
    return oauth_bp.google.authorize(
        callback=url_for('.authorized', _external=True))


@oauth_bp.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('google_user', None)

    flash("You have successfully logged out.")

    return redirect(url_for('.index'))


@oauth_bp.route('/login/authorized')
def authorized():
    try:
        resp = oauth_bp.google.authorized_response()
    except OAuthException as e:
        error_message = "Encountered an error in response from Google: {0}".format(e.data)

        log.exception(error_message)
        flash(error_message)

        return redirect(url_for('.index'))

    next_url_string = session.pop('next_url', url_for('.index'))

    if resp is None:
        flash("You didn't sign in.")
        return redirect(next_url_string)

    session.permanent = True
    session['google_token'] = (resp['access_token'], '')
    session['google_user'] = oauth_bp.google.get('userinfo').data

    flash("You have successfully authenticated.")
    return redirect(next_url_string)
