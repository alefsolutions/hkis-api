# routes/households.py
from flask import Blueprint, jsonify, request
from utils.db import get_db_connection
from utils.auth import token_required
from mysql.connector import Error

household_bp = Blueprint('households', __name__, url_prefix='/api/households')

@household_bp.route('/geo', methods=['GET'])
@token_required
def all_household_geodata():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
              h.house_code,
              h.longitude,
              h.latitude,
              sc.support_color AS support_color
            FROM 
              households h
            LEFT JOIN 
              support_colors sc ON h.support_color_id = sc.support_color_id;
        ''')
        rows = cursor.fetchall()
        return jsonify(rows)
    except Error as e:
        print("DB error:", e)
        return jsonify({'message': 'Internal Server Error'}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()