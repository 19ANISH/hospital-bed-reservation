from flask import Flask, json, redirect, render_template, flash, request
from flask.globals import request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_required, logout_user, login_user, login_manager, LoginManager, current_user

from flask_mail import Mail
import json


# local server connection
local_server = True
app = Flask(__name__)
app.secret_key = "1907"

# opening the json file
# in read mode
with open('config.json', 'r') as c:
    params = json.load(c)["params"]


# setting mail for admin to authenticate the hospital and sent them the permit
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['admin-email'],
    MAIL_PASSWORD=params['admin-password']
)
mail = Mail(app)


# login manager to check the login sessions and logout sessions
# gives unique user access
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# SQL database Xamp Server connection
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://username:password@localhost/databaseName"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/test'
db = SQLAlchemy(app)

# syntax from internet


@login_manager.user_loader
def load_user(user_id):
    return Hospitaluser.query.get(int(user_id))


# Coloring the console logs
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# db for testing
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

# creating class for hospitaluser which is to added by the admin


class Hospitaluser(UserMixin, db.Model):
    def get_id(self):
        return (self.id)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    # hospital code is HosCode
    HosCode = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    # password can be same for 2 hospitals

# database for storing hospital data in database


class Hospitaldata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    HosCode = db.Column(db.String(100), unique=True)
    HosName = db.Column(db.String(200))
    normalbed = db.Column(db.Integer)
    icubed = db.Column(db.Integer)
    ventbed = db.Column(db.Integer)

# database to store data of the beds booked by the patient


class Bookingbed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(20),unique=True)
    email = db.Column(db.String(100), unique=True)
    bedtype = db.Column(db.String(50))
    HosCode = db.Column(db.String(100))
    # many people can book in same hospital
    medicalhistory = db.Column(db.String(10))
    pname = db.Column(db.String(100))
    pphone = db.Column(db.String(12))
    paddress = db.Column(db.String(100))
    page = db.Column(db.Integer)


class Triger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    HosCode = db.Column(db.String(100))
    normalbed = db.Column(db.Integer)
    icubed = db.Column(db.Integer)
    ventbed = db.Column(db.Integer)
    querys = db.Column(db.String(50))
    date = db.Column(db.String(50))

# index page


@app.route("/")
def home():
    return render_template('index.html')

# login for hospital with these routes


@app.route('/hospitalLogin', methods=['POST', 'GET'])
def hospitalLogin():
    if request.method == 'POST':
        HosCode = request.form.get('HosCode')
        password = request.form.get('password')
        hospital_user = Hospitaluser.query.filter_by(HosCode=HosCode).first()
        if hospital_user and check_password_hash(hospital_user.password, password):
            # login_user(hospital_user,remember=False)
            login_user(hospital_user)
            flash("Login Success", "info")
            return render_template("index.html")
            # return "Success"
        else:
            flash("Invalid Credentials", "danger")
            # it will redirect us to this page
            return render_template("hospitalLogin.html")
            # return "Fail"
    return render_template("hospitalLogin.html")


# admin login check and routes
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if(username == params['user'] and password == params['password']):
            session['user'] = username
            flash("Admin Logged In", 'success')
            return render_template("addHospitalUser.html")
            # return "Logged In"
        else:
            flash("Invalid Credentials", "warning")

    return render_template("admin.html")


# log-out admin
@app.route('/logoutadmin')
def logoutadmin():
    session.pop('user')
    flash('Logged-Out Successfully', 'success')
    # return redirect(url_for('admin'))
    return redirect(url_for('home'))


