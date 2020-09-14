from functools import wraps
from flask_jwt_extended import get_jwt_claims
from flask import current_app, abort

def admin_required(f):
    @wraps(f)
    def decorator_func(*args,**kargs):
        claim  = get_jwt_claims()
        print(claim)
        if claim['is_admin'] and claim['is_admin'] is not None:
            return f(*args,**kargs)
        else:
            current_app.logger.info('is not admin or permission is not defined')
            abort(401)

    return decorator_func
