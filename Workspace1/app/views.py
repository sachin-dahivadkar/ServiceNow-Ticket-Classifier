from flask import Flask, make_response, request, render_template, redirect, url_for, flash, session, abort
from .forms import Loginform
from app import app
from werkzeug.security import check_password_hash, generate_password_hash
from .model import UserInfo
from flask_login import login_user, logout_user, current_user, login_required
import pandas as pd 
import numpy as np 

# ML Packages
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfTransformer



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<name>')
def user(name):
    return '<h3>welcome Mr. {}</h3>'.format(name)


@app.route('/set')
def setCookie():
    response = make_response("This is my set cookie")
    response.set_cookie("Appmy", "Test cookie app")
    return response


@app.route('/get')
def get_Cookie():
    appMy = request.cookies.get("Appmy")
    return "My cookie content is:" + appMy


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")



@app.route('/login', methods=['GET', 'POST'])
def login():

    form = Loginform()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(
                username=form.username.data).first()

            if user:

                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for('predict'))
                else:
                    flash("Invalid Credentials")
            else:
                flash("Invalid User")

    return render_template("login.html", form=form)


@app.route('/predict', methods=['GET','POST'])
@login_required
def predict():
    form=Loginform()
    predicted=''
    TC_NB_clf_model= open("D:\\Workspace1\\NB_TC_Model.pkl","rb")
    TC_NB_clf=joblib.load(TC_NB_clf_model)
    if request.method=='POST':
        namequery= request.form.get('namequery')
        data=[namequery]

        # cv= CountVectorizer()
        # cv_count=cv.fit_transform(data).toarray()

        # transformerTfid = TfidfTransformer()
        # tf_clf = transformerTfid.fit_transform(cv_count)

        predicted=TC_NB_clf.predict(data)        
    else:
        namequery= request.form.get('namequery')
    return render_template("predict.html",name=current_user.username,prediction=predicted,namequery=namequery, form=form)

 
@app.route("/logout")
@login_required
def logout():

    logout_user()
    flash("logged out successfully...")
    return redirect(url_for('login'))

""" @app("/result")
   return render_template(url_for('login'))
 """
