"""
Simple Book Management Application
Flask Web Tier + MySQL RDS Database Tier
Web form for adding, listing, updating, and deleting books
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://root:password@localhost:3306/books_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key-for-sessions'
db = SQLAlchemy(app)


# ===== DATABASE MODEL =====

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(100), nullable=False)
    book_name = db.Column(db.String(200), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Book {self.book_name}>'


# ===== ROUTES =====

@app.route('/')
def index():
    """Home page with form to add book"""
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/add', methods=['POST'])
def add_book():
    """Add a new book"""
    try:
        author_name = request.form.get('author_name')
        book_name = request.form.get('book_name')
        
        if not author_name or not book_name:
            flash('Author name and book name are required!', 'error')
            return redirect(url_for('index'))
        
        book = Book(author_name=author_name, book_name=book_name)
        db.session.add(book)
        db.session.commit()
        
        flash(f'Book "{book_name}" added successfully!', 'success')
        return redirect(url_for('index'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding book: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """Delete a book"""
    try:
        book = Book.query.get_or_404(book_id)
        book_name = book.book_name
        db.session.delete(book)
        db.session.commit()
        
        flash(f'Book "{book_name}" deleted successfully!', 'success')
        return redirect(url_for('index'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    """Edit a book"""
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        try:
            book.author_name = request.form.get('author_name')
            book.book_name = request.form.get('book_name')
            
            if not book.author_name or not book.book_name:
                flash('Author name and book name are required!', 'error')
                return redirect(url_for('edit_book', book_id=book.id))
            
            db.session.commit()
            flash(f'Book updated successfully!', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating book: {str(e)}', 'error')
            return redirect(url_for('edit_book', book_id=book.id))
    
    return render_template('edit.html', book=book)


# Create tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
