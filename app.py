# app.py
from flask import Flask, g, request, send_from_directory, abort, jsonify
from flask_cors import CORS
from flask_restful import Resource, reqparse
from functools import wraps
from dotenv import load_dotenv
import os
import json
import jwt
from jwt  import InvalidTokenError

app = Flask(__name__)
CORS(app)

load_dotenv()

KEYCLOAK_PUBLIC_KEY = os.getenv('KEYCLOAK_PUBLIC_KEY')

def require_token(f):
    """
    Decorator that validates JWT tokens from Keycloak.
    Checks Authorization header, verifies token signature and stores decoded token in g.user.
    Returns 401 if token is missing, malformed or invalid.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return {'message': 'Token malformado'}, 401
        
        if not token:
            return {'message': 'Token no proporcionado'}, 401

        try:
            # Verificar el token usando la clave pública de Keycloak
            decoded = jwt.decode(
                token,
                KEYCLOAK_PUBLIC_KEY,
                algorithms=['RS256'],
                audience='account'
            )
            g.user = decoded
        except InvalidTokenError as e:
            return {'message': 'Token inválido'}, 401

        return f(*args, **kwargs)
    return decorated

def get_db():
    """
    Executes a Neo4j query to get first 5 person names.
    Returns JSON string of results.
    """
    results = conn.query("MATCH (p:Person) RETURN p.name LIMIT 5")
    return json.dumps(results)

@app.route('/public', methods=['GET'])
def home():
    """Public endpoint that returns a welcome message."""
    return "Hello, World!"

@app.route('/private', methods=['GET'])
@require_token
def info():
    """Protected endpoint that requires valid JWT token."""
    return "Private"

@app.route('/data', methods=['POST'])
@require_token
def data():
    """
    Protected endpoint that accepts JSON data.
    Validates required fields (name, email).
    Returns 415 if not JSON, 400 if missing fields, 200 if successful.
    """
    # Check if the request has JSON content
    if not request.is_json:
        return {"error": "Content type must be application/json"}, 415
    
    # Get the JSON data
    data = request.get_json()
    
    # Validate required fields (example)
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing required field: {field}"}, 400
    
    # Process the data (example)
    return jsonify({
        "message": "Data received successfully",
        "data": data
    }), 200

if __name__ == '__main__':
    app.run(debug=True)