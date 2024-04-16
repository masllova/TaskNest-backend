import jwt

class JWTManager:
    SECRET_KEY = "your_secret_key_here"

    @classmethod
    def generate_token(cls, user_id):
        payload = {'user_id': user_id}
        token = jwt.encode(payload, cls.SECRET_KEY, algorithm='HS256')
        return token

    @classmethod
    def decode_token(cls, token):
        try:
            decoded_token = jwt.decode(token, cls.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token['user_id']
            return user_id
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
