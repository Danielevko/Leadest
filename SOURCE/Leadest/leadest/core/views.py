from flask import render_template, request, Blueprint
from leadest.models import LeadsFile
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import gcsfs
from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
from leadest.core.forms import Upload_for_dashboard
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from leadest import db
from leadest.models import LeadsFile
from io import BytesIO
from leadest.leadsfiles.forms import Upload_Leads_File
from flask import Flask, render_template, request, send_file
import pandas as pd
from io import StringIO
import dask.dataframe as dd
from datetime import datetime
import numpy
import csv
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import gcsfs
import io
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import datetime
from time import time
import warnings
from datetime import date
from sklearn import preprocessing
from datetime import date
from kmodes.kprototypes import KPrototypes
import random
import sklearn.metrics as metrics
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn import preprocessing
import pickle
from google.cloud import storage
from google.oauth2 import service_account
import json
from sklearn.model_selection import GridSearchCV
from sqlalchemy import func
import smtplib

CREDENTIALS = {
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


def today_date(i):
    today = datetime.date.today()
    return str(today)


def csvUpload(file):
    temp = []
    data_from_file = file.stream.read()  # This line uses the same variable and worked fine
    # Convert the FileStorage to list of lists here.

    stream = io.StringIO(data_from_file.decode("UTF8"), newline=None)
    reader = csv.reader(stream)
    for row in reader:
        temp.append(row)

    return temp


def import_from_gcp(file_name, bucket_name):
    PROJECT_NAME = 'final-project-lead-me'

    URL = "gs://"

    # Creating a pythonic file-system interface to Google Cloud Storage.
    fs = gcsfs.GCSFileSystem(project=PROJECT_NAME)
    for i in fs.ls(bucket_name):
        if file_name in i:
            print(i)
            return pd.read_csv(URL + i, storage_options={"token": CREDENTIALS}, encoding="ISO-8859-1")
    return print("File not found")


def upload_to_gcp(df, bucket_name, file_name):
    ddf = dd.from_pandas(df, npartitions=1, sort=False)
    print(bucket_name, file_name)
    file_name = ddf.to_csv('gs://{}/{}-*.csv'.format(bucket_name, file_name), index=False, sep=',', header=True,
                           name_function=today_date, storage_options={'token': CREDENTIALS})
    return [True, file_name]


core = Blueprint('core', __name__)


@core.route('/')
def index():
    return render_template('index.html')


@core.route('/info')
def info():
    return render_template('info.html')


@core.route('/after_first')
def after_first():
    return render_template('after_first.html')


@core.route('/after_second')
def after_second():
    return render_template('after_second.html')


@core.route('/after_third')
def after_third():
    return render_template('after_third.html')


@core.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'))
        if 'is_sold' in df:
            File_for_dashboard = 'File_for_dashboard_sold'
            FILE_NAME = "{}_{}".format(File_for_dashboard, current_user.username)
            upload_to_gcp(df, "final_project_leads/{}".format(current_user.username), FILE_NAME)
            return render_template('dashboard_1.html')
        else:
            File_for_dashboard = 'File_for_dashboard_not_sold'
            FILE_NAME = "{}_{}".format(File_for_dashboard, current_user.username)
            upload_to_gcp(df, "final_project_leads/{}".format(current_user.username), FILE_NAME)
            return render_template('dashboard_2.html')
    return render_template('dashboard.html')


@core.route('/chart1')
def chart1():
    FILE_FROM_CLIENT = 'File_for_dashboard_sold'
    df = import_from_gcp(FILE_FROM_CLIENT, "final_project_leads/{}".format(current_user.username))

    fig = px.bar(df, x="is_sold", y="car_price", color="is_buisness", barmode="group")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Car Price vs. Is sold"
    description = 'Above is a graph showing Car Price vs. Is sold. Divided by if the customer was a business customer.'
    return render_template('chart1.html', graphJSON=graphJSON, header=header, description=description)


@core.route('/chart2')
def chart2():
    FILE_FROM_CLIENT = 'File_for_dashboard_sold'
    df = import_from_gcp(FILE_FROM_CLIENT, "final_project_leads/{}".format(current_user.username))
    fig = px.scatter(df, x="car_price", y="car_year", color="is_sold")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Car year vs. Car price"
    description = """
    Above is a graph showing the year of a car, compared with its price, divided by whether it sold.
    """
    return render_template('chart1.html', graphJSON=graphJSON, header=header, description=description)


@core.route('/chart3')
def chart3():
    FILE_FROM_CLIENT = 'File_for_dashboard_sold'
    df = import_from_gcp(FILE_FROM_CLIENT, "final_project_leads/{}".format(current_user.username))

    fig = px.histogram(df, x="segment", color="is_sold")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Is Sold vs. Segment"
    description = """
       In the chart above you can see how many leads were sold, divided by their segment based on the unsupervised algorithm.
        """
    return render_template('chart1.html', graphJSON=graphJSON, header=header, description=description)


@core.route('/chart4')
def chart4():
    FILE_FROM_CLIENT = 'File_for_dashboard_not_sold'
    df = import_from_gcp(FILE_FROM_CLIENT, "final_project_leads/{}".format(current_user.username))
    fig = px.histogram(df, x="creation_time", color="is_buisness")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Creation Time vs. Is Business"
    description = ("\n"
                   "Above is a graph showing the lead counts by hour versus if it was a business lead.")
    return render_template('chart1.html', graphJSON=graphJSON, header=header, description=description)


@core.route('/chart5')
def chart5():
    FILE_FROM_CLIENT = 'File_for_dashboard_not_sold'
    df = import_from_gcp(FILE_FROM_CLIENT, "final_project_leads/{}".format(current_user.username))
    fig = px.histogram(df, x="platform", color="is_buisness")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Platform vs. Is Business"
    description = """
    Above is a graph showing the lead counts by platform versus if it was a business lead.
    """
    return render_template('chart1.html', graphJSON=graphJSON, header=header, description=description)


@core.route('/chart6')
def chart6():
    FILE_FROM_CLIENT = 'File_for_dashboard_not_sold'
    df = import_from_gcp(FILE_FROM_CLIENT, "final_project_leads/{}".format(current_user.username))
    fig = px.scatter(df, x="car_year", y="year_of_birth", color="platform")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Car Year vs. Year of Birth"
    description = """
    The graph above shows birth year versus wanted car year, divided by platform.
    """
    return render_template('chart1.html', graphJSON=graphJSON, header=header, description=description)
