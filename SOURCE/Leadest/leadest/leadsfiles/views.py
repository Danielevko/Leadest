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

# !/usr/bin/env python
# File name: first_part_analysis_clustering_leads.py
# Description: Clustering the leads
# Authors: Daniel Levkovitz - Tanya Filozof
# Date: 2022-04-14
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


def csvUpload(file):
    temp = []
    data_from_file = file.stream.read()  # This line uses the same variable and worked fine
    # Convert the FileStorage to list of lists here.

    stream = io.StringIO(data_from_file.decode("UTF8"), newline=None)
    reader = csv.reader(stream)
    for row in reader:
        temp.append(row)

    return temp


leads_files = Blueprint('leads_files', __name__)


@leads_files.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = Upload_Leads_File()
    if request.method == 'POST':
        count = 0
        file = request.files['file']
        data_file = csvUpload(file)
        headers = data_file.pop(0)
        df_leads = pd.DataFrame(data_file, columns=headers)
        now = datetime.datetime.now()
        dt_time = now.strftime('%Y-%m-%d %H:%M:%S')
        username = current_user.username
        exists = db.session.query(LeadsFile.user_id).filter_by(user_id=username).first() is not None
        count_from_sql = db.session.query(LeadsFile.user_id, func.count(LeadsFile.user_id)).group_by(
            LeadsFile.user_id).all()

        if exists == True:
            for value in count_from_sql:
                print(value)
                if value[0] == current_user.username:
                    count_for_user = (value[1])
            print(count_for_user)
            if count_for_user == 1:
                count_for_db = 2
                leads_file = LeadsFile(filename=file.filename, data=file.read(), user_id=username, date=now,
                                       counter=count_for_db)
                FILE_NAME = "{}_{}".format(leads_file.filename.split(".")[0], current_user.username)
                upload_to_gcp(df_leads, "final_project_leads/{}".format(current_user.username), FILE_NAME)
                db.session.add(leads_file)
                db.session.commit()
                part_two(FILE_NAME)
                return redirect(url_for('core.after_second'))
            if count_for_user >= 2:
                count_for_db = 3
                leads_file = LeadsFile(filename=file.filename, data=file.read(), user_id=username, date=now,
                                       counter=count_for_db)
                FILE_NAME = "{}_{}".format(leads_file.filename.split(".")[0], current_user.username)
                upload_to_gcp(df_leads, "final_project_leads/{}".format(current_user.username), FILE_NAME)
                db.session.add(leads_file)
                db.session.commit()
                uploaded_file_after_clustering = part_three(FILE_NAME)
                print(uploaded_file_after_clustering)
                return redirect(url_for('core.after_third'))
        else:
            count_for_db = 1
            print()
            leads_file = LeadsFile(filename=file.filename, data=file.read(), user_id=username, date=now,
                                   counter=count_for_db)
            FILE_NAME = "{}_{}".format(leads_file.filename.split(".")[0], current_user.username)
            upload_to_gcp(df_leads, "final_project_leads/{}".format(current_user.username), FILE_NAME)
            db.session.add(leads_file)
            db.session.commit()
            uploaded_file_after_clustering = part_one(FILE_NAME)
            print(uploaded_file_after_clustering)
            return redirect(url_for('core.after_first'))
    return render_template('upload.html', form=form)


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


def import_model(file_name, bucket_name):
    bucket_name = bucket_name.split("/")
    gcp_json_credentials_dict = json.loads(json.dumps(CREDENTIALS))
    creds = service_account.Credentials.from_service_account_info(gcp_json_credentials_dict)
    client = storage.Client(project=gcp_json_credentials_dict['project_id'], credentials=creds)
    try:
        for blob in client.list_blobs(bucket_name[0],
                                      prefix=bucket_name[1]):
            if file_name in str(blob):
                print(blob)
                return blob.download_as_string()
    except ValueError:
        print("File not found")


def calculate_age(born):
    today = datetime.date.today()
    return today.year - born


def checking_duplications(df_leads):
    # checking duplicates id leads
    if sum(df_leads.duplicated(subset='id_lead')) != 0:
        raise Exception("Duplications in id_lead column, Number of duplications: {}".format(
            len(df_leads['id_lead']) - len(df_leads['id_lead'].drop_duplicates())))
        return False
    elif sum(df_leads.duplicated(subset='id')) != 0:
        raise Exception("Duplications in id_lead column, Number of duplications: {}".format(
            len(df_leads['id']) - len(df_leads['id'].drop_duplicates())))
        return False
    else:
        print("No Duplication")
        return True


def today_date(i):
    today = datetime.date.today()
    return str(today)


def clean_amount_cars(df_cars, amount=30):
    """
    Return the indexes of cars with less than 30
    """
    temp_index_cars = []
    temp_car_names = list(set(df_cars['car'].values))
    for i in temp_car_names:
        if len(df_cars[df_cars['car'] == i]) < amount:
            temp_index_cars.append(df_cars[df_cars['car'] == i].index)
    temp_index_cars = [x for sublist in temp_index_cars for x in sublist]

    return temp_index_cars


