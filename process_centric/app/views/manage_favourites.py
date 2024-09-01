from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
import requests
from process_centric.app.consts import ADD_FAVOURITE_GEAR_URL, REMOVE_FAVOURITE_GEAR_URL
import logging


manage_favourite_blueprint = Blueprint('manage_favourite', __name__)

@manage_favourite_blueprint.route('/', methods = ['POST'])
def manage_favourite():
    if 'google_id' not in session:
        logging.debug("No user in session, redirecting to login.")
        login_url = url_for('auth.login')
        return redirect(login_url)
    
    gear_id = request.form.get('item_id')
    #print("GEAR ID: ", gear_id)
    action = request.form.get('action')
    #print(action)
    email = session['email']
    if action == 'add':
        response = requests.post(ADD_FAVOURITE_GEAR_URL, json={
            'gearid': gear_id, 
            'email': email
        })
        response_json = response.json()
        if response.ok:
            flash('Gear added to favourites successfully!', 'success')
        elif response_json.get('message') == 'Item already present in favourites':
            flash('Item already present in favourites', 'success')
        else:
            flash('Failed to add gear to favourites.', 'error')

    elif action == 'remove':

        response = requests.post(REMOVE_FAVOURITE_GEAR_URL, json={
            'gearid': gear_id, 
            'email': email
        })

        if response.ok:
            flash('Gear removed from favourites successfully!', 'success')
        else:
            flash('Failed to remove gear from favourites.', 'error')

    return redirect(request.referrer)