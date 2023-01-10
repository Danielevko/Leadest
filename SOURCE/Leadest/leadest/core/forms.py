from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed


class Upload_for_dashboard(FlaskForm):
    file = FileField('Upload your csv leads file', validators=[FileAllowed(['CSV'])])
    submit = SubmitField('Submit')
