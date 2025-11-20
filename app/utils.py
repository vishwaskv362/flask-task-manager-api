"""Utility functions for the Flask application."""

from functools import wraps
from flask import request, jsonify


def validate_json(required_fields):
    """Decorator to validate required JSON fields in request."""

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request must be JSON"}), 400

            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return (
                    jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}),
                    400,
                )

            return f(*args, **kwargs)

        return wrapped

    return decorator


def paginate_query(query, page=1, per_page=20):
    """Paginate a SQLAlchemy query."""
    page = max(1, page)
    per_page = min(100, max(1, per_page))

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "items": [item.to_dict() for item in paginated.items],
        "total": paginated.total,
        "page": page,
        "per_page": per_page,
        "pages": paginated.pages,
    }
