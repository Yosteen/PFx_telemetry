from app import app
from flask import request,render_template
from flask_pymongo import PyMongo
import os, urllib3,requests,json,time
from datetime import datetime
from app.classes import Vcclass



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/citi"
mongo = PyMongo(app)


@app.route('/vc/home', methods=['GET','POST'])
def vchome():
    if request.method == 'GET':
        return render_template('vchome.html')
    else:
        ip = request.form['ip']
        uname = request.form['uname']
        password = request.form['pass']
        svmuname = request.form['svmuname']
        svmpass = request.form['svmpass']
        vc = Vcclass(ip,uname,password,svmuname,svmpass)
        vmks = vc.vmks()
        svm_mtus = vc.getsiovms()
        return render_template ('vcresults.html', vmks= vmks, svm_mtus=svm_mtus)
