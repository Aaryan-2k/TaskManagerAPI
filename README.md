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
```bash
git clone https://github.com/Aaryan-2k/TaskManagerAPI.git
cd TaskManagerAPI
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Start the development server
```bash
python manage.py runserver
```

## API Usage Examples

### Register a New User
```bash
curl -X POST http://localhost:8000/api/account/create/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123", "confirm_password": "testpass123", "email": "test@example.com"}'
```

### Login (Get Token)
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### Create a Task
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "description": "Test Description"}'
```

### List Tasks (with pagination)
```bash
curl -X GET http://localhost:8000/api/tasks/?page_num=1 \
  -H "Authorization: Bearer <your_token>"
```

### Filter Tasks by Completion Status
```bash
curl -X GET http://localhost:8000/api/tasks/?is_completed=true \
  -H "Authorization: Bearer <your_token>"
```