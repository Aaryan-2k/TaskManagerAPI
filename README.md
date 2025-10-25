# Task Manager API
A RESTful API for managing tasks with user authentication, built using Django REST Framework.

## Features
- CRUD operations for tasks
- JWT Authentication
- Pagination
- Filtering by completion status
- User registration and login
- Comprehensive test suite

## API Endpoints

### Authentication
- POST `/api/account/create/` - Register a new user (Public)
- POST `/api/token/` - Login and get JWT tokens (Public)
- POST `/api/token/refresh/` - Refresh JWT token (Public)

### Tasks
- GET `/api/tasks/` - List all tasks (paginated) 🔒
- POST `/api/tasks/` - Create a new task 🔒
- GET `/api/tasks/{id}/` - Get a specific task 🔒
- PUT `/api/tasks/{id}/` - Update a task 🔒 
- DELETE `/api/tasks/{id}/` - Delete a task 🔒

Note: 🔒 indicates endpoints that require JWT authentication token

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

## Running Tests

The application includes comprehensive test coverage for all major functionality. To run the tests:

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test api.tests.AuthenticationTests
```

The test suite includes:
- Authentication Tests (registration, login, token generation)
- Task API Tests (CRUD operations)
- Task Filter Tests (completion status filtering)
- Pagination Tests
- Permission Tests

## API Usage Examples

### Register a New User
```bash
curl -X POST http://localhost:8000/api/account/create/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123", "confirm_password": "testpass123", "email": "test@example.com"}'
```
Response:
```json
{
    "username": "testuser",
    "email": "test@example.com"
}
```

### Login (Get Token)
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```
Response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
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
  -H "Authorization: Bearer <your_access_token>"
```
```
Response:
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/tasks/?page_num=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "title": "Test Task",
            "description": "Test Description",
            "completed": false,
            "created_at": "2025-10-24T10:30:00Z",
            "updated_at": "2025-10-24T10:30:00Z"
        },
        ...
    ]
}
```

### Filter Tasks by Completion Status
```bash
curl -X GET http://localhost:8000/api/tasks/?is_completed=true \
  -H "Authorization: Bearer <your_access_token>"

```
Response:
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "user": 1,
            "title": "Completed Task",
            "description": "This task is done",
            "completed": true,
            "created_at": "2025-10-24T09:00:00Z",
            "updated_at": "2025-10-24T10:00:00Z"
        },
        ...
    ]
}
```
### Get a specific Task
```bash
curl -X GET http://localhost:8000/api/tasks/1/ \
  -H "Authorization: Bearer <your_access_token>"

```
Response:
```json
{
    "id": 1,
    "user": 1,
    "title": "Specific Task",
    "description": "Description",
    "completed": true,
    "created_at": "2025-10-24T10:30:00Z",
    "updated_at": "2025-10-24T11:00:00Z"
}
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/api/tasks/1/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "description": "Updated Description", "completed": true}'
```
Response:
```json
{
    "id": 1,
    "user": 1,
    "title": "Updated Task",
    "description": "Updated Description",
    "completed": true,
    "created_at": "2025-10-24T10:30:00Z",
    "updated_at": "2025-10-24T11:00:00Z"
}
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/api/tasks/1/ \
  -H "Authorization: Bearer <your_access_token>"
```
Response: 
HTTP Status 204 No Content
