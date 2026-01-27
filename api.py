"""
LitSense API
============
Flask REST API for employee management with comprehensive error handling.
"""

from flask import Flask, request

from error_handling import (
    # Exceptions
    NotFoundError,
    ValidationError,
    InvalidJSONError,
    # Response helpers
    success_response,
    error_response,
    # Handlers and middleware
    register_error_handlers,
    setup_request_logging,
    # Validation
    validate_json,
    validate_employee_data,
    logger
)

# =============================================================================
# App Configuration
# =============================================================================

app = Flask(__name__)

# Register error handlers and request logging
register_error_handlers(app)
setup_request_logging(app)

# =============================================================================
# In-Memory Data Store
# =============================================================================

employees = [
    {'id': 1, 'name': 'John Doe', 'position': 'Developer'},
    {'id': 2, 'name': 'Jane Smith', 'position': 'Designer'},
    {'id': 3, 'name': 'Emily Johnson', 'position': 'Manager'}
]

next_employee_id = 4


# =============================================================================
# Helper Functions
# =============================================================================

def find_employee(employee_id: int):
    """Find an employee by ID or raise NotFoundError."""
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if employee is None:
        raise NotFoundError("Employee", employee_id)
    return employee


def parse_json_body():
    """Parse and return JSON from request body, or raise InvalidJSONError."""
    if not request.is_json:
        raise InvalidJSONError()
    try:
        data = request.get_json()
        if data is None:
            raise InvalidJSONError()
        return data
    except Exception:
        raise InvalidJSONError()


# =============================================================================
# API Routes
# =============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return success_response({'status': 'healthy'}, message="API is running")


@app.route('/employees', methods=['GET'])
def get_employees():
    """
    Get all employees.
    
    Returns:
        200: List of all employees
    """
    logger.info(f"Fetching all employees (count: {len(employees)})")
    return success_response(employees)


@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee_by_id(employee_id: int):
    """
    Get a specific employee by ID.
    
    Args:
        employee_id: The employee's unique identifier
        
    Returns:
        200: Employee data
        404: Employee not found
    """
    employee = find_employee(employee_id)
    logger.info(f"Fetched employee: {employee['name']}")
    return success_response(employee)


@app.route('/employees', methods=['POST'])
@validate_json
def create_employee():
    """
    Create a new employee.
    
    Request Body:
        name (str): Employee's name (required)
        position (str): Employee's position (required)
        
    Returns:
        201: Created employee with assigned ID
        400: Validation error
    """
    global next_employee_id
    
    data = parse_json_body()
    
    # Validate employee data
    validation_errors = validate_employee_data(data, is_update=False)
    if validation_errors:
        raise ValidationError("Invalid employee data", errors=validation_errors)
    
    # Create new employee
    new_employee = {
        'id': next_employee_id,
        'name': data['name'].strip(),
        'position': data['position'].strip()
    }
    
    next_employee_id += 1
    employees.append(new_employee)
    
    logger.info(f"Created employee: {new_employee['name']} (ID: {new_employee['id']})")
    return success_response(new_employee, status_code=201, message="Employee created successfully")


@app.route('/employees/<int:employee_id>', methods=['PUT'])
@validate_json
def update_employee(employee_id: int):
    """
    Update an existing employee.
    
    Args:
        employee_id: The employee's unique identifier
        
    Request Body:
        name (str): Employee's name (optional)
        position (str): Employee's position (optional)
        
    Returns:
        200: Updated employee data
        400: Validation error
        404: Employee not found
    """
    employee = find_employee(employee_id)
    data = parse_json_body()
    
    # Validate update data (partial updates allowed)
    validation_errors = validate_employee_data(data, is_update=True)
    if validation_errors:
        raise ValidationError("Invalid employee data", errors=validation_errors)
    
    # Apply updates
    if 'name' in data:
        employee['name'] = data['name'].strip()
    if 'position' in data:
        employee['position'] = data['position'].strip()
    
    logger.info(f"Updated employee: {employee['name']} (ID: {employee_id})")
    return success_response(employee, message="Employee updated successfully")


@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id: int):
    """
    Delete an employee.
    
    Args:
        employee_id: The employee's unique identifier
        
    Returns:
        200: Confirmation message
        404: Employee not found
    """
    global employees
    
    employee = find_employee(employee_id)
    employee_name = employee['name']
    
    employees = [e for e in employees if e['id'] != employee_id]
    
    logger.info(f"Deleted employee: {employee_name} (ID: {employee_id})")
    return success_response(
        {'deleted_id': employee_id},
        message=f"Employee '{employee_name}' deleted successfully"
    )


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == '__main__':
    logger.info("Starting LitSense API server...")
    app.run(debug=True, host="0.0.0.0", port=8080)
    