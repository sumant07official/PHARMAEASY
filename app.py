import pandas as pd
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, session, flash
import mysql.connector
import warnings
import  re
import os
from datetime import date
import datetime
from datetime import timedelta, date
from PIL import Image
import smtplib
from email.message import Message
from email.mime.text import MIMEText
import diseaseprediction
from utils import *
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
app.secret_key = 'your secret key'

#database connection
mydb = mysql.connector.connect(
  host="localhost",
  port=3306,
  user="root",
  password="",
  database='disease_pharmacist_management'
)
print(mydb)
mycursor = mydb.cursor()

#create table function:
#create_tables(mycursor)

mycursor = mydb.cursor(dictionary=True)

#flask code

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'pass' in request.form:
        username = request.form['username']
        password = request.form['pass']
        sql="SELECT * FROM User_Master WHERE username = %s AND password = %s"
        mycursor.execute(sql,(username, password, ))
        userdata = mycursor.fetchone()
        if userdata:
            session['loggedin'] = True
            session['u_id'] = userdata['u_id']
            session['username'] = userdata['username']
            user_name = session['username']
            return redirect(url_for('index'))
            return render_template('index.html', user_name = user_name)
        else:
            msg = 'Incorrect username / password !'
        
    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('u_id', None)
    session.pop('username', None)
    return redirect(url_for('signin'))


@app.route('/signup')
def signup():
    return redirect(url_for('register'))


@app.route('/signin')
def signin():
    return redirect(url_for('login'))



@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'pass' in request.form and 'emailid' in request.form and 'fullname' in request.form and 'mobileno' in request.form :
        username = request.form['username']
        password = request.form['pass']
        emailid = request.form['emailid']
        fullname = request.form['fullname']
        mobileno = request.form['mobileno']
        mycursor = mydb.cursor(dictionary=True)
        sql="SELECT * FROM user_master WHERE username = %s OR emailid = %s "
        mycursor.execute(sql, (username, emailid, ))
        userdata = mycursor.fetchone()
        if userdata:
            msg = 'User already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailid):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not emailid or not fullname or not mobileno:
            msg = 'Please fill out the details properly !'
        else:
            sql="INSERT INTO User_Master VALUES (NULL, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, (username, fullname, mobileno, emailid, password, ))
            mydb.commit()
            msg = 'You have successfully registered !'

    elif request.method == 'POST':
        msg = 'Please fill out the details !'
    return render_template('registration.html', msg = msg)


@app.route('/index', methods =['GET'])
def index(): 
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_name = session['username']
        return render_template('index.html',user_name = user_name)


@app.route('/diseasepredictorpage', methods =['GET'])
def diseasepredictorpage(): 
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_name = session['username']
        sql="SELECT * FROM Symptom_Master"
        mycursor.execute(sql,)
        symptomdb = mycursor.fetchall()
        return render_template('disease.html',user_name = user_name,symptomdb=symptomdb,pred_disease1=0)


@app.route('/diseasepredictor', methods =['POST'])
def diseasepredictor():

    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_name = session['username']
        todaydate = str(date.today())
        sql="SELECT * FROM Symptom_Master"
        mycursor.execute(sql,)
        symptomdb = mycursor.fetchall()
        if request.method == 'POST':
            Symptom1 = request.form['inputsymptom1']
            Symptom2 = request.form['inputsymptom2']
            Symptom3 = request.form['inputsymptom3']
            Symptom4 = request.form['inputsymptom4']
            Symptom5 = request.form['inputsymptom5']
            selected_symptoms = None
            selected_symptoms = [Symptom1,Symptom2,Symptom3,Symptom4,Symptom5]
            pred_dis = diseaseprediction.dosomething(selected_symptoms)
            print(str(pred_dis[0]))
            pred_disease = "Predicted Disease: " + str(pred_dis[0])
            sql="SELECT d_id FROM `disease_master` WHERE disease_name = %s"
            mycursor.execute(sql, (str(pred_dis[0]),))
            diseasedb = mycursor.fetchone()
            dis_id = diseasedb['d_id']
            sql="SELECT m_id,d_id,medicine_name,medicine_description,img_path,medicine_price,expiry_date,DATEDIFF(expiry_date,%s) AS date_diff FROM medicine_master WHERE d_id = %s"
            mycursor.execute(sql, (todaydate,dis_id,))
            med_db = mycursor.fetchall()
            return render_template('disease.html',user_name = user_name,symptomdb=symptomdb, pred_disease=pred_disease, med_db=med_db)


