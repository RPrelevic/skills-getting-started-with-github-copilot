# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## Local Run

### Using `py` command (Windows)

If you're on Windows and the `python` command is not available, you can use the `py` launcher:

1. Install dependencies:
   ```
   py -m pip install -r requirements.txt
   ```

2. Run the application with uvicorn:
   ```
   py -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
   ```

### Using uvicorn directly

For FastAPI applications, it's recommended to use uvicorn as the ASGI server:

```
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

### Why it differs from regular python command

- **`py` vs `python`**: On Windows, the `py` launcher is the recommended way to run Python when multiple Python versions are installed or when the `python` command is not in your PATH. The `py` command automatically selects the appropriate Python version.

- **uvicorn vs direct execution**: FastAPI is an ASGI framework that requires an ASGI server like uvicorn to run properly. While you might be able to run `python app.py` directly, uvicorn provides:
  - Better performance and concurrency
  - Hot reloading with `--reload` flag
  - Production-ready server capabilities
  - Proper ASGI compliance for async operations

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
