from flask import Flask, redirect, url_for, flash, render_template, request
app = Flask(__name__)
app.secret_key = "some text"

@app.route('/')
def index():
    return render_template('index_13.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = "Invalid username or password!!"
        
        else:
            flash("You are successfully logged in!")
            return redirect(url_for('index'))
    
    return render_template('login_13.html', error = error)

if __name__ == '__main__':
    app.run()