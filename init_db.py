"""Database initialization and seeding utilities."""

from app.main import app
from app.models import db, User, Task, Category
from datetime import datetime, timedelta


def init_db():
    """Initialize the database and create tables."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")


def seed_db():
    """Seed the database with sample data."""
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create sample users
        users = [
            User(username="john_doe", email="john@example.com"),
            User(username="jane_smith", email="jane@example.com"),
            User(username="bob_wilson", email="bob@example.com"),
        ]

        for user in users:
            db.session.add(user)

        db.session.commit()

        # Create sample categories
        categories = [
            Category(name="Work", description="Work-related tasks"),
            Category(name="Personal", description="Personal tasks"),
            Category(name="Shopping", description="Shopping list items"),
            Category(name="Study", description="Learning and study tasks"),
        ]

        for category in categories:
            db.session.add(category)

        db.session.commit()

        # Create sample tasks
        tasks = [
            Task(
                title="Complete project proposal",
                description="Write and submit the Q4 project proposal",
                status="in_progress",
                priority="high",
                due_date=datetime.utcnow() + timedelta(days=3),
                user_id=1,
            ),
            Task(
                title="Review pull requests",
                description="Review pending PRs in the repository",
                status="pending",
                priority="medium",
                user_id=1,
            ),
            Task(
                title="Buy groceries",
                description="Milk, eggs, bread, vegetables",
                status="pending",
                priority="low",
                due_date=datetime.utcnow() + timedelta(days=1),
                user_id=2,
            ),
            Task(
                title="Finish Flask tutorial",
                description="Complete the advanced Flask course",
                status="in_progress",
                priority="high",
                user_id=2,
            ),
            Task(
                title="Update documentation",
                description="Update API documentation with new endpoints",
                status="completed",
                priority="medium",
                user_id=1,
            ),
            Task(
                title="Call dentist",
                description="Schedule annual checkup appointment",
                status="pending",
                priority="medium",
                user_id=3,
            ),
            Task(
                title="Read Python book",
                description="Read chapters 5-7",
                status="in_progress",
                priority="low",
                user_id=3,
            ),
        ]

        for task in tasks:
            db.session.add(task)

        db.session.commit()

        print("Database seeded successfully!")
        print(f"Created {len(users)} users")
        print(f"Created {len(categories)} categories")
        print(f"Created {len(tasks)} tasks")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            init_db()
        elif sys.argv[1] == "seed":
            seed_db()
        else:
            print("Usage: python init_db.py [init|seed]")
    else:
        print("Usage: python init_db.py [init|seed]")
        print("  init - Create database tables")
        print("  seed - Seed database with sample data")
