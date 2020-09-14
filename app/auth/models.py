#auth folder' models
from sqlalchemy.exc import IntegrityError
from app import AppFlask

db = AppFlask.get_instance_db()

class User(db.Model):              
    __tablename__='Users'

    id = db.Column(db.Integer,primary_key=True)   
    username = db.Column(db.String(30),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(50),nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f'User: {self.username}'

    def __str__(self):
        return self.username

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_user_pass(self,password):
        self.password = password
        db.session.commit()

    def change_role(self):
        self.is_admin = True
        db.session.commit()
    
    @staticmethod
    def get_role(usern):
        role = User.query.filter_by(username=usern).first()
        role = role.is_admin
        return role

    @staticmethod
    def get_users():
        users = []
        query = User.query.all()
        for user in query:
            data = {'username':user.username, 'email':user.email,'password':user.password,'privilegies':user.is_admin}
            users.append(data)
        return users


class Blacklist(db.Model):
    __tablename__= 'blacklist'

    jti = db.Column(db.String(50), primary_key=True)
    type_token = db.Column(db.String(10),nullable=False)
    is_revoked = db.Column(db.Boolean,nullable=False)
    it_was_add = db.Column(db.DateTime,nullable=False)

    def __init__(self, type_token,jti,is_revoked, it_was_add):
        self.jti = jti
        self.type_token = type_token
        self.is_revoked = is_revoked
        self.it_was_add = it_was_add

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_state(self):
        self.is_revoked = True
        db.session.commit()