# creating a route to add the details of hospital
# only admin is allowed to give access to add the hospital
# hospital data i.e. avaiblity of bed is a different function and route
@app.route('/addHospitalUser', methods=['POST', 'GET'])
def hospitalUser():
    # only when admin is logged in the following conditions will work
    if('user' in session and session['user'] == params['user']):
        if request.method == "POST":
            email = request.form.get('email')
            HosCode = request.form.get('HosCode')
            password = request.form.get('password')
            encpassword = generate_password_hash(password)
            HosCode = HosCode.upper()
            emailUser = Hospitaluser.query.filter_by(email=email).first()
            #user_HosCode = HospitalUser.query.filter_by(HosCode=HosCode).first()
            if emailUser:
                flash("Email or Hospital Code is already taken", "warning")
                # return render_template("admin.html")
            db.engine.execute(
                f"INSERT INTO `hospitaluser` (`email`,`HosCode`,`password`) VALUES ('{email}','{HosCode}','{encpassword}') ")
            # sending the mail in which there are details to the hospital user
            mail.send_message("Welcome", sender=params['admin-email'], recipients=[
                              email], body=f"Thanks for registering on our site\nFollowing are your unique credentials\nEmail Address:- {email}\nHospital Code:- {HosCode}\nPassword:- {password}\n\nDon't share your password with anyone\n\n\t\tThank You")

            flash("Mail Sent and Data Inserted", "success")
            return render_template("addHospitalUser.html")
    else:
        flash("Login and TryAgain", "warning")
        return redirect(url_for('admin'))

# @login_manager.user_loader
# def load_hospital(hospital_id):
#     return Hospitaluser.query.get(int(hospital_id))


# route to enter hospital data
@login_required
@app.route("/addHospitalInfo", methods=['POST', 'GET'])
def addHospitalInfo():
    # we check if the hospital code exists or not in the database
    # hc = current_user.HosCode
    try:
        email = current_user.email
    except:
        return render_template("hospitalLogin.html")
    # print(email)
    posts = Hospitaluser.query.filter_by(email=email).first()
    code = posts.HosCode
    # print(code)
    postsdata = Hospitaldata.query.filter_by(HosCode=code).first()
    # print(bcolors.OKCYAN, postsdata.HosName, bcolors.ENDC)
    if request.method == "POST":
        HosCode = request.form.get('HosCode')
        HosName = request.form.get('HosName')
        normalbed = request.form.get('normalbed')
        icubed = request.form.get('icubed')
        ventbed = request.form.get('ventbed')
        HosCode = HosCode.upper()
        # print(postsdata.HosName)
        # if the hospital code is registered then only info can be added
        huser = Hospitaluser.query.filter_by(HosCode=HosCode).first()
        # if the hospital has perviously entered data then can or we should update the info
        hduser = Hospitaldata.query.filter_by(HosCode=HosCode).first()
        if hduser:
            flash("Data is already present you can update it", "primary")
            return render_template('hospitalData.html')
        if huser:
            db.engine.execute(
                f"INSERT INTO `hospitaldata` (`HosCode`,`HosName`,`normalbed`,`icubed`,`ventbed`) VALUES ('{HosCode}','{HosName}','{normalbed}','{icubed}','{ventbed}')")
            flash("Data Inserted Successfully", 'success')
        else:
            flash("Hospital Code Not Registered", 'warning')

    # return "success"
    return render_template('hospitalData.html', postsdata=postsdata)

# editing or updating the hospital data which previously exists in the database


@app.route("/hedit/<string:id>", methods=['POST', 'GET'])
@login_required
# hedit is hospital edit
def hedit(id):
    posts = Hospitaldata.query.filter_by(id=id).first()

    if request.method == 'POST':
        HosCode = request.form.get('HosCode')
        HosName = request.form.get('HosName')
        normalbed = request.form.get('normalbed')
        icubed = request.form.get('icubed')
        ventbed = request.form.get('ventbed')
        # HosCode = HosCode.upper()
        db.engine.execute(
            f"UPDATE `hospitaldata` SET `HosCode` = '{HosCode}', `HosName` = '{HosName}', `normalbed` = '{normalbed}', `icubed` = '{icubed}', `ventbed` = '{ventbed}' WHERE `hospitaldata`.`id`={id}")
        flash("Data Updated", "success")
        # return render_template("hospitalData.html")
        # return redirect("/")
        return redirect("/addHospitalInfo")
    # posts=Hospitaldata.query.filter_by(id=id).first()
    return render_template("hedit.html", posts=posts)


# deleting the data
@app.route("/hdelete/<string:id>", methods=['POST', 'GET'])
@login_required
def hdelete(id):
    db.engine.execute(
        f"DELETE  FROM `hospitaldata` WHERE `hospitaldata`.`id` = '{id}'")
    # db.engine.execute(f"DELETE  FROM `hospitaldata` WHERE `hospitaldata`.`id` = 'None'")
    flash("Data Deleted Successfully", 'warning')
    return redirect('/addHospitalInfo')

