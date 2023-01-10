from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from leadest import db
from werkzeug.security import generate_password_hash,check_password_hash
from leadest.models import User, LeadsFile,Branch
from leadest.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from google.cloud import storage
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import gcsfs



def send_email1(send_to, subject):
    send_from = "leadest.leadme@gmail.com"
    password = "yrsljwfliamfnlqj"

    message = """\
    <p>Thanks for using Leadme! <br>
    your Clustered CSV is attached to this email.&nbsp;</p>
    <p><br></p>
    <p><strong>Greetings&nbsp;</strong><br><strong>Leadest&nbsp;    </strong></p>
    """
    for receiver in send_to:
        multipart = MIMEMultipart()
        multipart["From"] = send_from
        multipart["To"] = receiver
        multipart["Subject"] = subject
        ##attachment = MIMEApplication(df.to_csv())
        ##attachment["Content-Disposition"] = 'attachment; filename=" {}"'.format(f"{subject}.csv")
        ##multipart.attach(attachment)
        HOST = "smtp.gmail.com"
        PORT = "587"
        SERVER = smtplib.SMTP()
        SERVER.connect(HOST, PORT)

        server.starttls()
        server.login(send_from, password)
        server.sendmail(send_from, send_to, multipart.as_string())
        server.quit()

users = Blueprint('users', __name__)
CREDENTIALS={
"type": "service_account",
    "project_id": "phonic-monolith-345108",
    "private_key_id": "1b247c6ef857ff56c071ccc5f0e6487e285b9eb8",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCfhnvmi+vJe2At\nqt74kSYMJiwslgENhEr07tCPjJr6orWa5B+yNVYy4DeYUM6th8JlFHvId1KoVl4F\nPlIIpFEfKI4F2uFpSQ+UEKfPVtw2ZkORY6Va3FNn8HMpbhggHQuxBQfgcmLx8su7\nYuMQTyZKZrWgXzqRo37TitUKVFfTj5rZ/g72OcSHQhRHbrMTz5LcDslrf83LXkfT\nYi7pXmYEdYkeDoS/+fVtS0S1M7AWBlc94hGa9CN8So+m1ZxcADV5ChUzgv2e0LX8\nkeYctio3rgsWJI3r4j/dIIC/oNl+AbEPuUshM1RHvbOUiGtaIXI7D1zpQ3RHPckD\nTZTjgAuPAgMBAAECggEAKDHZjDibO5Qjor4YGmdwP8Vqgf113HMF8/ssf878ycQv\noAx01BFOW9lVCMLroJvBZniny9YM9K92Vznhr52/dutgBael/kJTc4pSzhJjwC06\nPyrtYhx7w4e5bKn52DWZWYwb9Pi9Z5s2rEt5TQW0bzC7+OGlv0aD0Ud88HJaAssY\n0+MuPvCDIf3kCjb8zkrJed9IhhcrtLsJPRXJf8cQ+lMu3RlaQxtl8HpOJncKinZd\nwZXhKM5TzcOfM1iaW212ikV+GHUkQxgpXmYnsI/yvVkwmwflSDKP1NXAadc2C+tY\nWllBaNq2CW6s+BQt+2JjhNQgPSbQvOaYiqwpth52yQKBgQDhlse6vP5cpyh7ecVN\n9ixDvJNaJIpV1X4mep5fwdd68k+GpQEt+t7KvyKGElXFb7h927iwoUBZA/gyCdEc\nwaIs0iQT3/yONn3lMmr4NU5EZebco7RE7z6VeBSVOrQnbZyVlRjHXaoZ2qwZ35NW\ntMnf00T++ly7QkFw1UMUHbAGowKBgQC1B84J5o8DEUZiZuRuCod0Mh7UWbzW6t9X\nEAJav+WJVZVxHOowLQ7/BqVo2LSh1wv5SgtyU/vevxYHXvpVR42swTDg8QATWPAh\n2IfaMEZ3/fZncqnTwJFfJx5pQR7dZInwJy5G/Ze5pBPfhTi0Ga+VZOWeuy7AR3z3\nKIbMs6PyJQKBgAy1XdMbSokVsaYjGgZmU+ANA5AUduaW/GBWkA188hKvC+Pd788T\nTvHFCsDaz5Ir1QziD+mDbAiXvKe0/d7M2cIEpJuqBqRMVZNP387T0fDwfKz5W/J2\nN+Rbu20cvYFrH2Md3yN8F1UViJR8j+RWkvjVAhILMKYr+VvN59V+RqhZAoGAezVA\nqcRdeTz8pmRY+/v2jMK/8M7Sk4NvVhXzREhutLWm7EE9smQ4XKHtWhqDddKit5wJ\nhlpahhOPrpyZzAjTB8zEs5PS9VgGt0Jj08AfdfNHDMkhhJj/V7+MFx7XHt8acnR4\nLqDR7usZC3vkR89jjU4KaaoD+6GsD5tpg1CQOHECgYEAwoqtch4dcxHx0u2PzXxc\naJxx+900zk8e5d9tta02N7B8/L9NGs4L8OzdQ93vFC5ESNSokGCU8u7W1GgILBGt\nieANO5wvPoKt+SzxFk2qVHWnzGCDCVAir/jPOHKUuxm915rVHfI9iJONsKzfxhAG\nvVzQev1ELkgCYWjELUxbC64=\n-----END PRIVATE KEY-----\n",
    "client_email": "final-project-lead-me@phonic-monolith-345108.iam.gserviceaccount.com",
    "client_id": "100061919088317530052",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/final-project-lead-me%40phonic-monolith-345108.iam.gserviceaccount.com"
}


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("YES@")
        user = User(role=form.role.data,
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
            name=form.name.data,
            id_m=form.id_m.data,
            phone=form.phone.data,
            gender=form.gender.data)

        db.session.add(user)
        print(user)

        db.session.commit()
        return redirect(url_for('branches.branch_register',manager_id=user.id))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not
        if user is not None:
            if user.check_password(form.password.data):

            #Log in the user
                login_user(user)
        else:
            return render_template('login.html', form=form)

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')
            print(next)

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.index')
                print(current_user.username)

                return redirect(next)
    return render_template('login.html', form=form)




@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        print("YES")
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        current_user.password = form.password.data
        db.session.commit()
        print("SUCCESS")
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.name.data = current_user.name
    return render_template('account.html', form=form)

#@users.route("/<username>")
#def user_posts(username):
#    page = request.args.get('page', 1, type=int)
#    user = User.query.filter_by(username=username).first_or_404()
#    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
#    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
