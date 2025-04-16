import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load environment variables from .env file
load_dotenv()

# AWS Rekognition Client Setup using environment variables
rekognition = boto3.client(
    'rekognition',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Name of your Rekognition collection
COLLECTION_ID = "hkis-faces"

# Register or index a face
def register_face(image_bytes, external_id):
    try:
        response = rekognition.index_faces(
            CollectionId=COLLECTION_ID,
            Image={'Bytes': image_bytes},
            ExternalImageId=external_id,
            DetectionAttributes=['DEFAULT']
        )
        return response['FaceRecords']
    except ClientError as e:
        print(f"Error registering face: {e}")
        return None

# Search for a matching face
def recognize_face(image_bytes, threshold=85):
    try:
        response = rekognition.search_faces_by_image(
            CollectionId=COLLECTION_ID,
            Image={'Bytes': image_bytes},
            FaceMatchThreshold=threshold,
            MaxFaces=1
        )
        return response.get('FaceMatches', [])
    except ClientError as e:
        print(f"Error recognizing face: {e}")
        return None

# Delete a face from collection by FaceId
def delete_face(face_id):
    try:
        response = rekognition.delete_faces(
            CollectionId=COLLECTION_ID,
            FaceIds=[face_id]
        )
        return response['DeletedFaces']
    except ClientError as e:
        print(f"Error deleting face: {e}")
        return None

# List all faces in the collection
def list_faces(limit=10):
    try:
        response = rekognition.list_faces(
            CollectionId=COLLECTION_ID,
            MaxResults=limit
        )
        return response['Faces']
    except ClientError as e:
        print(f"Error listing faces: {e}")
        return None
