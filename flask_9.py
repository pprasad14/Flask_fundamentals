from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def display():
    return render_template('index_9.html')

if __name__ == '__main__':
    app.run()
    