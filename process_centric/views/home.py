from flask import redirect, url_for, session, request, flash, Blueprint, render_template
import logging





home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def home():
    if 'google_id' not in session:
        logging.debug("No user in session, redirecting to login.")
        login_url = url_for('auth.login')
        return redirect(login_url)
    name = session['first_name']
    lastname = session['last_name']
    return render_template('index.html', name=name, lastname=lastname)