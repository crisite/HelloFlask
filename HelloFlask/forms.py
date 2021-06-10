from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , BooleanField ,SubmitField , SelectField ,SelectMultipleField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_wtf.file import file_required, file_allowed

app = Flask(__name__)
app.secret = 'my hard secret'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[file_required(), file_allowed(['jpg','png','Images only!'])])
    submit = SubmitField('Upload')