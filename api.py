import json
from flask import Flask, request, jsonify


app = Flask(__name__)

employees = [{'id': 1, 'name': 'John Doe', 'position': 'Developer'},
                {'id': 2, 'name': 'Jane Smith', 'position': 'Designer'},
                {'id': 3, 'name': 'Emily Johnson', 'position': 'Manager'}]

nextEmployeeId = 4

@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)


def get_employee(employee_id):
    return next((employee for employee in employees if employee['id'] == employee_id), None)

def employee_is_valid(employee):
    for key in employee.keys():
        if key not in ['name', 'position']:
            return False
    return True


@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee_by_id(employee_id):
    employee = get_employee(employee_id)
    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404
    return jsonify(employee)

@app.route('/employees', methods=['POST'])
def create_employee():
    global nextEmployeeId
    employee = json.loads(request.data)
    
    if not employee_is_valid(employee):
        return jsonify({'error': 'Invalid employee data'}), 400
    
    employee['id'] = nextEmployeeId
    nextEmployeeId += 1
    employees.append(employee)
    return jsonify(employee), 201

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = get_employee(employee_id)
    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404
    
    updated_employee = json.loads(request.data)
    if not employee_is_valid(updated_employee):
        return jsonify({'error': 'Invalid employee data'}), 400
    
    employee.update(updated_employee)

    return jsonify(employee)


@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    global employees
    employee = get_employee(employee_id)
    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404
    
    employees = [e for e in employees if e['id'] != employee_id]
    return jsonify(employees), 200



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
    