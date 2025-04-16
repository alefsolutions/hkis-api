from flask import Blueprint, request, jsonify
from utils.facial import register_face, recognize_face, delete_face, list_faces
from utils.auth import token_required

facial_bp = Blueprint('facial', __name__, url_prefix='/api/faces')

# POST /api/faces/register
@facial_bp.route('/register', methods=['POST'])
# @token_required
def register():
    if 'image' not in request.files or 'external_id' not in request.form:
        return jsonify({'error': 'Image file and external_id are required'}), 400

    image_file = request.files['image']
    external_id = request.form['external_id']
    image_bytes = image_file.read()

    result = register_face(image_bytes, external_id)
    if result is None or len(result) == 0:
        return jsonify({'error': 'Failed to register face'}), 500

    return jsonify({
        'message': 'Face registered successfully',
        'face_records': result
    }), 200

# POST /api/faces/recognize
@facial_bp.route('/recognize', methods=['POST'])
# @token_required
def recognize():
    if 'image' not in request.files:
        return jsonify({'error': 'Image file is required'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()

    matches = recognize_face(image_bytes)
    if matches is None:
        return jsonify({'error': 'Recognition failed'}), 500

    if len(matches) == 0:
        return jsonify({'message': 'No match found'}), 200

    matched_face = matches[0]
    return jsonify({
        'message': 'Match found',
        'external_id': matched_face['Face']['ExternalImageId'],
        'confidence': matched_face['Similarity'],
        'face_id': matched_face['Face']['FaceId']
    }), 200

# DELETE /api/faces/<face_id>
@facial_bp.route('/<face_id>', methods=['DELETE'])
# @token_required
def delete(face_id):
    result = delete_face(face_id)
    if result is None or len(result) == 0:
        return jsonify({'error': 'Face ID not found or failed to delete'}), 404

    return jsonify({
        'message': 'Face deleted successfully',
        'deleted_faces': result
    }), 200

# GET /api/faces
@facial_bp.route('', methods=['GET'])
# @token_required
def list_all_faces():
    limit = int(request.args.get('limit', 10))
    faces = list_faces(limit=limit)

    if faces is None:
        return jsonify({'error': 'Failed to list faces'}), 500

    return jsonify({
        'faces': faces
    }), 200
