from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from leadest.models import User
from leadest.models import Branch

class RegistrateBranch(FlaskForm):
    company_name=StringField('Companys name', validators=[DataRequired()])
    address=StringField('Address', validators=[DataRequired()])
    city=StringField('City', validators=[DataRequired()])

    submit = SubmitField('Submit!')
