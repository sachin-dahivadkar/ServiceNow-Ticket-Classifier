from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import InputRequired,Email


class Loginform(FlaskForm):
    username=StringField('Username', validators=[InputRequired()])
    password=PasswordField('Password', validators=[InputRequired()])
    #submit=SubmitField('Login')
    

