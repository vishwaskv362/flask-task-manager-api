# Flask Task Manager API 🚀

A comprehensive REST API built with Flask for task management, user authentication, and data persistence using SQLite. This project demonstrates modern Python development practices using **uv** package manager for dependency management and virtual environment handling.

## 📋 Features

- **10 RESTful API Endpoints** for complete CRUD operations
- **SQLite Database** integration with SQLAlchemy ORM
- **User Management** system with task ownership
- **Task Management** with status, priority, and due dates
- **Category System** for organizing tasks
- **Statistics Dashboard** for analytics
- **CORS Support** for cross-origin requests
- **Environment Configuration** for different deployment stages
- **Database Seeding** utilities for quick setup

## 🛠️ Tech Stack

- **Framework**: Flask 3.0+
- **Database**: SQLite with SQLAlchemy ORM
- **Package Manager**: uv (fast Python package installer and resolver)
- **CORS**: Flask-CORS for API access
- **Testing**: pytest and pytest-cov
- **Code Quality**: Black, Ruff

## 📦 Why uv?

This project uses [uv](https://github.com/astral-sh/uv) - a blazingly fast Python package installer and resolver written in Rust. Benefits include:

- ⚡ **10-100x faster** than pip
- 🔒 **Reliable dependency resolution**
- 🎯 **Drop-in replacement** for pip
- 📦 **Built-in virtual environment management**
- 🔄 **Compatible with pyproject.toml**

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- uv package manager

### Installing uv

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Project Setup

1. **Clone the repository:**
```powershell
git clone <repository-url>
cd flask-task-manager-api
```

2. **Create and activate virtual environment with uv:**
```powershell
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
```

3. **Install dependencies:**
```powershell
uv pip install -e .
```

4. **Install development dependencies:**
```powershell
uv pip install -e ".[dev]"
```

5. **Set up environment variables:**
```powershell
Copy-Item .env.example .env
# Edit .env with your configuration
```

6. **Initialize the database:**
```powershell
# Create tables
uv run python init_db.py init

# Seed with sample data (optional)
uv run python init_db.py seed
```

7. **Run the application:**
```powershell
uv run python -m app.main
```

The API will be available at `http://localhost:5000`

## 📚 API Endpoints

### General Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check endpoint |

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users |
| POST | `/api/users` | Create a new user |
| GET | `/api/users/<id>` | Get specific user |
| DELETE | `/api/users/<id>` | Delete a user |

### Task Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks (supports filtering) |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/<id>` | Get specific task |
| PUT | `/api/tasks/<id>` | Update a task |
| DELETE | `/api/tasks/<id>` | Delete a task |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | Get all categories |
| POST | `/api/categories` | Create a new category |

### Statistics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Get application statistics |

## 📝 API Usage Examples

### Create a User
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "email": "john@example.com"}'
```

### Create a Task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the Flask API project",
    "status": "in_progress",
    "priority": "high",
    "user_id": 1
  }'
```

### Get Tasks by Status
```bash
curl http://localhost:5000/api/tasks?status=pending&priority=high
```

### Update a Task
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Get Statistics
```bash
curl http://localhost:5000/api/stats
```

## 🧪 Testing

Run tests with pytest:

```powershell
# Install test dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html
```

## 🔧 Development

### Code Formatting

```powershell
# Format code with Black
uv run black app/

# Lint with Ruff
uv run ruff check app/
```

### Database Management

```powershell
# Reset and reseed database
uv run python init_db.py seed

# Just initialize tables
uv run python init_db.py init
```

## 📂 Project Structure

```
flask-task-manager-api/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Flask application and routes
│   ├── models.py            # Database models
│   ├── config.py            # Configuration settings
│   └── utils.py             # Utility functions
├── tests/                   # Test directory
├── init_db.py               # Database initialization script
├── pyproject.toml           # Project dependencies (uv)
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── .python-version          # Python version specification
└── README.md                # This file
```

## 🌐 Environment Variables

Create a `.env` file based on `.env.example`:

```env
FLASK_APP=app.main:app
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///tasks.db
```

## 🚢 Deployment

### Production Considerations

1. **Set production environment:**
```powershell
$env:FLASK_ENV="production"
```

2. **Use a production WSGI server:**
```powershell
uv pip install gunicorn
uv run gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

3. **Update SECRET_KEY** in production environment

4. **Consider using PostgreSQL** instead of SQLite for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Resources

- [uv Documentation](https://github.com/astral-sh/uv)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 💡 Alternative: Using Pixi

While this project is configured for **uv**, you can also use [Pixi](https://pixi.sh/) - another modern package manager that supports both Python and system dependencies.

### Setting up with Pixi

```powershell
# Install Pixi
powershell -c "iwr -useb https://pixi.sh/install.ps1 | iex"

# Initialize Pixi project
pixi init

# Add Python dependencies
pixi add python=3.10 flask flask-cors flask-sqlalchemy python-dotenv

# Add dev dependencies
pixi add --feature dev pytest pytest-cov black ruff

# Run the application
pixi run python -m app.main
```

### Why consider Pixi?

- 🌍 **Cross-platform** package management (Python + system deps)
- 📦 **Conda-compatible** with broader ecosystem
- 🔐 **Reproducible** environments with lock files
- 🚀 **Fast** installation and dependency resolution

Choose **uv** for pure Python projects (recommended for this repo) or **Pixi** when you need system-level dependencies and cross-platform support.

---

**Built with ❤️ using Flask and uv**
