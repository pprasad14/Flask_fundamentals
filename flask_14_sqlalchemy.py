from flask import Flask, render_template, request, flash, url_for, redirect, send_from_directory
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
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))  
   addr = db.Column(db.String(200))
   pin = db.Column(db.String(10))
   img_path = db.Column(db.String(150))
   
   def __init__(self, name, city, addr, pin, pic_path = "NULL"):
       self.name = name
       self.city = city
       self.addr = addr
       self.pin = pin
       self.img_path = pic_path
   
@app.route('/')
def show_all():
#    return "home"
    return render_template('show_all_14.html', students = students.query.all(),path = UPLOAD_FOLDER)


@app.route('/new', methods = ['POST','GET'])
def new():
     
    if request.method == 'POST':
        
        if not request.form['name'] or not request.form['city'] or not request.form['addr'] or not request.form['pin']:
#            return "no"
            flash("Please enter all fields", 'error')
            return render_template("new_14.html")
        else:
#            return "ys"
            try:
                file_name = request.files['img']
            
                if file_name and allowed_file(file_name.filename):
                    file_n = secure_filename(file_name.filename)
                    file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], file_n))
    
                    student = students(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'], file_n)
    #                              str(UPLOAD_FOLDER.split("\\")[-1]+'/'+
    #            return "yes"
                    db.session.add(student)
                    db.session.commit()
                    flash("Image and Data stored successfully!")
            except:
#                return "ys"
                student = students(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'], "NULL")
                db.session.add(student)
                db.session.commit()
                
                flash("No image uploaded!")        
                flash("Record was successfully added")
            
    return render_template("new_14.html")
#    return redirect(url_for('new'))
#    return render_template('new_14.html')

@app.route('/edit/<who>', methods = ['POST','GET'])
def edit(who):
#    print(request)
    if request.method in ['POST','GET']:

#        return "edited {}".format(who)

        temp = students.query.filter_by(id = who)
#        return "done"
#        a = []
#        for t in temp['id' == who]:
#            a.append(t)
#        return "done!"
#        return "{}".format(a) 
#        return "{}".format(temp['id' == who].img_path)
        return render_template("edit_14_new.html", resArr = temp['id' == who])
#    
#        students.query.filter_by(id = who).delete()
#        db.session.commit()
#        return render_template("new_14.html")
         

@app.route('/change', methods = ['POST','GET'])
def change():
    if request.method in ['POST','GET']:
    
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
            return render_template("edit_14_new.html", resArr = students.query.filter_by(id = id_)['id' == id_])
       
        try:
            
            new_image = request.files['img']
#            return "y"
            filename_new = secure_filename(new_image.filename)
#            return "{}".format(filename_new)
            if new_image and allowed_file(filename_new):

                x = students.query.filter_by(id = id_)
#               
                remove_img = x['img_path' == id_].img_path
#               
#                 return "{}".format(remove_img)
                new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_new))
#               #deleting image
                if remove_img != "NULL":
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], remove_img))
                
                stmt = "UPDATE students SET name = '{}', city = '{}', addr = '{}',\
                   pin = '{}', img_path = '{}' WHERE student_id = {};".format(nm, cy, ad, pn, filename_new, id_)
#                
                db.engine.execute(text(stmt))
#                
                db.session.commit()
            flash("Image Uploaded!")
#                         
        except:   
            
            filename_old = request.form['img_']
#            return "n"
#            
            stmt = "UPDATE students SET name = '{}', city = '{}', addr = '{}',\
                    pin = '{}', img_path = '{}' WHERE student_id = {};".format(nm, cy, ad, pn, filename_old, id_)
            
            db.engine.execute(text(stmt))
                
            db.session.commit()

            flash("Old Image Used!  ")
        flash("  Record has been successfully changed!")
    
    return render_template("show_all_14.html", students = students.query.all())

@app.route('/delete/<who>', methods = ['POST','GET'])
def delete(who):
#    return "{}".format(who)
    if request.method in ['POST','GET']:
        
#        return "deleted {}".format(who)
        x = students.query.filter_by(id = who)
        remove_img = x['img_path' == who].img_path
        
        # deleting image
        if remove_img in os.listdir(UPLOAD_FOLDER):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],remove_img))
        
        students.query.filter_by(id = who).delete()
        db.session.commit()
        return render_template("show_all_14.html", students = students.query.all())
                 
def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/<s_id>', methods = ['GET','POST'])
def upload_img(s_id):
#    return "yes"
    if request.method == 'POST':
#        print(request.files['img'])
        if 'img' not in request.files:
            flash("No file part!")
#            return "no img"
            return redirect(request.url)
        file_img = request.files['img']
    
#        return "{}".format(file_img.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
#        if file.filename == '':
#            flash("No selected file!")
#            return redirect(request.url)
#        return "img yes"
        if file_img and allowed_file(file_img.filename):
#            return "yes"
            
            x = students.query.filter_by(id = s_id)
#                
            remove_img = x['img_path' == s_id].img_path
            if remove_img != 'NULL':
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],remove_img))

            
            filename = secure_filename(file_img.filename)
            # check if image already present:
#            if filename in os.listdir(UPLOAD_FOLDER):
#                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
#                
            file_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            path_stmt = "UPDATE students SET img_path = '{}' WHERE student_id = \
                    {};".format(filename, s_id) # str(UPLOAD_FOLDER.split("\\")[-1]+'/'+
            
            db.engine.execute(text(path_stmt))
        
            db.session.commit()
            
            flash("Image stored successfully!")
        else:
            flash("Error with image upload!")
            
        return redirect(url_for('show_all'))
#            return redirect(url_for('uploaded_file',filename = filename))
        
    return '''
    <!doctype html>
    
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="POST" enctype="multipart/form-data">
      <p><input type = "file" name = "img"></p>
      <p><input type = "submit" value = "Upload"></p>
    </form>
    '''
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
if __name__ == "__main__":
    db.create_all()
    app.run()