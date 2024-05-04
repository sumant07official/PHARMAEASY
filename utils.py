import pandas as pd
import numpy as np
import mysql.connector
import warnings
import  re
from datetime import date
import datetime
from datetime import timedelta, date
import smtplib
from email.message import Message
from email.mime.text import MIMEText
warnings.filterwarnings("ignore", category=UserWarning)


def countfunc(mycursor):
    sql="SELECT COUNT(*) AS 'COUNT' FROM user_master"
    mycursor.execute(sql,)
    u_count = mycursor.fetchone()
    orderstatusc = 'completed'
    sql="SELECT COUNT(*) AS 'COUNT' FROM order_transaction WHERE order_status = %s"
    mycursor.execute(sql,(orderstatusc,))
    oc_count = mycursor.fetchone()
    orderstatusp = 'pending'
    sql="SELECT COUNT(*) AS 'COUNT' FROM order_transaction WHERE order_status = %s"
    mycursor.execute(sql,(orderstatusp,))
    op_count = mycursor.fetchone()
    sql="SELECT COUNT(*) AS 'COUNT' FROM medicine_master"
    mycursor.execute(sql,)
    m_count = mycursor.fetchone()

    return [u_count['COUNT'],oc_count['COUNT'],op_count['COUNT'],m_count['COUNT']]



def send_email(textmsg,subject,emailid):
    sender = "sharduln93@gmail.com"
    username = "sharduln93@gmail.com"
    password = "xszstmzvaazgfahq"
    msg = MIMEText(str(textmsg))
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = emailid
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username, password)
    server.sendmail(sender, emailid, msg.as_string())
    server.quit()
    print("mail send successfully")
