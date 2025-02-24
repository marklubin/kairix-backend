from flask import Blueprint, request, jsonify
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Kairix API!'})

