from flask import Flask, render_template, request, jsonify, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
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
ma = Marshmallow(app)

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

class studentsSchema(ma.Schema):
    class Meta:
        # Fields to expose	
        fields = ('id','name', 'city', 'addr', 'pin', 'img_path')

student_schema = studentsSchema() #for one student
students_schema = studentsSchema(many=True) # for all students

temp = {"id": "-1", "name": "", "city": "", "addr": "", "pin": "", "img_path": ""}

@app.route("/")
def show_all():
	return render_template('AJAX_form.html', resArr = temp)

# endpoint to show all users
@app.route("/get", methods=["GET"])
def get_user():
    all_users = students.query.all()
    result = students_schema.dump(all_users)
    return jsonify(result.data)

# endpoint to get user detail by id
@app.route("/get/<id>", methods=["GET"])
def user_detail(id):
    user = students.query.get(id)
    return student_schema.jsonify(user)

@app.route("/new", methods = ['GET', 'POST'])
def new():
	
	if request.method == 'POST':

		if request.form['id'] == '-1':
			
			if not request.form['name'] or not request.form['city'] or not request.form['addr'] or not request.form['pin']:
				return jsonify({"error":"Missing Data!"})

			else: 
				student = students(request.form['name'], request.form['city'], request.form['addr'],
                                           request.form['pin'], "NULL")
				db.session.add(student)
				db.session.commit()
				return jsonify({"message":"Record created!"})

			# return jsonify({"message":"success"})


@app.route("/delete/<who>", methods = ['GET'])
def delete(who):

        # x = students.query.filter_by(id=who)
        # remove_img = x['img_path' == who].img_path

        # deleting image
        # if remove_img in os.listdir(UPLOAD_FOLDER):
            # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], remove_img))
    try:
        students.query.filter_by(id=who).delete()
        db.session.commit()
        return jsonify({'message':'Deletion Successfull'})
    except:
    	return jsonify({'error':'Deletion Error'})    

if __name__ == '__main__':
	app.run(debug=True)




