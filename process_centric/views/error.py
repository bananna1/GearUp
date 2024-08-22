from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
import requests

error_blueprint = Blueprint('error', __name__)

@error_blueprint.route('/', methods = ['GET'])
def error():
    
    message = request.args.get('error_message')
    previous_url = request.args.get('previous_url')

    print(message)

    return render_template('error.html', error_message=message, previous_url=previous_url)