# hospital logout route


@app.route("/hospitalLogout")
@login_required
# without login you cannot logout
def hospital_logout():
    logout_user()
    flash("Logged Out Successfully", 'success')
    return render_template("index.html")

# route to book bed


@app.route('/bedbooking', methods=['POST', 'GET'])
def bedbooking():
    # return "bed"
    query = db.engine.execute(f"SELECT * FROM `hospitaldata`")
    if request.method == 'POST':
        email = request.form.get('email')
        HosCode = request.form.get('HosCode')
        bedtype = request.form.get('bedtype')
        medicalhistory = request.form.get('medicalhistory')
        pname = request.form.get('pname')
        pphone = request.form.get('pphone')
        paddress = request.form.get('paddress')
        page = request.form.get('page')
        check = Hospitaldata.query.filter_by(HosCode=HosCode).first()
        if not check:
            flash("Hospital Code Doesn't Exists", "warning")
            # we use hoscode as it is unique so we can identify the hospital from all the data available
        code = HosCode
        dbb = db.engine.execute(
            f"SELECT * FROM `hospitaldata` WHERE `hospitaldata`.`HosCode` = '{code}'")
        # selecting which bedtype is required to user
        bedtype = bedtype
        if bedtype == "NormalBed":
            for d in dbb:
                seat = d.normalbed
                # print(seat)
                ar = Hospitaldata.query.filter_by(HosCode=HosCode).first()
                ar.normalbed = seat - 1
                db.session.commit()
        elif bedtype == "IcuBed":
            for d in dbb:
                seat = d.icubed
                # print(seat)
                ar = Hospitaldata.query.filter_by(HosCode=HosCode).first()
                ar.icubed = seat - 1
                db.session.commit()

        elif bedtype == "VentBed":
            for d in dbb:
                seat = d.ventbed
                # print(seat)
                ar = Hospitaldata.query.filter_by(HosCode=HosCode).first()
                ar.ventbed = seat - 1
                db.session.commit()
        else:
            pass
        check2 = Hospitaldata.query.filter_by(HosCode=HosCode).first()
        # dbe = db.engine.execute(f"SELECT `email` FROM `hospitaluser` WHERE `hospitaluser`.`HosCode` = '{code}'")
        # print(dbe)
        if (seat > 0 and check2):
            res = Bookingbed(email=email, bedtype=bedtype, HosCode=HosCode, medicalhistory=medicalhistory, pname=pname,
                             pphone=pphone, paddress=paddress, page=page)
            db.session.add(res)
            db.session.commit()
            mail.send_message("Welcome", sender=params['admin-email'], recipients=[email],
                              body=f"Thanks for booking\nDetails\nEmail Address used:- {email}\nHospital Code:- {HosCode}\nBed Type:- {bedtype}\nPatient Name:- {pname}\nPatient Contact:- {pphone}\n\nContact the hospital as soon as possible\n\n\t\tThank You")
            # mail.send_message("Welcome", sender=params['admin-email'], recipients=[dbe],
            #                   body=f"Thanks for booking\nDetails\nEmail Address used:- {email}\nHospital Code:- {HosCode}\nBed Type:- {bedtype}\nPatient Name:- {pname}\nPatient Contact:- {pphone}\n\nContact the hospital as soon as possible\n\n\t\tThank You")

            flash("Bed Booked, Contact Hospital for further details", "success")
        else:
            flash("Something went wrong, TRY AGAIN", "danger")

    return render_template("booking.html", query=query)

# triger routes


@app.route("/trigers")
def trigers():
    query = Triger.query.all()
    return render_template("trigers.html", query=query)


# database connection testing
@app.route("/test")
def test():
    try:
        # all the queries we get and it is stored so that we can print it and see what's required
        a = Test.query.all()
        print(a)
        return "db connected"
    except Exception as e:
        # to get the exception we return e
        return f"db not connected {e}"


if __name__ == '__main__':
    app.run(debug=True)  # to run the flask app
