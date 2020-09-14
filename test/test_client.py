from . import BaseTestClass
from sqlalchemy.exc import IntegrityError
from app.auth.models import User
import requests
from flask import make_response, url_for

class ClientTestCase(BaseTestClass):

    def test_email_repited(self):
        with self.cn:
            self.assertRaises(IntegrityError,BaseTestClass.create_user,'admin','password','common@email.com')

    def test_is_instance_user(self):
        with self.cn:
            self.assertIsInstance(BaseTestClass.create_user('malcom','passwlrd','malcon@email.com'),User,'It\'s not an instance')


    
    def test_jwt_no_validate(self):
        resp = self.client.get('http://localhost:5000/protected/')
        data = resp.data
        self.assertEqual(401,resp.status_code)
        self.assertIn(b'Missing cookie',data)

    def test_user_login(self):
        resp = self.client.post('http://localhost:5000/login/',data = {'username':'admin','password':'password'})
        print(resp)
'''
    def test_blacklist_checked(self):
        pass


    def test_db_table_exist(self):
        pass

    def test_user_exist(self):
        pass

    def test_user_password_wrong(self):
        pass
'''
