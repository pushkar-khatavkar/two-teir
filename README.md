# Book Management System

A simple and elegant web application for managing your book collection. Built with Flask and MySQL, ready to deploy on AWS.

## Features

- ➕ **Add Books** - Add new books with author name and book title
- 📖 **View Books** - Browse all books in your collection
- ✏️ **Edit Books** - Update book information
- 🗑️ **Delete Books** - Remove books from collection
- 💾 **Persistent Storage** - All data saved in MySQL database
- 🎨 **Beautiful UI** - Modern, responsive design
- ☁️ **AWS Ready** - Easy deployment to AWS RDS

## Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+ (or AWS RDS MySQL)
- pip

### Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to: `http://localhost:5000`

## Usage

### Add a Book
1. Enter the author name
2. Enter the book title
3. Click "Add Book"
4. The book will appear in the list below

### Edit a Book
1. Find the book in the list
2. Click the "✏️ Edit" button
3. Update the author name or book title
4. Click "💾 Save Changes"

### Delete a Book
1. Find the book in the list
2. Click the "🗑️ Delete" button
3. Confirm the deletion

## Database Configuration

### Local MySQL
Create a database first:
```bash
mysql -u root -p
CREATE DATABASE books_db;
EXIT;
```

Then set `DATABASE_URL` in `.env`:
```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/books_db
```

### AWS RDS MySQL

1. Create MySQL RDS instance in AWS Console
2. Update `.env`:
   ```
   DATABASE_URL=mysql+pymysql://admin:your_password@your-rds-endpoint.region.rds.amazonaws.com:3306/books_db
   ```

3. Database tables created automatically on first run

## Project Structure

```
two-tier/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── .gitignore                 # Git ignore rules
└── templates/
    ├── index.html             # Main page (add & list books)
    └── edit.html              # Edit book page
```

## Technologies Used

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database
- **MySQL** - Database
- **HTML5 & CSS3** - Frontend
- **Python 3** - Backend

## Database Schema

### Books Table
```sql
CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    author_name VARCHAR(100) NOT NULL,
    book_name VARCHAR(200) NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## API Information

While this is a web form application, here's how data flows:

- **POST /add** - Add new book (form submission)
- **POST /delete/<book_id>** - Delete book (form submission)
- **GET /edit/<book_id>** - Show edit form
- **POST /edit/<book_id>** - Update book (form submission)
- **GET /** - Show main page with all books

## Deployment

### Deploy to AWS EC2

1. Launch EC2 instance (Ubuntu 20.04+)
2. Install Python and MySQL client:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv mysql-client
   ```
3. Clone repository:
   ```bash
   git clone <your-repo-url>
   cd two-tier
   ```
4. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Configure .env with RDS endpoint
7. Run application:
   ```bash
   python app.py
   ```

### Production Deployment with Gunicorn

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

## Troubleshooting

### Database Connection Error
```
Check that:
- MySQL is running
- DATABASE_URL in .env is correct
- Database and user exist
- User has proper permissions
```

### Port Already in Use
```bash
# Find process using port 5000
lsof -ti:5000

# Kill the process
kill -9 <PID>
```

### Tables Not Created
- Application creates tables automatically on startup
- Check that your database user has CREATE privileges

## Notes

- The application uses Flask sessions for messages, ensure `secret_key` is set
- Flash messages auto-close after being dismissed
- Dates are stored in UTC format
- All fields are required (Author name and Book name)

## Future Enhancements

- Add book categories/genres
- Search and filter functionality
- User authentication and multi-user support
- Book ratings and reviews
- Export to CSV/PDF
- Advanced search with pagination

## License

This project is provided for educational purposes.

## Support

For issues or questions, refer to:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
