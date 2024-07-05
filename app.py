
<<<<<<< HEAD
# A very simple Flask Hello World app for you to get started with...
=======
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
    
@app.route('/')
def index():
    return redirect(url_for('get_all_students'))

@app.route('/test')
def testing_2():
    return "<p> testing another route</p>"    
>>>>>>> origin/main

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

