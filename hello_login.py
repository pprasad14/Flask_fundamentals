import MySQLdb

from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/success')
def success():
   return 'Added to database successfully!'

@app.route('/login',methods = ['POST', 'GET'])
def login():          
    
    hostname = "localhost"
    username = "root"
    password = "MySqlp@ssw0rd"
    database = "test"
    
    user = request.form['nm']
    pw = request.form['pw']
  
    db = MySQLdb.connect(hostname, username, password, database)
    cursor = db.cursor()
    
    sql = "INSERT INTO LOGIN(name, password) VALUES('{}','{}')".format(user, pw)
      
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    
    db.close()
         
    return redirect(url_for('success'))
   

if __name__ == '__main__':
   app.run()
   