@app.route('/viewmedicine', methods =['GET'])
def viewmedicine(): 
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_name = session['username']
        todaydate = str(date.today())
        #count
        sql="SELECT ROUND(COUNT(*)/2) as row_count FROM `medicine_master`"
        mycursor.execute(sql,)
        count_db = mycursor.fetchone()
        rowcnt = count_db['row_count']
        #first half medicine
        sql="SELECT m_id,d_id,medicine_name,medicine_description,img_path,medicine_price,expiry_date,DATEDIFF(expiry_date,%s) AS date_diff FROM medicine_master LIMIT %s"
        mycursor.execute(sql,(todaydate,rowcnt,))
        allmed_db1 = mycursor.fetchall()
        #secoond half medicine
        sql="SELECT m_id,d_id,medicine_name,medicine_description,img_path,medicine_price,expiry_date,DATEDIFF(expiry_date,%s) AS date_diff FROM medicine_master LIMIT %s OFFSET %s"
        mycursor.execute(sql,(todaydate,rowcnt,rowcnt, ))
        allmed_db2 = mycursor.fetchall()
        return render_template('medicine.html',user_name = user_name,allmed_db1=allmed_db1,allmed_db2=allmed_db2)


@app.route('/buymedicine', methods =['POST'])
def buymedicine():
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_name = session['username']
        user_id = session['u_id']
        if request.method == 'POST' and 'mId' in request.form:
            med_id = request.form['mId']
            datediff = request.form['datediff']
            sql="SELECT * FROM `medicine_master` WHERE m_id = %s"
            mycursor.execute(sql,(med_id, ))
            meddetail_db = mycursor.fetchone()
            if int(datediff) <= 30:
                med_price = int(int(meddetail_db['medicine_price']) * 0.75)
            else:
                med_price = meddetail_db['medicine_price']
        
        return render_template('buymedicine.html',user_name = user_name,meddetail_db=meddetail_db,med_price=med_price)


@app.route('/checkout', methods =['POST'])
def checkout():
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_name = session['username']
        user_id = session['u_id']
        if request.method == 'POST' and 'mId' in request.form:
            med_id = request.form['mId']
            inputquan = request.form['inputquan']
            inputadd = request.form['inputadd']
            medprice = request.form['medprice']
            total_amount = int(int(medprice) * int(inputquan))
        return render_template('payment.html',user_name = user_name,med_id=med_id,inputquan=inputquan,inputadd=inputadd,total_amount=total_amount)


@app.route('/orderpayment', methods =['POST'])
def orderpayment():
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_name = session['username']
        user_id = session['u_id']
        if request.method == 'POST' and 'med_id' in request.form:
            med_id = request.form['med_id']
            inputquan = request.form['inputquan']
            inputadd = request.form['inputadd']
            totalamount = request.form['total_amount']
            todaydt =  str(date.today())
            orderstatus = 'pending'
            sql="INSERT INTO order_transaction VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, (user_id,med_id,todaydt,inputquan,totalamount,orderstatus,inputadd, ))
            mydb.commit()
            #sendmail
            sql="SELECT * FROM `user_master` WHERE u_id = %s"
            mycursor.execute(sql,(user_id, ))
            user_detail_db = mycursor.fetchone()
            emailid = user_detail_db['emailid']
            subject = "Order Confirmation"
            textmsg = "Thank you for your recent order at [PharmaEasy]. Your order is currently being processed and will be shipped within 2-3 business days."
            send_email(textmsg,subject,emailid)

        return redirect(url_for('orderhistpage'))


