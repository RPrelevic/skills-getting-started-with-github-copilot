# Mergington High School Activities API

![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=flat-square)

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

## Testing

The application includes a comprehensive test suite using pytest to ensure all functionality works correctly.

### Running Tests

1. **Install test dependencies** (if not already installed):
   ```
   py -m pip install -r requirements.txt
   ```

2. **Run all tests**:
   ```
   py -m pytest tests/ -v
   ```

3. **Run tests with coverage report**:
   ```
   py -m pytest tests/ --cov=src --cov-report=term-missing -v
   ```

4. **Run specific test files**:
   ```
   py -m pytest tests/test_activities.py -v
   py -m pytest tests/test_validation.py -v
   ```

5. **Update coverage badge automatically**:
   ```
   # Windows
   scripts\update_badge.bat
   
   # Linux/Mac
   ./scripts/update_badge.sh
   
   # Direct Python execution
   py scripts/update_coverage_badge.py
   ```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Test fixtures and configuration
├── test_activities.py    # Main API endpoint tests
└── test_validation.py    # Edge cases and validation tests
```

### Test Coverage

The test suite includes:
- **22 comprehensive tests** covering all API endpoints
- **100% code coverage** of the main application
- **Core functionality tests**: signup, unregister, activity listing
- **Edge case validation**: special characters, unicode, long emails
- **Error scenario testing**: 404/400 responses, validation errors
- **Data integrity tests**: concurrent operations, data structure validation

#### Coverage Quality Indicators
- 🟢 **Green Badge (≥90%)**: Excellent coverage - Current status
- 🟡 **Amber Badge (≥75% <90%)**: Good coverage - needs improvement
- 🔴 **Red Badge (<75%)**: Poor coverage - requires attention

#### Automatic Badge Updates
The coverage badge is automatically updated:
- **🤖 GitHub Actions**: Automatically updates on every push/PR
- **💻 Local Updates**: Run `scripts\update_badge.bat` (Windows) or `./scripts/update_badge.sh` (Linux/Mac)
- **🔄 Manual Updates**: Use `py scripts/update_coverage_badge.py` directly

The badge color changes automatically based on coverage percentage, providing instant visual feedback on code quality.

### Test Features

- Automatic test data setup and cleanup
- FastAPI TestClient for realistic API testing
- Comprehensive assertions for response codes and data
- URL encoding and special character support testing
- Mock data isolation between tests

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/participants/{email}`               | Remove a participant from an activity                               |

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
