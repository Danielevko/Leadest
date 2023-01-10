from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from leadest import db
from flask import render_template,url_for,flash, redirect,request,Blueprint
from leadest.branches.forms import RegistrateBranch
from flask_login import current_user, login_required
from leadest.models import User, Branch


branches = Blueprint('branches', __name__)

@branches.route('/branch_register/<int:manager_id>',methods=['GET','POST'])

def branch_register(manager_id):
    form=RegistrateBranch()
    if form.validate_on_submit():
        print("YAYYYY!!")
        branch = Branch(company_name=form.company_name.data,
            address=form.address.data,
            city=form.city.data,
            manager_id=manager_id)
        db.session.add(branch)
        db.session.commit()
        flash("Thanks for register to LEADEST! please Login to enjoy Leadest!")
        return redirect(url_for('users.login'))
        print("FAIL")
    else:
        print("not validate")


        return render_template('branch_register.html',manager_id=manager_id,form=form)

@branches.route('/branch_update/<int:branch_id>', methods=['GET', 'POST'])
@login_required
def branch_update(branch_id):
    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        branch_to_update=Branches.query.get_or_404(branch_id)
        branch_to_update.company_name = form.company_name.data
        branch_to_update.address = form.address.data
        branch_to_update.city = form.city.data
        db.session.commit()
        return redirect(url_for('users.account'))
    else:
        return render_template('branch_update.html')
