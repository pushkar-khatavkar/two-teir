# Two-Tier Flask Student Management System

A simple Flask REST API with MySQL database for managing students, courses, and enrollments. Ready to deploy on AWS.

## Architecture

```
Flask Web Tier → MySQL RDS Database Tier
```

## Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+ (or AWS RDS MySQL)
- pip

### Setup

1. **Install dependencies**
   ```bash
   pip install Flask Flask-SQLAlchemy PyMySQL python-dotenv
   ```

2. **Configure database**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL
   ```

3. **Run the app**
   ```bash
   python app.py
   ```
   Access at: `http://localhost:5000`

## API Endpoints

### Students
- `GET /api/students` - List all students
- `GET /api/students/<id>` - Get student
- `POST /api/students` - Create student
- `PUT /api/students/<id>` - Update student
- `DELETE /api/students/<id>` - Delete student

### Courses
- `GET /api/courses` - List all courses
- `GET /api/courses/<id>` - Get course
- `POST /api/courses` - Create course
- `PUT /api/courses/<id>` - Update course
- `DELETE /api/courses/<id>` - Delete course

### Enrollments
- `GET /api/enrollments` - List all enrollments
- `POST /api/enrollments` - Enroll student in course
- `PUT /api/enrollments/<id>` - Update enrollment (grade)
- `DELETE /api/enrollments/<id>` - Unenroll student

### Query Relationships
- `GET /api/students/<id>/courses` - Get student's courses
- `GET /api/courses/<id>/students` - Get course's students

## Example Requests

### Create Student
```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "student_id": "STU001"
  }'
```

### Create Course
```bash
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "course_code": "CS101",
    "course_name": "Intro to CS",
    "instructor": "Dr. Smith",
    "credits": 3,
    "capacity": 30
  }'
```

### Enroll Student
```bash
curl -X POST http://localhost:5000/api/enrollments \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "course_id": 1
  }'
```

## Database Models

**Students**
- id, first_name, last_name, email (unique), student_id (unique), enrollment_date

**Courses**
- id, course_code (unique), course_name, description, credits, instructor, capacity, created_date

**Enrollments**
- id, student_id, course_id, enrollment_date, grade

## AWS Deployment

### Using RDS MySQL

1. Create MySQL RDS instance in AWS console
2. Update `.env`:
   ```
   DATABASE_URL=mysql+pymysql://admin:password@your-rds-endpoint:3306/student_db
   ```
3. Deploy to AWS EC2 or ECS with Docker

### Using Docker

```bash
docker build -t flask-app .
docker run -p 5000:5000 -e DATABASE_URL=your_db_url flask-app
```

## Health Check
```bash
curl http://localhost:5000/health
```

## Project Structure
```
two-tier/
├── app.py              # Single file - all code
├── .env.example        # Environment template
├── requirements.txt    # Dependencies
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Dependencies
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- PyMySQL 1.1.0
- python-dotenv 1.0.0

## Notes
- All tables created automatically on first run
- Unique constraints prevent duplicate emails and student IDs
- Foreign keys ensure data integrity
- Capacity checking for course enrollment
