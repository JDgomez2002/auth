# app.py
from flask import Flask, g, request, send_from_directory, abort
from flask_cors import CORS
from flask_restful import Resource, reqparse
from functools import wraps
import os
import json
import jwt
from jwt.exceptions import InvalidTokenError

app = Flask(__name__)
CORS(app)

# Configuración de Keycloak
KEYCLOAK_PUBLIC_KEY = os.getenv('KEYCLOAK_PUBLIC_KEY', '')  # Asegúrate de tener la clave pública de Keycloak
KEYCLOAK_URL = os.getenv('KEYCLOAK_URL', '')
KEYCLOAK_REALM = os.getenv('KEYCLOAK_REALM', '')

def require_token(f):
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
    results = conn.query("MATCH (p:Person) RETURN p.name LIMIT 5")
    return json.dumps(results)

@app.route('/public', methods=['GET'])
def home():
    return "Hello, World!"

@app.route('/private', methods=['GET'])
@require_token
def info():
    names = get_db()
    return names

@app.route('/data', methods=['POST'])
@require_token
def data():
    names = get_db()
    return names

if __name__ == '__main__':
    app.run(debug=True)