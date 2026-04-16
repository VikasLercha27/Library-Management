# Library Management System

A comprehensive desktop application for managing library operations including book/movie inventory, member management, and issue/return tracking.

## Features

- **User Authentication** - Admin and regular user access with secure password hashing
- **Inventory Management** - Manage books and movies across multiple categories (Science, Economics, Fiction, Children, Personal Development)
- **Member Management** - Register and track library members with contact information and Aadhar verification
- **Issue & Return** - Track book/movie borrowing and returns with automatic fine calculation
- **Due Date Tracking** - Calendar-based date selection for issue and return dates
- **Fine Management** - Automatic fine calculation for overdue items (₹2 per day)
- **Category-wise Reports** - View items by category with detailed information
- **Admin Dashboard** - Administrative features for managing users, members, and inventory

## Requirements

- Python 3.x
- tkinter (usually included with Python)
- tkcalendar

## Installation

1. Install required dependencies:
```bash
pip install tkcalendar
```

2. Run the application:
```bash
python libraray.py
```

## Default Login Credentials

| Username | Password | Role |
|----------|----------|------|
| adm      | adm      | Admin |
| user     | user     | Regular User |

## System Structure

### Data Categories

The system includes the following categories:
- **Science (SC)** - Educational and scientific materials
- **Economics (EC)** - Business and economics books
- **Fiction (FC)** - Novels and fiction works
- **Children (CH)** - Children's books and movies
- **Personal Development (PD)** - Self-help and development materials

### Sample Data

The system comes pre-loaded with:
- 26 items (16 books, 10 movies)
- 4 sample members
- Sample issue records with overdue tracking

## Key Features

### Authentication
- Secure password hashing using SHA-256
- Role-based access (Admin/Regular User)
- Active/Inactive user management

### Inventory
- Unique serial codes for each item
- Cost tracking since procurement date
- Availability status tracking
- Support for both books and movies

### Membership
- Member ID generation
- Contact and address tracking
- Aadhar number verification
- Membership period management
- Fine balance tracking

### Issue Management
- Calendar date selection interface
- Automatic return date suggestions
- Overdue item tracking
- Fine calculation (₹2 per day for overdue items)
- Return date flexibility

## Usage

1. **Login** - Start the application and login with your credentials
2. **Navigate** - Use the menu options to access different modules
3. **Manage Inventory** - Add, update, or view books and movies
4. **Member Operations** - Register new members or update existing ones
5. **Issue Books** - Select member and book, set return date
6. **Return Books** - Mark books as returned and track fines
7. **Pay Fines** - Manage member fines

## Technical Details

- **GUI Framework** - Tkinter with ttk widgets
- **Database** - In-memory database (can be extended to use SQL)
- **Security** - SHA-256 password hashing
- **Date Handling** - Python datetime for date calculations

## Future Enhancements

- Database persistence (SQLite/MySQL)
- Email notifications for due dates
- Barcode scanning integration
- Advanced reporting and analytics
- Multi-user concurrent access
- Backup and restore functionality

## Notes

- Fine calculation is ₹2 per day for overdue items
- The application uses in-memory storage; data will be lost on restart
- Calendar widget enhancement via tkcalendar for better date selection
