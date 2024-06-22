# auth_layer/auth.py

from flask import Flask, redirect, url_for, session, request
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import os
import sys
import pathlib
from consts import GET_USER_URL, ADD_USER_URL

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from consts import *

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)


# Path to the client_secret.json
CLIENT_SECRETS_FILE = os.path.join(pathlib.Path(__file__).parent, 'client_secret.json')

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)


@app.route('/auth/login')
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)


@app.route('/auth/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args['state']:
        return redirect(url_for('login'))

    credentials = flow.credentials
    request_session = Request()

    try:
        id_info = id_token.verify_oauth2_token(
            id_info=credentials.id_token,
            request=request_session,
            audience=GOOGLE_CLIENT_ID
        )
    except ValueError:
        return 'Invalid token'

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
    print(url)
    user = requests.get(url)
    if not user:
        requests.post(ADD_USER_URL, json = {
            'email': email,
            'name': first_name,
            'lastname': last_name
        })
    return redirect(url_for('profile'))

@app.route('/auth/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/profile')
def profile():
    if 'google_id' not in session:
        return redirect(url_for('login'))
    return f'Hello, {session["email"]}!'

if __name__ == '__main__':
    app.run(debug=True, port=5005)