def calc_car_prices_by_model_year(df_leads, df_cars):
    """
    Calculate the average car price based on the type and the year of the car, if there is no year information,
    calculate the average based on the type of car.
    """
    df_mean_car_by_model_and_year = df_cars.groupby(['car', 'model', 'year']).mean()
    df_mean_car_by_model_and_year['price'] = df_mean_car_by_model_and_year['price'].map(lambda x: round(x, 2))
    temp_prices = []
    for index, row in df_leads.iterrows():
        # If the car_type is in df_cars it will enter
        try:
            # Creating a new Dataframe which grouped by the car_type
            new_df = df_mean_car_by_model_and_year.loc[df_mean_car_by_model_and_year.index].loc[
                row['car_type']].reset_index()
            # If the car_model is in df_cars, will select only the prices of the model
            if row['car_model'] in new_df['model'].values:
                new_df = new_df[new_df['model'] == row['car_model']]
                # if there is info of model and year, will get the price of the model and year
                if row['car_year'] in new_df['year'].values:
                    temp = \
                        new_df[(new_df['model'] == row['car_model']) & (new_df['year'] == row['car_year'])][
                            'price'].values[
                            0]
                    temp = round(temp, 2)
                    temp_prices.append(temp)
                else:
                    # if not, will give the minimum year price.
                    temp_prices.append(new_df[new_df['price'] == min(new_df['price'])]['price'].values[0])
            else:
                # if there is no info of car_model, will give the car_price be year
                new_df = new_df.groupby(['year']).mean()
                if row['car_year'] in new_df.index:
                    temp_prices.append(new_df.loc[row['car_year']]['price'])
                else:
                    temp_prices.append(new_df.loc[min(new_df.index)]['price'])
        except:
            # If the car type is not located in df_cars it will calculate price by the car year
            new_df = df_cars.groupby(['year']).mean()
            if row['car_year'] in new_df.index:
                temp_prices.append(new_df.loc[row['car_year']]['price'])
            else:
                # if the year is not located it will calculate by the minimum year
                temp_prices.append(new_df.loc[min(new_df.index)]['price'])

    return temp_prices


def convert_time_to_categorical(x):
    if (x >= 4) and (x <= 7):
        return 'Early Morning'
    elif (x > 7) and (x <= 11):
        return 'Morning'
    elif (x > 11) and (x <= 15):
        return 'Noon'
    elif (x > 15) and (x <= 19):
        return 'After Noon'
    elif (x >= 20) and (x <= 23):
        return 'Evening'
    elif (x == 24) or (1 <= x <= 3):
        return "Night"
    else:
        return 'Late Night'


def calc_cluster_score(important_labels, new_labels, df_groupby_segmant_temp, df_groupby_segmant):
    for i, j in zip(important_labels, new_labels):
        if df_groupby_segmant[i].dtypes == np.float64:
            if i == 'age':
                df_groupby_segmant_temp[j] = df_groupby_segmant[i].rank(method='min', ascending=False)
                continue
            df_groupby_segmant_temp[j] = df_groupby_segmant[i].rank(method='max')
        else:
            if i == 'is_buisness':
                df_groupby_segmant_temp[j] = df_groupby_segmant[i].apply(lambda x: 1 if x == True else 0)
            elif i == 'department':
                df_groupby_segmant_temp[j] = df_groupby_segmant[i].apply(
                    lambda x: 1 if x in ['Administration', 'Marketing and sales', 'Human resources'] else 0)
            elif i == 'time_catagor':
                df_groupby_segmant_temp[j] = df_groupby_segmant[i].apply(
                    lambda x: 1 if x in ['Morning', 'Noon', 'After Noon'] else 0)

    return df_groupby_segmant_temp


def segment_result(x):
    if x == 1:
        return "low"
    elif x == 2:
        return "medium"
    elif x == 3:
        return "high"
    elif x == 4:
        return "hot"


def today_date(i):
    today = date.today()
    return str(today)


def send_email1(send_to, subject, df_leads, df_summary):
    send_from = "leadest.leadme@gmail.com"
    password = "wtuvidjflonghugz"
    subject2 = "Leadest - Segmentation Summary"

    message = """\
    <p>Thanks for using Leadme! <br>
    your Clustered CSV is attached to this email.</p>
        <p><br></p>
  Additionally, we sent you a CSV summary of what each Lead type means!
        <p><br></p>
    <p><strong>Greeting,</strong>
    <br>
    <strong>Leadest</strong></p>
    """
    for receiver in send_to:
        multipart = MIMEMultipart()
        multipart["From"] = send_from
        multipart["To"] = receiver
        multipart["Subject"] = subject
        attachment1 = MIMEApplication(df_leads.to_csv(index=False))
        attachment1["Content-Disposition"] = 'attachment; filename=" {}"'.format(f"{subject}.csv")
        attachment2 = MIMEApplication(df_summary.to_csv(index=False))
        attachment2["Content-Disposition"] = 'attachment; filename=" {}"'.format(f"{subject2}.csv")
        multipart.attach(attachment1)
        multipart.attach(attachment2)
        multipart.attach(MIMEText(message, "html"))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(multipart["From"], password)
        server.sendmail(multipart["From"], multipart["To"], multipart.as_string())
        server.quit()


