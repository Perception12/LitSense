"""
Error Handling Module for LitSense API
======================================
Provides custom exceptions, error handlers, and validation utilities.
"""

import logging
from functools import wraps
from flask import jsonify, request
from typing import Any, Callable, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('litsense')


# =============================================================================
# Custom Exceptions
# =============================================================================

class APIError(Exception):
    """Base exception for all API errors."""
    
    def __init__(self, message: str, status_code: int = 400, payload: Optional[Dict] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to a dictionary for JSON response."""
        error_dict = {
            'error': True,
            'message': self.message,
            'status_code': self.status_code
        }
        if self.payload:
            error_dict['details'] = self.payload
        return error_dict


class NotFoundError(APIError):
    """Raised when a requested resource is not found."""
    
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(message, status_code=404)
        self.resource = resource
        self.identifier = identifier


class ValidationError(APIError):
    """Raised when request data validation fails."""
    
    def __init__(self, message: str, errors: Optional[List[str]] = None):
        super().__init__(message, status_code=400, payload={'validation_errors': errors or []})
        self.errors = errors or []


class DuplicateResourceError(APIError):
    """Raised when attempting to create a duplicate resource."""
    
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with identifier '{identifier}' already exists"
        super().__init__(message, status_code=409)


class InvalidJSONError(APIError):
    """Raised when request body contains invalid JSON."""
    
    def __init__(self):
        super().__init__("Request body must be valid JSON", status_code=400)


class MissingFieldError(ValidationError):
    """Raised when a required field is missing."""
    
    def __init__(self, field_name: str):
        message = f"Missing required field: '{field_name}'"
        super().__init__(message, errors=[f"Field '{field_name}' is required"])


class InvalidFieldError(ValidationError):
    """Raised when a field has an invalid value."""
    
    def __init__(self, field_name: str, reason: str):
        message = f"Invalid value for field '{field_name}': {reason}"
        super().__init__(message, errors=[message])


# =============================================================================
# Error Response Helpers
# =============================================================================

def error_response(message: str, status_code: int = 400, details: Optional[Dict] = None):
    """
    Create a standardized error response.
    
    Args:
        message: Human-readable error message
        status_code: HTTP status code
        details: Additional error details
    
    Returns:
        Tuple of (response, status_code)
    """
    response = {
        'error': True,
        'message': message,
        'status_code': status_code
    }
    if details:
        response['details'] = details
    
    logger.warning(f"API Error [{status_code}]: {message}")
    return jsonify(response), status_code


def success_response(data: Any, status_code: int = 200, message: Optional[str] = None):
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        status_code: HTTP status code
        message: Optional success message
    
    Returns:
        Tuple of (response, status_code)
    """
    response = {
        'success': True,
        'data': data
    }
    if message:
        response['message'] = message
    
    return jsonify(response), status_code


# =============================================================================
# Flask Error Handlers
# =============================================================================

def register_error_handlers(app):
    """
    Register all error handlers with the Flask app.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors."""
        logger.error(f"APIError: {error.message}")
        return jsonify(error.to_dict()), error.status_code
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle 400 Bad Request errors."""
        return error_response("Bad request", 400)
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 Not Found errors."""
        return error_response("Resource not found", 404)
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        return error_response(
            f"Method {request.method} not allowed for this endpoint", 
            405
        )
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 Internal Server errors."""
        logger.exception("Internal server error occurred")
        return error_response("Internal server error", 500)
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle any unexpected exceptions."""
        logger.exception(f"Unexpected error: {str(error)}")
        return error_response("An unexpected error occurred", 500)
    
    logger.info("Error handlers registered successfully")


# =============================================================================
# Validation Utilities
# =============================================================================

def validate_json(f: Callable) -> Callable:
    """
    Decorator to validate that request body contains valid JSON.
    
    Usage:
        @app.route('/endpoint', methods=['POST'])
        @validate_json
        def my_endpoint():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            raise InvalidJSONError()
        try:
            request.get_json()
        except Exception:
            raise InvalidJSONError()
        return f(*args, **kwargs)
    return decorated_function


def validate_required_fields(required_fields: List[str]) -> Callable:
    """
    Decorator factory to validate required fields in request JSON.
    
    Usage:
        @app.route('/endpoint', methods=['POST'])
        @validate_required_fields(['name', 'email'])
        def my_endpoint():
            ...
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json(silent=True) or {}
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                raise ValidationError(
                    "Missing required fields",
                    errors=[f"Field '{field}' is required" for field in missing_fields]
                )
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_employee_data(data: Dict, is_update: bool = False) -> List[str]:
    """
    Validate employee data and return list of validation errors.
    
    Args:
        data: Employee data dictionary
        is_update: If True, fields are optional (for partial updates)
    
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    allowed_fields = {'name', 'position'}
    
    # Check for unknown fields
    unknown_fields = set(data.keys()) - allowed_fields
    if unknown_fields:
        errors.append(f"Unknown fields: {', '.join(unknown_fields)}")
    
    # Validate required fields (for create operations)
    if not is_update:
        if 'name' not in data:
            errors.append("Field 'name' is required")
        if 'position' not in data:
            errors.append("Field 'position' is required")
    
    # Validate field types and values
    if 'name' in data:
        if not isinstance(data['name'], str):
            errors.append("Field 'name' must be a string")
        elif len(data['name'].strip()) == 0:
            errors.append("Field 'name' cannot be empty")
        elif len(data['name']) > 100:
            errors.append("Field 'name' must be 100 characters or less")
    
    if 'position' in data:
        if not isinstance(data['position'], str):
            errors.append("Field 'position' must be a string")
        elif len(data['position'].strip()) == 0:
            errors.append("Field 'position' cannot be empty")
        elif len(data['position']) > 100:
            errors.append("Field 'position' must be 100 characters or less")
    
    return errors


# =============================================================================
# Request Logging Middleware
# =============================================================================

def log_request_info():
    """Log information about incoming requests."""
    logger.info(f"{request.method} {request.path} - {request.remote_addr}")


def setup_request_logging(app):
    """
    Set up request/response logging for the Flask app.
    
    Args:
        app: Flask application instance
    """
    @app.before_request
    def before_request():
        log_request_info()
    
    @app.after_request
    def after_request(response):
        logger.info(f"Response: {response.status}")
        return response
