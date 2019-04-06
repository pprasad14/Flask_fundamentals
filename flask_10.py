from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
    return render_template("student_10.html")

@app.route('/result', methods = ['POST','GET'])
def result():
#    return "test"
    if request.method == 'POST':
        results = request.form
        return render_template('result_10.html', results = results)

if __name__ == '__main__':
    app.run()