def send_email2(send_to, subject, df):
    send_from = "leadest.leadme@gmail.com"
    password = "wtuvidjflonghugz"

    message = "<p>Thanks for using Leadme! <br> We learned the best model which is {} and saved it in our cloud. <br> The accuracy of the learning model was {}  <br>Next time you will use Leadme we will predict which lead will become a sell!</p> <p><br></p> <p><strong>Greetings </strong><br><strong>Leadest</strong></p>".format(
        df.index[0], df['Accuracy'][0])
    for receiver in send_to:
        multipart = MIMEMultipart()
        multipart["From"] = send_from
        multipart["To"] = receiver
        multipart["Subject"] = subject
        multipart.attach(MIMEText(message, "html"))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(multipart["From"], password)
        server.sendmail(multipart["From"], multipart["To"], multipart.as_string())
        server.quit()


def send_email3(send_to, subject, df_leads, df_summary):
    send_from = "leadest.leadme@gmail.com"
    password = "wtuvidjflonghugz"
    subject2 = "Leadest - Segmentation Summary"

    message = """\
    <p>Thanks for using Leadme! <br>
    We predicted for you which lead will become a sell!</p>
    <p><br></p>
    <p><strong>Greetings&nbsp;</strong><br><strong>Leadest</strong></p>
    """
    for receiver in send_to:
        multipart = MIMEMultipart()
        multipart["From"] = send_from
        multipart["To"] = receiver
        multipart["Subject"] = subject
        attachment1 = MIMEApplication(df_leads.to_csv(index=False))
        attachment1["Content-Disposition"] = 'attachment; filename=" {}"'.format(f"{subject}.csv")
        attachment2 = MIMEApplication(df_summary.to_csv(index=False))
        attachment2["Content-Disposition"] = 'attachment; filename=" {}"'.format(f"{subject2}.csv")
        multipart.attach(attachment1)
        multipart.attach(attachment2)
        multipart.attach(MIMEText(message, "html"))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(multipart["From"], password)
        server.sendmail(multipart["From"], multipart["To"], multipart.as_string())
        server.quit()


