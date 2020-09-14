from flask import Flask, render_template
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import SMTPHandler

class AppFlask():


    app = Flask(__name__,instance_relative_config=True)
    jwt = JWTManager()
    db = SQLAlchemy()
    migrate = Migrate()

    def create_app(setting_module,app=app,jwt=jwt,db=db,migrate=migrate):

        app.config.from_object(setting_module)
        if app.config.get('TESTING',False):
            app.config.from_pyfile('config-testing.py',silent=True)
        else:
            app.config.from_pyfile('config.py',silent=True)

        jwt.init_app(app)
        migrate.init_app(app,db)
        db.init_app(app)

        from .auth.models import Blacklist
        @jwt.token_in_blacklist_loader
        def check_if_token_is_revoked(decrypted_token):
            jti = decrypted_token['jti']
            entry = Blacklist.query.get(jti)    
            if entry is None:
                return True
            return entry == True


        from .public.routes import public
        app.register_blueprint(public)

        from .admin.routes import admin
        app.register_blueprint(admin)

        from .auth.routes import auth
        app.register_blueprint(auth)

        logging_handler(app)

        register_error_handler(app)

        return app
    
    def get_instance_db(db=db):
        return db

    def get_instance_jwt(jwt=jwt):
        return jwt

def logging_handler(app):

    del app.logger.handlers[:]

    loggers = [app.logger,]

    handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_func())
    
    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL'] or app.config['APP_ENV'] == app.config['APP_ENV_TESTING'] or app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.ERROR)
        handlers.append(console_handler)

    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

        mail_handler = SMTPHandler((app.config['MAIL_SERVER'],app.config['MAIL_PORT']),
                app.config['ADMIN'],app.config['DONT_REPLY_FROM_EMAIL'],
                f"[ERROR]{app.config['APP_ENV']} aplicacion fallo",
                (app.config['MAIL_USERNAME'],
                app.config['MAIL_PASSWORD']),())

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_verbose_func())
        handlers.append(mail_handler)

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def verbose_func():
    return logging.Formatter('[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S') 

def mail_verbose_func():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d

            Message:            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )


def register_error_handler(app):

    @app.errorhandler(401)
    def unauthorized_error(e):
        return render_template("401.html"),401
    
    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template("500.html"),500

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template("404.html"),400
    

