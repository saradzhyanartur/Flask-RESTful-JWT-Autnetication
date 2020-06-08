from flask_jwt_extended import JWTManager
from usersAPI import revoked_store

jwt = JWTManager()
#print('[AUTHENTICATION] revoked store id: ', id(revoked_store))

@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    '''Tokens that have not been registered with Redis are considered to
    be the same as those that have been revoked'''
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is None:
        return True
    return entry == 'true'