@app.route('/orderhistpage', methods =['GET'])
def orderhistpage():
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_id = session['u_id']
        user_name = session['username']
        sql="SELECT * FROM `order_transaction` LEFT JOIN medicine_master ON medicine_master.m_id = order_transaction.medicines WHERE order_transaction.u_id = %s ORDER BY o_id DESC"
        mycursor.execute(sql,(user_id, ))
        order_db = mycursor.fetchall()
        return render_template('orderhistory.html',user_name = user_name,order_db=order_db)


@app.route('/aboutus', methods =['GET'])
def aboutus(): 
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_name = session['username']
        return render_template('about.html',user_name = user_name)


@app.route('/contactusinfopage', methods =['GET', 'POST'])
def contactusinfopage():
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_name = session['username']
        user_id = session['u_id']
        sql="SELECT * FROM User_Master WHERE u_id = %s"
        mycursor.execute(sql,(user_id, ))
        contactusdb = mycursor.fetchone()

        return render_template('contact.html',user_name = user_name, contactusdb=contactusdb)


@app.route('/contactusinfo', methods =['POST'])
def contactusinfo():
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        user_name = session['username']
        user_id = session['u_id']
        sql="SELECT * FROM User_Master WHERE u_id = %s"
        mycursor.execute(sql,(user_id, ))
        contactusdb = mycursor.fetchone()
        if request.method == 'POST':
            todaydt =  str(date.today())
            inputmedicine = request.form['inputmedicine']
            inputmssg = request.form['inputmssg']
            sql="INSERT INTO ContactUs_Transaction VALUES (NULL, %s, %s, %s, %s)"
            mycursor.execute(sql, (user_id,inputmedicine, inputmssg, todaydt, ))
            mydb.commit()

        return render_template('contact.html',user_name = user_name, contactusdb=contactusdb)


#adminpart
@app.route('/admin')
@app.route('/adminlogin', methods =['GET', 'POST'])
def adminlogin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'pass' in request.form:
        username = request.form['username']
        password = request.form['pass']
        sql="SELECT * FROM Admin_Master WHERE username = %s AND password = %s"
        mycursor.execute(sql,(username, password, ))
        admindata = mycursor.fetchone()
        if admindata:
            session['loggedin'] = True
            session['admin_id'] = admindata['admin_id']
            session['username'] = 'Admin(Medical)'
            cntlist = countfunc(mycursor)
            
            return redirect(url_for('dashboard'))
            return render_template('adminindex.html', user_name = user_name, cntlist=cntlist)
        else:
            msg = 'Incorrect username / password !'
    return render_template('admin/adminlogin.html', msg = msg)


@app.route('/adminlogout')
def adminlogout():
    session.pop('loggedin', None)
    session.pop('admin_id', None)
    session.pop('username', None)
    return redirect(url_for('adminlogin'))


@app.route('/dashboard', methods =['GET', 'POST'])
def dashboard(): 
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        cntlist = countfunc(mycursor)
        return render_template('admin/adminindex.html',user_name = user_name, cntlist = cntlist)


@app.route('/exploreusers', methods =['GET'])
def exploreusers():
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        sql="SELECT * FROM `user_master` ORDER BY u_id ASC"
        mycursor.execute(sql,)
        userdatabase = mycursor.fetchall()

        return render_template('admin/exploreuser.html',user_name = user_name, userdatabase=userdatabase)


@app.route('/exploremedicine', methods =['GET','POST'])
def exploremedicine():
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        sql="SELECT m_id,disease_master.disease_name,medicine_name,medicine_description,medicine_price,expiry_date,img_path FROM `medicine_master` LEFT JOIN disease_master ON disease_master.d_id = medicine_master.d_id ORDER BY m_id ASC"
        mycursor.execute(sql,)
        medicine_db = mycursor.fetchall()

        sql="SELECT medicines FROM order_transaction"
        mycursor.execute(sql,)
        medicineid_db = mycursor.fetchall()
        medid_list = []
        for item in medicineid_db:
            medid_list.append(int(item['medicines']))

        return render_template('admin/exploremedicine.html',user_name = user_name, medicine_db=medicine_db,medicineid_db=medid_list)


