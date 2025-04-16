import json
import requests
from jose import jwt
from functools import wraps
from flask import request, jsonify

REGION = "ap-southeast-2"
USER_POOL_ID = "ap-southeast-2_8di6Rh9O5"  # ← Replace with yours
COGNITO_ISSUER = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}"
JWK_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"

# Cache JWKs
_jwk_cache = None
def get_jwk_keys():
    global _jwk_cache
    if not _jwk_cache:
        response = requests.get(JWK_URL)
        _jwk_cache = response.json()["keys"]
    return _jwk_cache

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        # 1. Try get token from cookie
        if request.cookies.get("hkis_token"):
            token = request.cookies.get("hkis_token")

        # 2. Or from Authorization header
        if not token and "Authorization" in request.headers:
            bearer = request.headers.get("Authorization")
            if bearer and bearer.startswith("Bearer "):
                token = bearer.replace("Bearer ", "")

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            # Decode + verify
            jwks = get_jwk_keys()
            header = jwt.get_unverified_header(token)
            key = next((k for k in jwks if k["kid"] == header["kid"]), None)
            if not key:
                return jsonify({"message": "Public key not found"}), 401

            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience="6ke7cvg9lsk19fj2ji2q94v1o",  # Optional: set your App Client ID here
                issuer=COGNITO_ISSUER
            )

            request.user = payload  # Attach user payload to request context

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.JWTError as e:
            return jsonify({"message": "Invalid token!", "error": str(e)}), 401

        return f(*args, **kwargs)

    return decorated
