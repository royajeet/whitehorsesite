from flask import Flask, render_template, json, request ,redirect, session
#from flask.ext.mysql import MySQL
#from flask_pymongo import PyMongo
import MySQLdb , json
from werkzeug import generate_password_hash, check_password_hash

#mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'isha'

"""
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'flipkart'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
"""

u='root'
p='root'
h='localhost'

@app.route('/')
def main():
    return render_template('index.html')
    
@app.route('/showHome')
def showHome():
	return redirect ('/')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        conn=MySQLdb.connect(user=u, passwd=p, host=h, db='flipkart')
        c = conn.cursor()
        c.execute('select * from phoneDetails;')
        phonedetails = c.fetchall()
        print type(phonedetails)
        conn.close()
        return render_template('phoneDetails.html', data=phonedetails)
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def login_validate():
    try:
        _email= request.form['inputEmail']
        _password = request.form['inputPassword']
        conn=MySQLdb.connect(user=u, passwd=p, host=h, db='flipkart')
        c = conn.cursor()
        c.callproc('login_validate',(_email,))
        data=c.fetchall()
        if data[0][1] == str(_password):
            session['user'] = data[0][0]
            conn.close()
            return redirect('/userHome')
 
    except Exception as e:
        return render_template('error.html',error = str(e))




@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn=MySQLdb.connect(user=u, passwd=p, host=h, db='flipkart')
            c = conn.cursor()
            #hashed_password = generate_password_hash(_password)
            c.callproc('new_procedure',(_name,_email,_password))
            data = c.fetchall()

            if len(data) is 0:
                conn.commit()
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally: 
        conn.close()
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
