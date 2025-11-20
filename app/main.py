"""Main Flask application with API endpoints."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from app.models import db, User, Task, Category
from app.config import config
from datetime import datetime
import os


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register routes
    register_routes(app)

    return app


def register_routes(app):
    """Register all API endpoints."""

    @app.route("/")
    def index():
        """Root endpoint with API information."""
        return jsonify(
            {
                "message": "Flask Task Manager API",
                "version": "0.1.0",
                "endpoints": {
                    "health": "/health",
                    "users": "/api/users",
                    "tasks": "/api/tasks",
                    "categories": "/api/categories",
                    "statistics": "/api/stats",
                },
            }
        )

    @app.route("/health")
    def health():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

    # ========== USER ENDPOINTS ==========

    @app.route("/api/users", methods=["GET"])
    def get_users():
        """Get all users."""
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    @app.route("/api/users", methods=["POST"])
    def create_user():
        """Create a new user."""
        data = request.get_json()

        if not data or not data.get("username") or not data.get("email"):
            return jsonify({"error": "Username and email are required"}), 400

        # Check if user already exists
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"error": "Username already exists"}), 400

        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already exists"}), 400

        user = User(username=data["username"], email=data["email"])
        db.session.add(user)
        db.session.commit()

        return jsonify(user.to_dict()), 201

    @app.route("/api/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        """Get a specific user by ID."""
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    @app.route("/api/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        """Delete a user."""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200

    # ========== TASK ENDPOINTS ==========

    @app.route("/api/tasks", methods=["GET"])
    def get_tasks():
        """Get all tasks with optional filtering."""
        status = request.args.get("status")
        priority = request.args.get("priority")
        user_id = request.args.get("user_id", type=int)

        query = Task.query

        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if user_id:
            query = query.filter_by(user_id=user_id)

        tasks = query.all()
        return jsonify([task.to_dict() for task in tasks])

    @app.route("/api/tasks", methods=["POST"])
    def create_task():
        """Create a new task."""
        data = request.get_json()

        if not data or not data.get("title") or not data.get("user_id"):
            return jsonify({"error": "Title and user_id are required"}), 400

        # Verify user exists
        user = User.query.get(data["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        task = Task(
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", "pending"),
            priority=data.get("priority", "medium"),
            user_id=data["user_id"],
        )

        if data.get("due_date"):
            try:
                task.due_date = datetime.fromisoformat(data["due_date"])
            except ValueError:
                return jsonify({"error": "Invalid due_date format"}), 400

        db.session.add(task)
        db.session.commit()

        return jsonify(task.to_dict()), 201

    @app.route("/api/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id):
        """Get a specific task by ID."""
        task = Task.query.get_or_404(task_id)
        return jsonify(task.to_dict())

    @app.route("/api/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        """Update a task."""
        task = Task.query.get_or_404(task_id)
        data = request.get_json()

        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "status" in data:
            task.status = data["status"]
        if "priority" in data:
            task.priority = data["priority"]
        if "due_date" in data:
            try:
                task.due_date = datetime.fromisoformat(data["due_date"])
            except ValueError:
                return jsonify({"error": "Invalid due_date format"}), 400

        task.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(task.to_dict())

    @app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        """Delete a task."""
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200

    # ========== CATEGORY ENDPOINTS ==========

    @app.route("/api/categories", methods=["GET"])
    def get_categories():
        """Get all categories."""
        categories = Category.query.all()
        return jsonify([category.to_dict() for category in categories])

    @app.route("/api/categories", methods=["POST"])
    def create_category():
        """Create a new category."""
        data = request.get_json()

        if not data or not data.get("name"):
            return jsonify({"error": "Category name is required"}), 400

        if Category.query.filter_by(name=data["name"]).first():
            return jsonify({"error": "Category already exists"}), 400

        category = Category(name=data["name"], description=data.get("description", ""))
        db.session.add(category)
        db.session.commit()

        return jsonify(category.to_dict()), 201

    # ========== STATISTICS ENDPOINT ==========

    @app.route("/api/stats")
    def get_statistics():
        """Get application statistics."""
        total_users = User.query.count()
        total_tasks = Task.query.count()
        total_categories = Category.query.count()

        task_stats = {
            "pending": Task.query.filter_by(status="pending").count(),
            "in_progress": Task.query.filter_by(status="in_progress").count(),
            "completed": Task.query.filter_by(status="completed").count(),
        }

        priority_stats = {
            "low": Task.query.filter_by(priority="low").count(),
            "medium": Task.query.filter_by(priority="medium").count(),
            "high": Task.query.filter_by(priority="high").count(),
        }

        return jsonify(
            {
                "total_users": total_users,
                "total_tasks": total_tasks,
                "total_categories": total_categories,
                "tasks_by_status": task_stats,
                "tasks_by_priority": priority_stats,
            }
        )

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


# Create the application instance
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
