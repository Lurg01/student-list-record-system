# 1 > Importing Frameworks and libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_


# 2 > Pagamit ng Flask at pagsubtitute sa variable app at gamitin ang app upang i configure ang ating database
app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/student_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 3 > Nag declare tayo ng class upang makagawa ng object.
# Creating model table for our student database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    year = db.Column(db.String(100))
    section = db.Column(db.String(100))


    # 3-1 > Gumamit tayo ng def __init__() upang makapagkonstrak. Iinitialize ang attributes ng class
    def __init__(self, name, address, email, phone, year, section):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.year = year
        self.section = section


# 4 > nagdeclare tayo ng function na Index na may route upang mabasa ang lahat ng student data
@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", students=all_data)


# 5 > Ang route naman na ito ng may insert function ay upang makapag insert tayo ng data sa database
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        year = request.form['year']
        section = request.form['section']

        my_data = Data(name, address, email, phone, year, section)
        db.session.add(my_data)
        db.session.commit()

        flash("Student Inserted Successfully")

        return redirect(url_for('Index'))


# 6 > Ang route naman na ito ay may function na pag uupdate sa ating existing data sa student database
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.address = request.form['address']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.year = request.form['year']
        my_data.section = request.form['section']

        db.session.commit()
        flash("Student Updated Successfully")

        return redirect(url_for('Index'))

# 7 > Ang route naman na ito ay may function na pagdedelete sa student database.
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")

    return redirect(url_for('Index'))

# 8 > Ang route na ito ay may function upang mkapagsearch tayo ng specific data sa ating student database
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = Data.query.filter(or_(Data.name.like(search), Data.year.like(search), Data.section.like(search))).all()

        return render_template("index.html", students = results, legend = " Search Results")
    else:
        return redirect(url_for('Index'))

# 9 > ginamit natin ang statement nato upang eexecute kung ang file ay nirun directly at hindi
# ito inimport.
if __name__ == "__main__":
    app.run(debug=True)



