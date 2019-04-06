from flask import Flask

app = Flask(__name__)

@app.route('/blog/<int:id>')
def blog_display(id):
    return "Blog Id : {}".format(id)

@app.route('/rev/<float:rev_id>')
def rev_display(rev_id):
    return "Revision Id : {}".format(rev_id)

if __name__ == "__main__":
    app.run()
