from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired, Email

class ContactForm(FlaskForm):       
    name = StringField('Full-Name',validators=[Length(max=35),DataRequired()])     
    telephone = StringField('Telephone Number',validators=[DataRequired()])        
    email = StringField('E-mail',validators=[Email(),DataRequired()])          
    submit = SubmitField('Contact Me')

class MessageForm(FlaskForm):
    message = StringField('',validators=[DataRequired()])
    submit = SubmitField('>')
