from flask import Flask, render_template, request, redirect, url_for,jsonify,make_response, session
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql as sql
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from passlib.hash import pbkdf2_sha256 as sha
import requests
from flask_mail import *
import os




app = Flask(__name__) 

#app.secret_key = "gssgsfg874873y498r2bchy3g87e32894yc89yb3q894y98"
app.secret_key = "hijfpipjjpijeijijiohohiohgyyhfuifjij123445pjpijpij"
app.config['UPLOAD_FOLDER'] = 'static/'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='jaladjhamb@gmail.com'
app.config['MAIL_PASSWORD']='Shankey##1234'
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USE_TLS'] = False
mail = Mail(app)

@app.route("/")  
def index():  
    return render_template("index.html")

def read_data():
    data = pd.read_csv("Athlete_events.csv")
    return data 

@app.route("/Data/")
def form():
    data = read_data()
    Team = list(data["Team"].unique())
    Year = list(data["Year"].unique())
    Season = list(data["Season"].unique())
    Sport = list(data["Sport"].unique())
    return render_template("form.html", Team=Team, Year=Year, Season=Season, Sport=Sport)

@app.route("/aftersubmit/", methods=['GET', 'POST'])
def aftersubmit():
    if request.method == "GET":
        return redirect(url_for("form"))
        #return render_template("form.html")
    else:
        Name = request.form.get("Name")
        Team = request.form.get("Team")
        Year = request.form.get("Year")
        Year = int(Year)
        Season = request.form.get("Season")
        Sport = request.form.get("Sport")
        data = read_data()
        temp = data.copy()
        print(Team, Year, Season, Sport)
        
        if Team:
            temp = temp[temp['Team'] == Team]
        if Year:
            temp = temp[temp['Year'] == Year]
            
        if Season:
            temp = temp[temp['Season'] == Season]
        if Sport:
            temp = temp[temp['Sport'] == Sport]
        
        return temp.to_html()


@app.route('/aftercontact', methods = ['POST'])
def aftercontact():
    db = sql.connect(host='localhost',port= 3306,user= 'root',database='olympics_contact')
    cur=db.cursor()
    name= request.form.get("Full Name")
    email = request.form.get("Email")
    Query = request.form.get("Query")
    
    
    
    cmd= f"insert into info(name,email,Query) values('{name}','{email}','{Query}')"
    cur.execute(cmd)
    db.commit()
    message = MIMEMultipart()
    message['To'] = email
    message['From'] = "jaladjhamb@gmail.com"
    message['Subject'] = "MAIL FOR CONFIRMATION"
    msg = """
            <h1 class="display-5" style="color:red">OLYMPICS</h1>
            <h2  class = "display-6 style='color:pink'>Hope you are doing well</h2>
            <p class = "lead" style='font-style:italic;color:black'>This is mail for confirmation that we have got your query and we'll revert back to you soon</p>
            
        """
    html = MIMEText(msg, "html")
    message.attach(html)
    host = "smtp.gmail.com"
    port = 465
    from_email = "jaladjhamb@gmail.com"
    password = "Shankey##1234" #os.environ.get("EMAIL_HOST_PASSWORD")
    try:
        with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) as server:
            server.login(from_email, password)
            server.sendmail(from_email, email, message.as_string())
    except Exception as e:
        return f"ERROR : {e} "
    else:
        
        return render_template("index.html",msg="data saved successfully, we will revert you back as soon as possible, we have even send you a mail on your email address for the confirmation")

    


app.run(port=80, debug=True)
