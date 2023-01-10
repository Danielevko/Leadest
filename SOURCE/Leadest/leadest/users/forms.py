# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
from flask_login import current_user
from leadest.models import User, Branch

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    role= SelectField('Role', choices=[('sales', 'Sales Manager'), ('branch', 'Branch Manager')])
    email=StringField('Email', validators=[DataRequired(),Email()])
    username=StringField('Username', validators=[DataRequired()])
    name=StringField('Name', validators=[DataRequired()])
    id_m=StringField('ID', validators=[DataRequired()])
    phone=StringField('Phone', validators=[DataRequired()])
    gender= SelectField('Gender', choices=[('female', 'Female'), ('male', 'Male')])
    birth_date=StringField('Birthdate', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired(),EqualTo('pass_confirm', message='Password must match!')])
    pass_confirm=PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has been registered already')


class UpdateUserForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(),Email()])
    name=StringField('Name', validators=[DataRequired()])
    phone=StringField('Phone', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired(),EqualTo('pass_confirm', message='Password must match!')])
    pass_confirm=PasswordField('Confirm Password', validators=[DataRequired()])
    address=StringField('Branch Address', validators=[DataRequired()])
    city=StringField('Branchs city', validators=[DataRequired()])
    company_name=StringField('Company Name', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, field):
        # Check if not None for that user email!
        if current_user.email!=field:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Your email has been registered already!')
