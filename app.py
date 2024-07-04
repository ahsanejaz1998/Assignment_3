from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)

@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        data = request.form
        try:
            student.first_name = data['first_name']
            student.last_name = data['last_name']
            student.dob = datetime.strptime(data['dob'], '%Y-%m-%d')
            student.amount_due = float(data['amount_due'])
            db.session.commit()
            return redirect(url_for('get_student', student_id=student.student_id))
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return render_template('update_student.html', student=student)

@app.route('/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    return render_template('all_students.html', students=students)

@app.route('/student/new', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        data = request.form
        try:
            new_student = Student(
                first_name=data['first_name'],
                last_name=data['last_name'],
                dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
                amount_due=float(data['amount_due'])
            )
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('get_student', student_id=new_student.student_id))
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return render_template('create_student.html')

@app.route('/student/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('get_all_students'))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
