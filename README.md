# PawnShop Project
This is a PawnShop application built with Django. It allows users to pawn their items, apply for loans, and view various items available for loans. The application includes user authentication (registration, login, logout) and has features for managing items and loans.
## Features
- User Registration and Authentication (Login, Logout, SignUp)
- Ability to view available items for pawn
- Loan creation and management
- Payments functionality (Update existing payments)
- Dynamic navigation bar depending on whether the user is logged in or not
- Responsive design with Bootstrap 4.6
## Tech Stack
- **Django** - Web framework used to build the application
- **Bootstrap 4.6** - Frontend framework for responsive design
- **SQLite** - Default database used (or you can change to another DB like PostgreSQL)
- **Python 3.x** - Programming language
## Installation
Follow the steps below to set up the project locally:
### 1. Clone the repository
  ```bash
  git clone https://github.com/yourusername/pawnshop.git
  cd pawnshop
  ```
### 2.Create and activate a virtual environment:
For Linux/Mac:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
  For Windows:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
### 3.Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
### 4.Apply database migrations:
  ```bash
  python manage.py migrate
  ```
### 5.Load sample data (optional):
  ```bash
  python manage.py loaddata test_data.json
  ```
### 6. Start the development server:
  ```bash
  python manage.py runserver
  ```

# PawnShop Relationship Diagram 


![](static/images/PawnShop_Diagram.png)

# PawnShop Preview
![](static/images/PawnShop_PreView.png)


## TestUser:
    
  ```bash

  username: anton_user
  
  password: 1qazcde3

  ```
## Visit PawnShop -> https://pawnshop-platform.onrender.com



