# routes/villages.py
from flask import Blueprint, jsonify
from utils.db import get_db_connection
from utils.auth import token_required
from mysql.connector import Error

village_bp = Blueprint('villages', __name__, url_prefix='/api/villages')

@village_bp.route('', methods=['GET'])
@token_required
def village_dataset_totals():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
              v.village_name,
              COUNT(h.id) AS total_households
            FROM 
              households h
            JOIN 
              living_ats la ON h.living_at_id = la.living_at_id
            JOIN 
              villages v ON la.village_id = v.id
            GROUP BY 
              v.village_name
            ORDER BY 
              total_households DESC;
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