from flask import Flask, redirect, url_for, session, request, flash
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import os
import sys
import pathlib
import logging
from consts import *

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize Flask app
app = Flask(__name__)
app.secret_key = b'8\xa1\x84\xe9\xf7\x93(o\xac9G\xe1\xe0h\xc8\x86\x14\xc0\xe9\xfeG\xbf\xca\xe0'

# Path to the client_secret.json
CLIENT_SECRETS_FILE = os.path.join(pathlib.Path(__file__).parent, 'client_secret.json')

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

@app.route('/auth/login')
def login():
    logging.debug("Starting login process.")
    logging.debug(f"REDIRECT_URI: {REDIRECT_URI}")
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    logging.debug(f"Authorization URL: {authorization_url}")
    logging.debug(f"Session state set: {session['state']}")
    return redirect(authorization_url)

@app.route('/auth/callback')
def callback():
    logging.debug("Callback route called.")

    # Ensure session state exists before use
    if 'state' not in session:
        logging.error("Session state not found. Possible session timeout or CSRF attack.")
        flash("Session expired or invalid. Please try logging in again.")
        return redirect(url_for('login'))

    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args.get('state'):
        logging.error("State mismatch. Possible CSRF attack.")
        flash("Session expired or invalid. Please try logging in again.")
        return redirect(url_for('login'))

    credentials = flow.credentials
    request_session = Request()

    try:
        id_info = id_token.verify_oauth2_token(
            id_token=credentials.id_token,
            request=request_session,
            audience=GOOGLE_CLIENT_ID
        )
    except ValueError:
        logging.error("Invalid token.")
        flash("Invalid token received. Please try logging in again.")
        return redirect(url_for('login'))

    google_id = id_info.get('sub')
    email = id_info.get('email')
    first_name = id_info.get('given_name')
    last_name = id_info.get('family_name')

    session['google_id'] = google_id
    session['email'] = email
    session['first_name'] = first_name
    session['last_name'] = last_name

    # Add user to the database if not already present
    url = f'{GET_USER_URL}/{email}'
    logging.debug(f"Fetching user with URL: {url}")
    user = requests.get(url)

    if user.status_code == 404:
        logging.debug("User not found, adding user.")
        requests.post(ADD_USER_URL, json={
            'email': email,
            'name': first_name,
            'lastname': last_name
        })
    return redirect(url_for('profile'))

@app.route('/auth/logout')
def logout():
    logging.debug("Logging out.")
    session.clear()
    return redirect('/')

@app.route('/profile')
def profile():
    if 'google_id' not in session:
        logging.debug("No user in session, redirecting to login.")
        return redirect(url_for('login'))
    return f'Hello, {session["email"]}!'

if __name__ == '__main__':
    logging.debug("Starting Flask app.")
    app.run(debug=True, port=5005)
