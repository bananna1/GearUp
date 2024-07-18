from flask import Blueprint, request, jsonify
import requests

display_results_blueprint = Blueprint('display_results', __name__)

@display_results_blueprint.route('/', methods=["POST"])
def display_results():
    return