def part_one(FILE_FROM_CLIENT):
    begin = time()

    """
    Part 1
    Importing Datasets from GCP
    """

    df_companies = import_from_gcp("Companies Data", "final_project_leads")
    df_leads = import_from_gcp(FILE_FROM_CLIENT,
                               "final_project_leads/{}".format(current_user.username))
    df_cars = import_from_gcp("vehicles4", "final_project_leads")

    """
    Part 2
    Checking duplications in the PK of df_leads
    """

    if not checking_duplications(df_leads):
        # Ask the client if he wants to delete the duplication
        df_leads.drop_duplicates(subset=['id_lead'], keep='first', inplace=True)
        df_leads.drop_duplicates(subset=['id'], keep='first', inplace=True)

    """
    Part 3: Data Preprocessing

    3.1 Data Cleaning
    """

    """
    3.1.1 Data Cleaning - Companies
    """

    # Cleaning the Companies Dataset
    df_companies = df_companies[df_companies['Market Cap'] != '-']
    df_companies = df_companies[df_companies['Market Cap'].notna()]
    df_companies = df_companies[df_companies['company_name'].map(lambda x: x.isascii())]

    """
    3.1.2 Data Cleaning - Cars
    """

    # Cleaning cars whose year is less than 1998
    df_cars = df_cars[df_cars['year'] >= df_leads['car_year'].min()]

    # Delete cars that we don't have data on their price
    df_cars = df_cars[df_cars.price != 0]

    # Cleaning cars that do not include the manufacturer from df_leads

    manufacturers_to_drop = np.unique(df_cars['car'])[
        ~np.in1d(np.unique(df_cars['car']), np.unique(df_leads['car_type']))].tolist()
    df_cars = df_cars[df_cars.car.isin(manufacturers_to_drop) == False]

    # Cleaning cars that do not include the same model from df_leads
    models_to_drop = np.asarray(list(set(df_cars['model'])))[
        ~np.in1d(np.asarray(list(set(df_cars['model']))), np.unique(df_leads['car_model']))]
    df_cars = df_cars[df_cars.model.isin(models_to_drop) == False]

    """
    3.2 Data Transformation
    Part 3.2.1 - df_leads
    """
    # Calculate lead age
    df_leads['age'] = df_leads['year_of_birth'].apply(calculate_age)

    # Calculate the car price for each lead
    df_leads['car_price'] = calc_car_prices_by_model_year(df_leads, df_cars)

    # Convert dates to date type in df_leads
    # Convert to datetime to proper datatype
    df_leads['rental_period'] = pd.to_datetime(df_leads['rental_period'], format='%d/%m/%Y')
    df_leads['creation_date'] = pd.to_datetime(df_leads['creation_date'], format='%d/%m/%Y')

    # Create a new column based on creation_date and rental_period that calculates the difference between them,
    # called 'desirable_rental_days'
    df_leads['desirable_rental_days'] = df_leads['rental_period'] - df_leads['creation_date']
    df_leads['desirable_rental_days'] = df_leads['desirable_rental_days'].dt.days

    # Verify that the users filled out the rental period correctly
    if len(df_leads[df_leads['desirable_rental_days'] < 0]) >= 1:
        raise Exception("User filled incorrect the rental period")
    else:
        print("desirable_rental_days is good")

    # Create column 'time_category' based on 'creation_time' in df_leads to Categorical
    df_leads['time_catagor'] = df_leads.apply(lambda x: convert_time_to_categorical(x['creation_time']), axis=1)

    """
    Data Transformation
    Part 3.2.2 - df_companies
    """

    # verify all the data in columns Market Cap and Profit is numeric
    try:
        df_companies['Market Cap'] = pd.to_numeric(df_companies['Market Cap'])
        df_companies['profit'] = pd.to_numeric(df_companies['profit'])
        print("Transform numeric columns in df companies successfully")
    except:
        print("Error occurred in converting Profit and Market Cap")

    # Create a copy of df_companies
    df_company_to_merge = df_companies.copy()
    # Drop unwanted columns in df_company_to_merge
    df_company_to_merge.drop(
        ['id_company', 'num. of employees', 'profitable', 'rank_change', 'rank', 'city', 'state', 'newcomer',
         'ceo_founder',
         'ceo_woman', 'prev_rank', 'CEO', 'Website', 'Ticker', 'sector', 'revenue'], inplace=True, axis=1)

    """
    Part 3.3
    Data Merge
    """

    # Make a copy of df_leads before merge
    df_leads_for_analysis = df_leads.copy()
    # Ensure that df_leads is sorted by 'id_lead'
    df_leads_for_analysis.sort_values(by="id_lead", inplace=True)

    # Merge df_company_to_merge and df_leads
    df_leads_for_analysis = df_leads.merge(df_company_to_merge, on='company_name', sort=False)
    df_leads_for_analysis.sort_values(by="id_lead", inplace=True)

    """
    Part 3.4
    Apply the Standard Scaler to numeric columns
    """

    # Keep the dataset after the preprocessing before the StandardScaler
    # This is the Dataset the client will get to perform sales
    df_leads_app = df_leads_for_analysis.copy()

    # Delete unwanted columns from df_leads_for_analysis

    df_leads_for_analysis.drop(
        ['id', 'id_lead', 'first_name', 'last_name', 'email', 'year_of_birth', 'country', 'address', 'creation_date',
         'rental_period', 'car_type', 'company_name', 'creation_time', 'car_model'], axis=1, inplace=True)

    # Preprocessing the Numeric Data using StandardScaler
    scaler = preprocessing.StandardScaler()
    df_leads_for_analysis[
        ['car_year', 'age', 'desirable_rental_days', 'car_price', 'Market Cap', 'profit']] = scaler.fit_transform(
        df_leads_for_analysis[['car_year', 'age', 'desirable_rental_days', 'car_price', 'Market Cap', 'profit']])

    """Part 4: K - Prototypes Algorithm

    k-prototypes clustering algorithm for mixed numerical/categorical data.

    Parameters
    -----------
    n_clusters : int, optional.
        The number of clusters to form as well as the number of
        centroids to generate.

    max_iter : int, default: 100
        Maximum number of iterations of the k-modes algorithm for a
        single run.

    n_init : int, default: 10
        Number of time the k-modes algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of cost.

    init : {'Huang', 'Cao', 'random' or a list of ndarrays}, default: 'Cao'
        Method for initialization:
        'Huang': Method in Huang [1997, 1998]
        'Cao': Method in Cao et al. [2009]
        'random': choose 'n_clusters' observations (rows) at random from
        data for the initial centroids.
        If a list of ndarrays is passed, it should be of length 2, with
        shapes (n_clusters, n_features) for numerical and categorical
        data respectively. These are the initial encoded centroids.

    verbose : integer, optional
        Verbosity mode.

    random_state : int, RandomState instance or None, optional, default: None
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    n_jobs : int, default: 1
        The number of jobs to use for the computation. This works by computing
        each of the n_init runs in parallel.
        If -1 all CPUs are used. If 1 is given, no parallel computing code is
        used at all, which is useful for debugging. For n_jobs below -1,
        (n_cpus + 1 + n_jobs) are used. Thus for n_jobs = -2, all CPUs but one
        are used.

    Notes
    -----
    See:
    Huang, Z.: Extensions to the k-modes algorithm for clustering large
    data sets with categorical values, Data Mining and Knowledge
    Discovery 2(3), 1998.
    https://github.com/nicodv/kmodes/blob/master/kmodes/kprototypes.py
    """

    # Creating list of categorical columns
    categorical_columns = [i for i in range(len(np.array(df_leads_for_analysis.dtypes))) if
                           np.array(df_leads_for_analysis.dtypes)[i] != np.dtype('float64')]

    # Using K-Prototypes Algorithm
    kproto = KPrototypes(n_jobs=-1, n_clusters=4, random_state=6, init='Cao', verbose=1, max_iter=100, n_init=10)
    clusters = kproto.fit_predict(df_leads_for_analysis, categorical=categorical_columns)

    """
    Part 5 Analyzing our KPI's and segmenting the leads
    """

    # Make sure our DF to the customer is sorted by 'id_lead' column
    df_leads_app.sort_values('id_lead', inplace=True)

    # Create a copy of the DF for the customer to use for making decisions about the KPI
    result_data = df_leads_app.copy()

    result_data['lead_type'] = clusters

    # Rename the numerical clusters
    result_data['Segment'] = result_data['lead_type'].map({0: 'First', 1: 'Second', 2: 'Third', 3: 'Forth'})
    # Order the cluster
    result_data['Segment'] = result_data['Segment'].astype('category')
    result_data['Segment'] = result_data['Segment'].cat.reorder_categories(['First', 'Second', 'Third', 'Forth'])

    # Creating a temp Dataframe to give a score for each attribute
    result_data.rename(columns={'lead_type': 'Total'}, inplace=True)
    df_groupby_segmant = result_data.groupby('Segment').agg(
        {
            'Total': 'count',
            'is_buisness': lambda x: x.value_counts().index[0],
            'gender': lambda x: x.value_counts().index[0],
            'department': lambda x: x.value_counts().index[0],
            'car_year': 'median',
            'platform': lambda x: x.value_counts().index[0],
            'age': 'median',
            'car_price': 'mean',
            'desirable_rental_days': 'median',
            'time_catagor': lambda x: x.value_counts().index[0],
            'Market Cap': 'mean',
            'profit': 'mean'
        }
    ).reset_index()

    """
    Part 5.1 - Scoring the results
    """

    df_groupby_segmant_temp = pd.DataFrame()

    important_labels = ['is_buisness', 'department', 'car_year', 'age', 'car_price', 'desirable_rental_days',
                        'time_catagor', 'profit', 'Market Cap']

    new_labels = ['is_buisness_score', 'department_score', 'car_year_score', 'age_score', 'car_price_score',
                  'desirable_rental_days_score', 'time_catagor_score', 'profit_score', 'Market Cap_score']

    ### Scoring output
    df_groupby_segmant_temp['rank'] = calc_cluster_score(new_labels=new_labels, important_labels=important_labels,
                                                         df_groupby_segmant_temp=df_groupby_segmant_temp,
                                                         df_groupby_segmant=df_groupby_segmant).sum(axis=1).rank()
    # Apply the segmentation on result_data
    result_data['Segment_Result'] = result_data['Segment'].map(
        {'First': df_groupby_segmant_temp['rank'][0], 'Second': df_groupby_segmant_temp['rank'][1],
         'Third': df_groupby_segmant_temp['rank'][2], 'Forth': df_groupby_segmant_temp['rank'][3]})
    result_data['Segment_order'] = result_data['Segment'].map(
        {'First': df_groupby_segmant_temp['rank'][0], 'Second': df_groupby_segmant_temp['rank'][1],
         'Third': df_groupby_segmant_temp['rank'][2], 'Forth': df_groupby_segmant_temp['rank'][3]})
    result_data['Segment_Result'] = result_data['Segment_Result'].apply(lambda x: segment_result(x))
    ## Order back by id_lead
    result_data.sort_values('id_lead', inplace=True)

    # Create a CSV file to summarize the results

    counter = 0
    df_groupby_segmant['Segment'] = df_groupby_segmant['Segment'].astype('string')
    for i in df_groupby_segmant_temp['rank']:
        df_groupby_segmant['Segment'].at[counter] = str(i)
        counter += 1
    counter = 0
    df_groupby_segmant.sort_values(by='Segment', inplace=True, ascending=False)
    for i in df_groupby_segmant_temp['rank']:
        df_groupby_segmant['Segment'].at[counter] = segment_result(int(i))
        counter += 1

    # df_leads_app is the Dataframe that the client will get, arranging the results
    df_leads_app['Segment_order'] = result_data['Segment_order']
    df_leads_app['Segment_order'] = df_leads_app['Segment_order'].astype(np.int32)
    df_leads_app['segment'] = result_data['Segment_Result']

    #  Order the Dataframe by the Segment (First - Hot, Second - High, Third - Medium, Forth - Low)

    df_leads_app.sort_values(by="Segment_order", inplace=True, ascending=False)
    df_leads_app.drop("Segment_order", axis=1, inplace=True)

    """
    Part 6 - Upload the file to GCP
    """
    #    Transform the DF to dask.dataframe and upload to the Cloud
    upload_results = upload_to_gcp(df_leads_app, "final_project_leads/{}".format(current_user.username),
                                   "leads_after_clustering")
    if upload_results[0]:
        print("{} uploaded successfully".format(upload_results[1]))

    send_email1([current_user.email], "Leadest - Clustered CSV File", df_leads_app, df_groupby_segmant)
    print("Email sent")

    # Calculate the script running time
    end = time()

    print('Script running time: {} seconds'.format(round(end - begin), 2))
    return (upload_results[1])


