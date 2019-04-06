from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:MySqlp@ssw0rd@localhost/test'
app.config['SECRET_KEY'] = "random string"

UPLOAD_FOLDER = r'C:\x\Docs\python\Cumulations_practice\python-virtual-environments\Vir\static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    img_path = db.Column(db.String(150))

    def __init__(self, name, city, addr, pin, pic_path="NULL"):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin
        self.img_path = pic_path

temp = {"id": "-1", "name": "", "city": "", "addr": "", "pin": "", "img_path": ""}

def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def show_all():
    return render_template('show_all_14_new.html', students=students.query.all(), resArr=temp, path=UPLOAD_FOLDER)

@app.route('/', methods = ['POST', 'GET'])
def new():
    if request.method == 'POST':
        # if new data is entered
        if request.form['id'] == "-1":

            if not request.form['name'] or not request.form['city'] or not request.form['addr'] or not request.form['pin']:
                #            return "no"
                flash("Please enter all fields", 'error')
                return render_template("show_all_14_new.html", students = students.query.all(), resArr = temp, path = UPLOAD_FOLDER)
            else:
                #            return "ys"
                try:
                    file_name = request.files['img']

                    if file_name and allowed_file(file_name.filename):
                        file_n = secure_filename(file_name.filename)
                        file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], file_n))

                        student = students(request.form['name'], request.form['city'], request.form['addr'],
                                           request.form['pin'], file_n)
                        #                              str(UPLOAD_FOLDER.split("\\")[-1]+'/'+
                        #            return "yes"
                        db.session.add(student)
                        db.session.commit()
                        flash("Image and Data stored successfully!")
                except:
                    student = students(request.form['name'], request.form['city'], request.form['addr'],
                                       request.form['pin'], "NULL")
                    db.session.add(student)
                    db.session.commit()

                    flash("No image uploaded!")

                flash("Record was successfully added")

        # if old data needs to be altered, ie "edit"
        else:
            # return request.form['id']
            if request.method in ['POST', 'GET']:

                id_ = request.form['id']
                nm = request.form['name']
                cy = request.form['city']
                ad = request.form['addr']
                pn = request.form['pin']
                #        try:
                #            request.files['img']
                #            return "yes"
                #        except:
                #            return "no"
                if not request.form['name'] or not request.form['city'] or not request.form['addr'] or not request.form['pin']:

                    flash("Please enter all fields", 'error')
                    return render_template("show_all_14_new.html", resArr=temp)

                try:

                    new_image = request.files['img']

                    filename_new = secure_filename(new_image.filename)

                    if new_image and allowed_file(filename_new):

                        x = students.query.filter_by(id=id_)

                        # get image name from database to remove
                        remove_img = x['img_path' == id_].img_path

                        # deleting image
                        if remove_img != "NULL":
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], remove_img))

                        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_new))

                        stmt = "UPDATE students SET name = '{}', city = '{}', addr = '{}',\
                               pin = '{}', img_path = '{}' WHERE student_id = {};".format(nm, cy, ad, pn, filename_new,
                                                                                          id_)
                        db.engine.execute(text(stmt))
                        db.session.commit()
                    flash("Image Uploaded!")

                except:
                    filename_old = request.form['img_']
                    stmt = "UPDATE students SET name = '{}', city = '{}', addr = '{}',\
                                pin = '{}', img_path = '{}' WHERE student_id = {};".format(nm, cy, ad, pn, filename_old,
                                                                                           id_)

                    db.engine.execute(text(stmt))
                    db.session.commit()

                    flash("Old Image Used!  ")
                flash("  Record has been successfully changed!")

    return render_template("show_all_14_new.html", students = students.query.all(), resArr = temp, path = UPLOAD_FOLDER)
#    return redirect(url_for('new'))
#    return render_template('new_14.html')

@app.route('/edit/<who>', methods = ['POST', 'GET'])
def edit(who):

    if request.method in ['POST', 'GET']:

        temp_val = students.query.filter_by(id = who)

        return render_template("show_all_14_new.html", resArr = temp_val['id' == who], students = students.query.all(), path = UPLOAD_FOLDER)

@app.route('/delete/<who>', methods = ['POST', 'GET'])
def delete(who):
    if request.method in ['POST', 'GET']:

        x = students.query.filter_by(id=who)
        remove_img = x['img_path' == who].img_path

        # deleting image
        if remove_img in os.listdir(UPLOAD_FOLDER):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], remove_img))

        students.query.filter_by(id=who).delete()
        db.session.commit()
        flash("Deletion successfull!")
        return render_template("show_all_14_new.html", students=students.query.all(), resArr = temp)

if __name__ == "__main__":
    db.create_all()
    app.run()
