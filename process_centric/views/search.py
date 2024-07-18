from flask import Blueprint, request, jsonify
import requests

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/', methods=["POST"])
def search():
    return