# TaskManagerAPI
A RESTful API for managing tasks with user authentication, built using Django REST Framework.

## Features
- CRUD operations for tasks
- JWT Authentication
- Pagination
- Filtering by completion status
- User registration and login

## API Endpoints

### Authentication
- POST `/api/account/create/` - Register a new user
- POST `/api/token/` - Login and get JWT tokens
- POST `/api/token/refresh/` - Refresh JWT token

### Tasks
- GET `/api/tasks/` - List all tasks 
- POST `/api/tasks/` - Create a new task --------> [Authentication is Required]
- GET `/api/tasks/{id}/` - Get a specific task --> [Authentication is Required]
- PUT `/api/tasks/{id}/` - Update a task --------> [Authentication is Required]
- DELETE `/api/tasks/{id}/` - Delete a task -----> [Authentication is Required]

## Setup Instructions
1. Clone the repository
git clone https://github.com/Aaryan-2k/TaskManagerAPI.git
cd TaskManagerAPI

2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows:--> venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run migrations
python manage.py migrate

5. Start the development server
python manage.py runserver