def logistic_regression(X_train, y_train, X_test):
    logmodel = LogisticRegression(random_state=100)
    logmodel.fit(X_train, y_train)
    predictions_logmodel = logmodel.predict(X_test)
    return predictions_logmodel, logmodel


def decision_tree(X_train, y_train, X_test):
    dt = DecisionTreeClassifier(random_state=101)
    dt.fit(X_train, y_train)
    return dt.predict(X_test), dt


def cv_decision_tree(X_train, y_train, X_test):
    params = {'max_depth': list(range(1, 10)),
              'min_samples_split': [2, 3, 4, 5],
              'min_samples_leaf': [1, 2, 3, 4, 5]}
    cv_dt = GridSearchCV(estimator=tree.DecisionTreeClassifier(), param_grid=params)
    cv_dt.fit(X_train, y_train)
    return cv_dt.predict(X_test), cv_dt


def random_forest(X_train, y_train, X_test):
    rfc = RandomForestClassifier(n_estimators=1500, random_state=6)
    rfc.fit(X_train, y_train)
    return rfc.predict(X_test), rfc


def return_the_best_model(*args, y_test):
    df_metrics = pd.DataFrame(index=["logmodel", "decision_tree", "decision_tree_cv", "random_forest"],
                              columns=["Accuracy", "Precision", "Recall", "F1-Score"])
    acc_list = []
    precision_list = []
    rc_list = []
    f1score_list = []
    for i in args:
        acc_list.append(metrics.accuracy_score(y_test, i))
        precision_list.append(metrics.precision_score(y_test, i))
        rc_list.append(metrics.recall_score(y_test, i))
        f1score_list.append(metrics.f1_score(y_test, i))
    df_metrics["Accuracy"] = acc_list
    df_metrics["Precision"] = precision_list
    df_metrics["Recall"] = rc_list
    df_metrics["F1-Score"] = f1score_list
    df_metrics["Sum"] = df_metrics.sum(axis=1)
    df_metrics["Rank"] = df_metrics["Sum"].rank()
    print(df_metrics)
    return df_metrics[df_metrics["Sum"] == max(df_metrics["Sum"])]


