from flask import Flask, render_template
app = Flask(__name__)

@app.route('/result')
def display():
    dict_ = {'phy':50, 'che':60, 'mat':70}
    return render_template('result_8.html', result = dict_)

if __name__ == '__main__':
    app.run()