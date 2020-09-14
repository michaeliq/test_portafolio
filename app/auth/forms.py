from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length, ValidationError
from .models import User

class UserForm(FlaskForm):     
    username = StringField('User Name', validators=[Length(max=25), DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])               
    email = StringField('E-mail',validators=[DataRequired(),Email()])                
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose an other one')

    def validate_email(self,email):
        user_e = User.query.filter_by(email=email.data).first()
        if user_e:
            raise ValidationError('That E-mail is taken. Please choose an other one')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[Length(max=25),DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Sign in')
