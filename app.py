from flask import (
    Flask,
    render_template,
    request
)
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///db.sqlite'

db=SQLAlchemy(app)

class LINKS(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    link=db.Column(db.String(1000))
    idlink=db.Column(db.String(6),unique=True)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shorten',methods=['POST'])
def shorten():
    links=request.form['link']
    return  render_template('shorten.html')








if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    