@app.route('/updatemedicinepage', methods=['POST'])
def updatemedicinepage():
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        if request.method == 'POST' and 'm_id' in request.form:
            m_id = request.form['m_id']
            sql="SELECT * FROM `medicine_master` LEFT JOIN disease_master on disease_master.d_id = medicine_master.d_id WHERE m_id = %s"
            mycursor.execute(sql,(m_id,))
            updatemed_db = mycursor.fetchone()
            sql="SELECT * FROM `disease_master`"
            mycursor.execute(sql,)
            diseasedb = mycursor.fetchall()
            min_date = str(date.today() + timedelta(days=1))
        return render_template('admin/updatemedicine.html',user_name = user_name, updatemed_db=updatemed_db,diseasedb=diseasedb,mindate=min_date)


@app.route('/updatemedicine', methods=['POST'])
def updatemedicine():
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        if request.method == 'POST' and 'm_id' in request.form and 'inputfile' in request.files:
            file = None
            file = request.files['inputfile']
            if file and allowed_file(file.filename) and file.filename not in os.listdir('./static/images/medicine_img/'):
                oldimgpath = request.form['oldimgpath']
                os.remove(os.path.join('./static/images/medicine_img/',oldimgpath))
                imgname = str(file.filename)
                image = Image.open(file)
                newsize = (250, 250)
                image = image.resize(newsize)
                image.save(os.path.join('./static/images/medicine_img/',imgname))
                m_id = request.form['m_id']
                file = request.files['inputfile']
                inputmedname = request.form['inputmedname']
                inputmedprice = request.form['inputmedprice']
                inputdiseaseid = request.form['diseaseid']
                inputmeddesc = request.form['inputmeddesc']
                inputexpdate = request.form['expdate']
                sql="UPDATE medicine_master SET d_id = %s,medicine_name = %s,medicine_description = %s,img_path = %s,expiry_date = %s,medicine_price = %s WHERE m_id = %s"
                mycursor.execute(sql, (inputdiseaseid,inputmedname,inputmeddesc,imgname,inputexpdate,inputmedprice,int(m_id), ))
                mydb.commit()

        elif request.method == 'POST' and 'm_id' in request.form:
            m_id = request.form['m_id']
            file = request.files['inputfile']
            inputmedname = request.form['inputmedname']
            inputmedprice = request.form['inputmedprice']
            inputdiseaseid = request.form['diseaseid']
            inputmeddesc = request.form['inputmeddesc']
            inputexpdate = request.form['expdate']
            sql="UPDATE medicine_master SET d_id = %s,medicine_name = %s,medicine_description = %s,expiry_date = %s,medicine_price = %s WHERE m_id = %s"
            mycursor.execute(sql, (inputdiseaseid,inputmedname,inputmeddesc,inputexpdate,inputmedprice,int(m_id), ))
            mydb.commit()

        return redirect(url_for('exploremedicine'))


@app.route('/deletemedicine', methods=['POST'])
def deletemedicine():
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        if request.method == 'POST' and 'm_id' in request.form:
            m_id = request.form['m_id']
            sql="DELETE FROM medicine_master WHERE m_id = %s"
            mycursor.execute(sql, (m_id,))
            mydb.commit()

        return redirect(url_for('exploremedicine'))


@app.route('/explorecorder', methods =['GET'])
def explorecorder():
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        sql="SELECT * FROM (SELECT * FROM `order_transaction` LEFT JOIN medicine_master ON medicine_master.m_id = order_transaction.medicines WHERE order_status = 'completed' ORDER BY o_id DESC) AS a LEFT JOIN user_master ON user_master.u_id = a.u_id"
        mycursor.execute(sql,)
        orderc_db = mycursor.fetchall()

        return render_template('admin/explorecorders.html',user_name = user_name, orderc_db=orderc_db)


