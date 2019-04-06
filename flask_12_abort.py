from flask import Flask, redirect, url_for, render_template, request, abort
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login_12.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            return redirect(url_for('success'))
        else:
            abort(401)
            
    return redirect(url_for('index'))

@app.route('/success')
def success():
    return "Admin logged in successfully!!"

if __name__ == '__main__':
    app.run()
    