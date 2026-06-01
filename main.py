import datetime as dt
import pandas as pd
import random
import smtplib
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

birthday_people = {}

def birthday_checker(datafile):
    global birthday_names
    birthday_file = pd.read_csv(datafile)
    current_date = (dt.datetime.now().month, dt.datetime.now().day)
    for index, row in birthday_file.iterrows():
        if current_date == (int(row['month']),int(row['day'])):
            birthday_people[row['name']] = row['email']
    if len(birthday_people)>0:
        return True

def create_letter(name):
    with open(f"letter_templates/letter_{random.randint(1,3)}.txt","r") as letter:
        letter_template = letter.read()
        letter_content = letter_template.replace("[NAME]",name)
        letter_content = letter_content.replace("Your friend","Johnny")
    return letter_content

def send_email(name):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=birthday_people[name],
                            msg=f"Subject:Happy Birthday!\n\n{create_letter(name)}"
                            )
        
if birthday_checker("birthdays_updated.csv"):
    for name in birthday_people:
        send_email(name)

