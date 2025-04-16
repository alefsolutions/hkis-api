# routes/candidates.py
from flask import Blueprint, jsonify
from utils.db import get_db_connection
from utils.auth import token_required
from mysql.connector import Error

candidate_bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')

@candidate_bp.route('', methods=['GET'])
@token_required
def candidate_support_totals():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
              cs.candidate_support AS candidate_name,
              COUNT(h.id) AS total_supporters
            FROM 
              households h
            JOIN 
              candidate_supports cs 
              ON h.candidate_support_id = cs.candidate_support_id
            GROUP BY 
              cs.candidate_support
            ORDER BY 
              total_supporters DESC;
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