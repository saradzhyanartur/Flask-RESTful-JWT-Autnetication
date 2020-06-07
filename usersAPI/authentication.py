from flask_jwt_extended import JWTManager

jwt = JWTManager()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    print('[Black List check Ran!]')
    #return decrypted_token['jti'] in BLACKLIST