@app.route('/exploreporder', methods =['GET','POST'])
def exploreporder():
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        sql="SELECT * FROM (SELECT * FROM `order_transaction` LEFT JOIN medicine_master ON medicine_master.m_id = order_transaction.medicines  WHERE order_status = 'pending' ORDER BY o_id ASC) AS a LEFT JOIN user_master ON user_master.u_id = a.u_id"
        mycursor.execute(sql,)
        orderp_db = mycursor.fetchall()

        return render_template('admin/exploreporders.html',user_name = user_name, orderp_db=orderp_db)


@app.route('/statusupdate', methods=['POST'])
def statusupdate():
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        if request.method == 'POST' and 'o_id' in request.form:
            o_id = request.form['o_id']
            sql="UPDATE `order_transaction` SET order_status = 'completed' WHERE o_id = %s"
            mycursor.execute(sql, (o_id,))
            mydb.commit()

        return redirect(url_for('explorecorder'))


@app.route('/addmedicine', methods =['GET', 'POST'])
def addmedicine():
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        sql="SELECT * FROM `disease_master`"
        mycursor.execute(sql,)
        diseasedb = mycursor.fetchall()
        min_date = str(date.today() + timedelta(days=1))
        return render_template('admin/addmedicine.html',user_name = user_name, diseasedb=diseasedb,mindate=min_date)


ALLOWED_EXTENSIONS = {'jpg','png'}
def allowed_file(filename):
  return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/addmedicineform', methods =['POST'])
def addmedicineform(): 
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        try:
            user_name = session['username']
            if request.method == 'POST':
                file = None
                file = request.files['inputfile']
                if file and allowed_file(file.filename) and file.filename not in os.listdir('./static/images/medicine_img/'):
                    imgname = str(file.filename)
                    image = Image.open(file)
                    newsize = (250, 250)
                    image = image.resize(newsize)
                    image.save(os.path.join('./static/images/medicine_img/',imgname))
                    inputmedname = request.form['inputmedname']
                    inputmedprice = request.form['inputmedprice']
                    inputdiseaseid = request.form['diseaseid']
                    inputmeddesc = request.form['inputmeddesc']
                    inputexpdate = request.form['expdate']
                    sql="INSERT INTO medicine_master VALUES (NULL, %s, %s, %s, %s, %s,%s)"
                    mycursor.execute(sql, (inputdiseaseid, inputmedname, inputmeddesc,imgname, inputmedprice, inputexpdate, ))
                    mydb.commit()
                    successmssg = 'Medicine Added Successfully'
                else:
                    successmssg = 'Same File Name Already Present in System'

            return render_template('admin/addmedicine.html',user_name = user_name, successmssg=successmssg)
            return redirect(url_for('addmedicine'))
            
        except Exception as e:
            successmssg = 'Medicine Not Added Successfully'
            return render_template('admin/addmedicine.html',user_name = user_name, successmssg=successmssg)
            return redirect(url_for('addmedicine'))


@app.route('/explorecallback', methods =['GET'])
def explorecallback():
    if 'username' not in session.keys():
        return redirect(url_for('adminlogin'))
    else:
        user_name = session['username']
        sql="SELECT contactus_transaction.cu_id,user_master.fullname,user_master.mobileno,user_master.emailid,medicine_name,message,cu_date FROM `contactus_transaction` LEFT JOIN user_master ON user_master.u_id = contactus_transaction.u_id ORDER BY cu_id ASC"
        mycursor.execute(sql,)
        callback_db = mycursor.fetchall()

        return render_template('admin/explorecallback.html',user_name = user_name, callback_db=callback_db)



if __name__ == '__main__':
    # Run the application
    app.run(debug=False)

