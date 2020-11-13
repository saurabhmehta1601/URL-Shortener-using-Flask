# Requirements
from flask import (Flask,render_template,request,redirect)
from flask_sqlalchemy import SQLAlchemy
from requiredfunctions import createid,isLink
import re

#Flask app initialization and connecting sqlite database 
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

db=SQLAlchemy(app)

# Cheaks whether entered link is already present in database or not
def linkPresent(link):
    record=LinkTable.query.filter_by(link=link).first()
    if(record==None):
        return False
    else:
        return True

# Table to store links and their shorten link forms
class LinkTable(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    link=db.Column(db.String(1000),unique=True,nullable=False)
    linkid=db.Column(db.String(6),unique=True,nullable=False)

# Homepage
@app.route('/',methods=["GET","POST"])
def home():
    message=''
    # When POST request is made
    if request.method=="POST":
        link=request.form["link-entry"]
        # Cheak if entered link is valid or not 
        if(isLink(link)):
            # Check if entered link is already in database or not 
            if(linkPresent(link)):
                linkid=LinkTable.query.filter_by(link=link).first().linkid
            else:
                # If link not present in database create new and add to database
                # Check whether newly created random linkid is already in database or not
                linkid=createid()
                while LinkTable.query.filter_by(linkid=linkid).first()!=None :
                    linkid=createid
                    # finally add the unique linkid to database
                db.session.add(LinkTable(link=link,linkid=linkid))
                db.session.commit()
                
            message="Your shorten link is "+linkid
        else:
            message="Please enter a valid link"
    # Simply return homepage if GET request is made
    return render_template('index.html',message=message)

# Redirect to link corresponding to the entered linkid
@app.route('/<linkid>')
def redir(linkid):
    redirLink=LinkTable.query.filter_by(linkid=linkid).first()
    link=redirLink.link
    return redirect(link)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)