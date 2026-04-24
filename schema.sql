-- Library Management System Database Schema
-- Run this script to create/upgrade the database tables

CREATE DATABASE IF NOT EXISTS library_management;
USE library_management;

-- Users table (for authentication)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    role ENUM('admin', 'librarian') DEFAULT 'librarian',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Books table (enhanced with AI fields)
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn_13 VARCHAR(13),
    isbn_10 VARCHAR(10),
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    publisher VARCHAR(255),
    category VARCHAR(100),
    ai_summary TEXT,
    ai_suggested_genres VARCHAR(255),
    cover_image_url TEXT,
    shelf_location VARCHAR(50),
    available_copies INT DEFAULT 1,
    total_copies INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(20) PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    enrollment_year INT,
    current_outstanding INT DEFAULT 0,
    borrow_limit INT DEFAULT 5,
    total_fines_paid DECIMAL(10,2) DEFAULT 0.00
);

-- Transactions table (borrow/return records)
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    book_id INT,
    borrow_date DATETIME,
    due_date DATE,
    return_date DATETIME,
    fine_amount DECIMAL(10,2) DEFAULT 0.00,
    book_condition_on_return VARCHAR(50) DEFAULT 'Good',
    status ENUM('Active', 'Returned', 'Overdue') DEFAULT 'Active',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- Create indexes for better performance
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_author ON books(author);
CREATE INDEX idx_books_isbn13 ON books(isbn_13);
CREATE INDEX idx_books_isbn10 ON books(isbn_10);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_student ON transactions(student_id);

-- Insert a default admin user (password: admin123)
-- Note: In production, use a proper password hash
INSERT IGNORE INTO users (username, password_hash, email, role) 
VALUES ('admin', 'pbkdf2:sha256:260000$defaultsalt$e4b1fa6ae62e8cdb7e55b1b35c6386ef54b9435a95ce16b9e67c91b5c1e5e6d8', 'admin@library.com', 'admin');
