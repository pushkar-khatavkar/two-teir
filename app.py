"""
Two-tier Flask Student Management System
Flask Web Tier + MySQL RDS Database Tier
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://root:password@localhost:3306/student_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ===== DATABASE MODELS =====

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'student_id': self.student_id,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None
        }


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, default=3)
    instructor = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, default=30)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_code': self.course_code,
            'course_name': self.course_name,
            'description': self.description,
            'credits': self.credits,
            'instructor': self.instructor,
            'capacity': self.capacity,
            'enrolled_count': len(self.enrollments),
            'created_date': self.created_date.isoformat() if self.created_date else None
        }


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.String(2))
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_student_course'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'student_name': f'{self.student.first_name} {self.student.last_name}',
            'course_code': self.course.course_code,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'grade': self.grade
        }


# ===== API ENDPOINTS =====

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200


@app.route('/', methods=['GET'])
def index():
    return {
        'message': 'Two-tier Flask Application',
        'version': '1.0.0',
        'endpoints': {
            'students': '/api/students',
            'courses': '/api/courses',
            'enrollments': '/api/enrollments'
        }
    }, 200


# STUDENT ENDPOINTS
@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200


@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify(student.to_dict()), 200


@app.route('/api/students', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        if not all(k in data for k in ['first_name', 'last_name', 'email', 'student_id']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            student_id=data['student_id']
        )
        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        data = request.get_json()
        if 'first_name' in data:
            student.first_name = data['first_name']
        if 'last_name' in data:
            student.last_name = data['last_name']
        if 'email' in data:
            student.email = data['email']
        db.session.commit()
        return jsonify(student.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# COURSE ENDPOINTS
@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses]), 200


@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify(course.to_dict()), 200


@app.route('/api/courses', methods=['POST'])
def create_course():
    try:
        data = request.get_json()
        if not all(k in data for k in ['course_code', 'course_name', 'instructor']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        course = Course(
            course_code=data['course_code'],
            course_name=data['course_name'],
            description=data.get('description', ''),
            credits=data.get('credits', 3),
            instructor=data['instructor'],
            capacity=data.get('capacity', 30)
        )
        db.session.add(course)
        db.session.commit()
        return jsonify(course.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        course = Course.query.get_or_404(course_id)
        data = request.get_json()
        if 'course_name' in data:
            course.course_name = data['course_name']
        if 'description' in data:
            course.description = data['description']
        if 'credits' in data:
            course.credits = data['credits']
        if 'instructor' in data:
            course.instructor = data['instructor']
        if 'capacity' in data:
            course.capacity = data['capacity']
        db.session.commit()
        return jsonify(course.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return jsonify({'message': 'Course deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ENROLLMENT ENDPOINTS
@app.route('/api/enrollments', methods=['GET'])
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([e.to_dict() for e in enrollments]), 200


@app.route('/api/enrollments', methods=['POST'])
def create_enrollment():
    try:
        data = request.get_json()
        if 'student_id' not in data or 'course_id' not in data:
            return jsonify({'error': 'Missing student_id or course_id'}), 400
        
        student = Student.query.get(data['student_id'])
        course = Course.query.get(data['course_id'])
        
        if not student or not course:
            return jsonify({'error': 'Student or course not found'}), 404
        
        if len(course.enrollments) >= course.capacity:
            return jsonify({'error': 'Course at full capacity'}), 409
        
        enrollment = Enrollment(
            student_id=data['student_id'],
            course_id=data['course_id']
        )
        db.session.add(enrollment)
        db.session.commit()
        return jsonify(enrollment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/enrollments/<int:enrollment_id>', methods=['PUT'])
def update_enrollment(enrollment_id):
    try:
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        data = request.get_json()
        if 'grade' in data:
            enrollment.grade = data['grade']
        db.session.commit()
        return jsonify(enrollment.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/enrollments/<int:enrollment_id>', methods=['DELETE'])
def delete_enrollment(enrollment_id):
    try:
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        db.session.delete(enrollment)
        db.session.commit()
        return jsonify({'message': 'Enrollment deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/students/<int:student_id>/courses', methods=['GET'])
def get_student_courses(student_id):
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    return jsonify([e.to_dict() for e in enrollments]), 200


@app.route('/api/courses/<int:course_id>/students', methods=['GET'])
def get_course_students(course_id):
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    return jsonify([e.to_dict() for e in enrollments]), 200


# Create tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
