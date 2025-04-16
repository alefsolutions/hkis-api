from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from mysql.connector import Error
import bcrypt
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user or not bcrypt.checkpw(password.encode(), user['password'].encode()):
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

        # Generate JWT
        payload = {
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(
                minutes=int(os.getenv('JWT_EXPIRY_MINUTES', 60))
            )
        }

        token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')

        print(token)

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token
        })

    except Error as e:
        print("DB error:", e)
        return jsonify({'message': 'Internal Server Error'}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
