from flask import Flask, redirect, url_for
app = Flask(__name__)

def insert_data(name, password):
    
    hostname = "localhost"
    username = "root"
    password = "MySqlp@ssw0rd"
    database = "test"

    db = MySQLdb.connect(hostname, username, password, database)
    cursor = db.cursor()
    
    sql = "INSERT INTO login(name, password) VALUES('{0}','{1}')".format(name, password)
      
    try:
        cursor.execute(sql)
        db.commit()
        print(")
    except:
        db.rollback()
        
        
        

@app.route('/login', methods = ['POST','GET'])
def login():
    print("Hello and Welcome!!")
    
    if request.method == 'POST':
        print("Method is POST")
        name = request.form['nm']
        password = request.form['pw']
        
        insert_data(name, password)
      
    else:
        print("Method is GET")
        user = request.args.get('nm')
        password = request.args.get('pw')
        
        insert_data(name, password)
    