def save_the_best_model(df_metrics, logmodel, dt, cv_dt, rfc):
    if 'log' in df_metrics.index[0]:
        return pickle.dumps(logmodel)
    elif 'decision_tree' in df_metrics.index[0]:
        return pickle.dumps(dt)
    elif 'decision_tree_cv' in df_metrics.index[0]:
        return pickle.dumps(cv_dt)
    elif "random_forest" in df_metrics.index[0]:
        return pickle.dumps(rfc)


def part_two(FILE_FROM_CLIENT):
    begin = time()

    # Ignore Warnings
    warnings.filterwarnings('ignore')

    # Define the Random Seed
    np.random.seed(1)
    random.seed(1)
    """
    Part 1
    Importing Datasets from GCP
    """
    df_companies = import_from_gcp("Companies Data", "final_project_leads")
    df_leads = import_from_gcp(FILE_FROM_CLIENT, "final_project_leads/{}".format(current_user.username))

    """
    Part 2
    Checking duplications in the PK of df_leads
    """
    if not checking_duplications(df_leads):
        df_leads.drop_duplicates(subset=['id_lead'], keep='first', inplace=True)
        df_leads.drop_duplicates(subset=['id'], keep='first', inplace=True)

    """
    Part 3: Data Preprocessing

    3.1 Merge df_companies for revenue data
    """
    df_company_to_merge = df_companies.copy()
    df_company_to_merge.drop(
        ['id_company', 'num. of employees', 'profitable', 'rank_change', 'rank', 'city', 'state', 'newcomer',
         'ceo_founder', 'ceo_woman', 'prev_rank', 'CEO', 'Website', 'Ticker', 'sector', 'Market Cap', 'profit'],
        inplace=True, axis=1)
    df_leads_for_analysis = df_leads.merge(df_company_to_merge, on='company_name', sort=False)

    """
    Part 3: Data Preprocessing

    3.2 Drop unwanted columns
    """

    df_leads_for_analysis.drop(
        ['id', 'id_lead', 'first_name', 'last_name', 'email', 'year_of_birth', 'country', 'address', 'creation_date',
         'rental_period', 'car_type', 'company_name', 'time_catagor', 'car_model', 'segment'], axis=1, inplace=True)

    """
    Part 3: Data Preprocessing

    3.3 Converting Categorical Features
    """

    df_leads_for_analysis['is_buisness'] = df_leads_for_analysis['is_buisness'].map(
        {True: 'True', False: 'False'})  # Replace boolean to string

    categorical_columns = [i for i in range(len(np.array(df_leads_for_analysis.dtypes))) if
                           np.array(df_leads_for_analysis.dtypes)[i] not in [np.dtype('float64'), np.dtype('int64')]]

    df_dummies = pd.get_dummies(df_leads_for_analysis[df_leads_for_analysis.columns[categorical_columns]],
                                drop_first=True)

    # Drop the Categorical columns from df_leads_for_analysis
    df_leads_for_analysis.drop(df_leads_for_analysis.columns[categorical_columns], axis=1, inplace=True)

    # Concat all the df_dummies
    df_leads_for_analysis = pd.concat([df_leads_for_analysis, df_dummies], axis=1)

    print("Finished Pre-processing")

    """
    Part 4: Splitting the Data to train and test
    """

    print("Splitting the data to Train and Test")
    X_train, X_test, y_train, y_test = train_test_split(df_leads_for_analysis.drop('is_sold_sold', axis=1),
                                                        df_leads_for_analysis['is_sold_sold'], test_size=0.25,
                                                        random_state=1834)
    """
    Part 5: Model selection
    """

    print("Part 5: Training the models")
    log_model = logistic_regression(X_train, y_train, X_test)
    dt_model = decision_tree(X_train, y_train, X_test)
    cv_dt_model = cv_decision_tree(X_train, y_train, X_test)
    rf_model = random_forest(X_train, y_train, X_test)

    """
    Part 6: Model selection
    """
    print("Select the best model")
    df_metrics = return_the_best_model(log_model[0], dt_model[0], cv_dt_model[0], rf_model[0], y_test=y_test)

    print("The best model is {}".format(df_metrics.index[0]))

    """
    Part 7: Save the best model
    """

    model_to_save = save_the_best_model(df_metrics, log_model[1], dt_model[1], cv_dt_model[1], rf_model[1])

    """
    Part 8: Upload to cloud
    """

    file_name = "best_model_{}".format(df_metrics.index[0])

    gcp_json_credentials_dict = json.loads(json.dumps(CREDENTIALS))
    creds = service_account.Credentials.from_service_account_info(gcp_json_credentials_dict)
    client = storage.Client(project=gcp_json_credentials_dict['project_id'], credentials=creds)

    bucket = client.bucket('final_project_leads')

    bucket.blob("{}/{}".format(current_user.username, file_name)).upload_from_string(model_to_save,
                                                                                     content_type='application/octet-stream')
    print("{} was uploaded to the cloud".format(file_name))

    # Calculate the script running time
    end = time()

    send_email2([current_user.email], "Leadest - Model was trainded", df_metrics)
    print("Email was sent")

    print('Script running time: {} seconds'.format(round(end - begin), 2))

    return file_name


