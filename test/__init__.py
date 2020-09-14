import unittest
from app.auth.models import User

from app import AppFlask


class BaseTestClass(unittest.TestCase):
    db = AppFlask.db

    def setUp(self,db = db):
        self.app = AppFlask.create_app(setting_module="config.testing")
        self.client = self.app.test_client()

        # Crea un contexto de aplicación
        self.cn = self.app.app_context()
        with self.cn:
            # Crea las tablas de la base de datos
            db.create_all()
            self.user1 = BaseTestClass.create_user('admin','password','common@email.com')
            self.user1.change_role()

    def tearDown(self,db = db):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()

    @staticmethod
    def create_user(username,password,email):            
        user = User(username,password,email)
        #user.change_role()
        user.save()
        return user

