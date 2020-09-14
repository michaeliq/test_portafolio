#admin folder's forms
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,SubmitField,HiddenField
from wtforms.validators import Length, Email,DataRequired

class NewTagForm(FlaskForm):
    target = StringField('Target', validators=[DataRequired(), Length(max=20)]) 
    knowlegd = IntegerField('Knowlegd', validators=[DataRequired()])           
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')

class UpdateTagForm(FlaskForm):
    id_hidden = HiddenField(validators=[DataRequired()])
    knowlegd = IntegerField('New Knowlegd',validators=[DataRequired()])
    description = StringField('New Description', validators=[DataRequired()])
    submit = SubmitField('Update Tag')