def part_three(FILE_NAME_FROM_CLIENT):
    begin = time()
    # Ignore Warnings
    warnings.filterwarnings('ignore')
    """
        Part 1: Import from the Cloud

        Part 1.1
        Import best model from GCP
        """

    model = pickle.loads(import_model("best_model", "final_project_leads/{}".format(current_user.username)))

    """
    Part 1.2
    Import Companies and Cars Data from GCP
    """

    df_companies = import_from_gcp("Companies Data", "final_project_leads")
    df_leads = import_from_gcp(FILE_NAME_FROM_CLIENT, "final_project_leads/{}".format(current_user.username))
    df_cars = import_from_gcp("vehicles4", "final_project_leads")

    """
    Part 2
    Checking duplications in the PK of df_leads
    """

    if not checking_duplications(df_leads):
        # Ask the client if he wants to delete the duplication
        df_leads.drop_duplicates(subset=['id_lead'], keep='first', inplace=True)
        df_leads.drop_duplicates(subset=['id'], keep='first', inplace=True)

    """
    Part 3: Data Preprocessing

    3.1 Data Cleaning
    """

    """
    3.1.1 Data Cleaning - Companies
    """

    # Cleaning the Companies Dataset
    df_companies = df_companies[df_companies['Market Cap'] != '-']
    df_companies = df_companies[df_companies['Market Cap'].notna()]
    df_companies = df_companies[df_companies['company_name'].map(lambda x: x.isascii())]

    """
    3.1.2 Data Cleaning - Cars
    """

    # Cleaning cars whose year is less than 1998
    df_cars = df_cars[df_cars['year'] >= df_leads['car_year'].min()]

    # Delete cars that we don't have data on their price
    df_cars = df_cars[df_cars.price != 0]

    # Cleaning cars that do not include the manufacturer from df_leads

    manufacturers_to_drop = np.unique(df_cars['car'])[
        ~np.in1d(np.unique(df_cars['car']), np.unique(df_leads['car_type']))].tolist()
    df_cars = df_cars[df_cars.car.isin(manufacturers_to_drop) == False]

    # Cleaning cars that do not include the same model from df_leads
    models_to_drop = np.asarray(list(set(df_cars['model'])))[
        ~np.in1d(np.asarray(list(set(df_cars['model']))), np.unique(df_leads['car_model']))]
    df_cars = df_cars[df_cars.model.isin(models_to_drop) == False]

    """
    3.2 Data Transformation
    Part 3.2.1 - df_leads
    """

    # Calculate lead age
    df_leads['age'] = df_leads['year_of_birth'].apply(calculate_age)

    # Calculate the car price for each lead
    df_leads['car_price'] = calc_car_prices_by_model_year(df_leads, df_cars)

    # Convert dates to date type in df_leads
    # Convert to datetime to proper datatype
    df_leads['rental_period'] = pd.to_datetime(df_leads['rental_period'], format='%d/%m/%Y')
    df_leads['creation_date'] = pd.to_datetime(df_leads['creation_date'], format='%d/%m/%Y')

    # Create a new column based on creation_date and rental_period that calculates the difference between them,
    # called 'desirable_rental_days'
    df_leads['desirable_rental_days'] = df_leads['rental_period'] - df_leads['creation_date']
    df_leads['desirable_rental_days'] = df_leads['desirable_rental_days'].dt.days

    # Verify that the users filled out the rental period correctly
    if len(df_leads[df_leads['desirable_rental_days'] < 0]) >= 1:
        raise Exception("User filled incorrect the rental period")
    else:
        print("desirable_rental_days is good")

    """
    Data Transformation
    Part 3.2.2 - df_companies
    """

    # verify all the data in columns Market Cap and Profit is numeric
    try:
        df_companies['Market Cap'] = pd.to_numeric(df_companies['Market Cap'])
        df_companies['profit'] = pd.to_numeric(df_companies['profit'])
        print("Transform numeric columns in df companies successfully")
    except:
        print("Error occurred in converting Profit and Market Cap")

    # Create a copy of df_companies
    df_company_to_merge = df_companies.copy()
    # Drop unwanted columns in df_company_to_merge
    df_company_to_merge.drop(
        ['id_company', 'num. of employees', 'profitable', 'rank_change', 'rank', 'city', 'state', 'newcomer',
         'ceo_founder', 'ceo_woman', 'prev_rank', 'CEO', 'Website', 'Ticker', 'sector'], inplace=True, axis=1)

    """
    Part 3.3
    Data Merge
    """

    # Make a copy of df_leads before merge
    df_leads_for_analysis = df_leads.copy()
    # Ensure that df_leads is sorted by 'id_lead'
    df_leads_for_analysis.sort_values(by="id_lead", inplace=True)

    # Merge df_company_to_merge and df_leads
    df_leads_for_analysis = df_leads.merge(df_company_to_merge, on='company_name', sort=False)
    df_leads_for_analysis.sort_values(by="id_lead", inplace=True)

    # Keep the dataset after the preprocessing before the StandardScaler
    # This is the Dataset the client will get to perform sales
    df_leads_app = df_leads_for_analysis.copy()

    # Drop unwanted columns from df_leads_for_analysis

    df_leads_for_analysis.drop(
        ['id', 'id_lead', 'first_name', 'last_name', 'email', 'year_of_birth', 'country', 'address', 'creation_date',
         'rental_period', 'car_type', 'company_name', 'car_model'], axis=1, inplace=True)

    """
    Part 3.3
    Converting Categorical Features
    """

    # Convert the 'is_buisness' boolean column to String type
    df_leads_for_analysis['is_buisness'] = df_leads_for_analysis['is_buisness'].map(
        {True: 'True', False: 'False'})  # Replace boolean to string

    # Creating list of categorical columns

    categorical_columns = [i for i in range(len(np.array(df_leads_for_analysis.dtypes))) if
                           np.array(df_leads_for_analysis.dtypes)[i] not in [np.dtype('float64'), np.dtype(
                               'int64')]]
    # Create a dummy DataFrame

    df_dummies = pd.get_dummies(df_leads_for_analysis[df_leads_for_analysis.columns[categorical_columns]],
                                drop_first=True)

    # Drop the Categorical columns from df_leads_for_analysis

    df_leads_for_analysis.drop(df_leads_for_analysis.columns[categorical_columns], axis=1, inplace=True)

    # Concat all the df_dummies

    df_leads_for_analysis = pd.concat([df_leads_for_analysis, df_dummies], axis=1)

    print("Data pre-processing completed successfully")

    """
    Part 4
    Make predictions
    """
    predictions = model.predict(df_leads_for_analysis)
    df_leads_app['is_sold'] = predictions

    # Sort by is_sold
    df_leads_app = df_leads_app.sort_values('is_sold', ascending=False)

    """
    Part 4
    Make Summary CSV File
    """

    result_data = df_leads_app.copy()
    result_data['Result'] = result_data['is_sold'].map({0: 'No', 1: 'Yes'})
    # Order the cluster
    result_data['Result'] = result_data['is_sold'].astype('category')

    result_data.rename(columns={'is_sold': 'Total'}, inplace=True)
    df_groupby_segmant = result_data.groupby('Result').agg(
        {
            'Total': 'count',
            'is_buisness': lambda x: x.value_counts().index[0],
            'gender': lambda x: x.value_counts().index[0],
            'department': lambda x: x.value_counts().index[0],
            'car_year': 'median',
            'platform': lambda x: x.value_counts().index[0],
            'age': np.mean,
            'car_price': 'mean',
            'desirable_rental_days': 'median',
            'Market Cap': 'mean',
            'profit': 'mean'
        }
    ).reset_index()

    """
    Part 5 - Upload the file to GCP
    """
    #    Transform the DF to dask.dataframe and upload to the Cloud
    upload_results = upload_to_gcp(df_leads_app, "final_project_leads/{}".format(current_user.username),
                                   "leads_after_clustering")
    if upload_results[0]:
        print("{} uploaded successfully".format(upload_results[1]))

    send_email3([current_user.email], "Leadest - Predicted CSV File", df_leads_app, df_groupby_segmant)
    print("Email sent")

    # Calculate the script running time
    end = time()

    print('Script running time: {} seconds'.format(round(end - begin), 2))
    return (upload_results[1])
