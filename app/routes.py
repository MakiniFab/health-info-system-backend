from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Client, Program, ProgramOutcome, ActivityLog
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Initialize Blueprint
main = Blueprint('main', __name__)

# AUTH
# Register a new user
@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Login user and generate JWT token
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.username)
        return jsonify(access_token=token)
    return jsonify({"message": "Invalid credentials"}), 401

# CLIENT
# Create a new client
@main.route('/clients', methods=['POST'])
@jwt_required()
def create_client():
    data = request.get_json()
    client = Client(
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=data['age'],
        huduma_number=data['huduma_number']
    )
    db.session.add(client)
    db.session.commit()

    # Log the client registration
    log = ActivityLog(
        doctor_username=get_jwt_identity(),
        action=f"Registered client {client.first_name} {client.last_name}"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Client registered successfully"}), 201

# List all clients
@main.route('/clients', methods=['GET'])
@jwt_required()
def list_clients():
    clients = Client.query.all()
    result = [
        {
            "id": c.id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "age": c.age,
            "huduma_number": c.huduma_number
        }
        for c in clients
    ]
    return jsonify(result)

# Retrieve a specific client by ID
@main.route('/clients/<int:id>', methods=['GET'])
@jwt_required()
def get_client(id):
    client = Client.query.get_or_404(id)
    enrolled_programs = [p.name for p in client.programs]
    outcomes = [
        {
            "program": o.program.name,
            "outcome": o.outcome,
            "notes": o.notes
        }
        for o in client.outcomes
    ]
    return jsonify({
        "first_name": client.first_name,
        "last_name": client.last_name,
        "age": client.age,
        "huduma_number": client.huduma_number,
        "programs": enrolled_programs,
        "outcomes": outcomes
    })

# PROGRAM
# Create a new program
@main.route('/programs', methods=['POST'])
@jwt_required()
def create_program():
    data = request.get_json()
    program = Program(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(program)
    db.session.commit()
    return jsonify({"message": "Program created successfully"}), 201

# List all programs
@main.route('/programs', methods=['GET'])
@jwt_required()
def list_programs():
    programs = Program.query.all()
    result = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description
        }
        for p in programs
    ]
    return jsonify(result)

# Enroll a client into a program
@main.route('/enroll', methods=['POST'])
@jwt_required()
def enroll_client():
    data = request.get_json()
    client = Client.query.get_or_404(data['client_id'])
    program = Program.query.get_or_404(data['program_id'])
    client.programs.append(program)
    db.session.commit()

    # Log the enrollment
    log = ActivityLog(
        doctor_username=get_jwt_identity(),
        action=f"Enrolled {client.first_name} {client.last_name} in {program.name}"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": f"{client.first_name} {client.last_name} enrolled in {program.name}"}), 200

# OUTCOME
# Add an outcome for a client in a program
@main.route('/outcomes', methods=['POST'])
@jwt_required()
def add_outcome():
    data = request.get_json()
    outcome = ProgramOutcome(
        client_id=data['client_id'],
        program_id=data['program_id'],
        outcome=data['outcome'],
        notes=data.get('notes', '')
    )
    db.session.add(outcome)

    client = Client.query.get(data['client_id'])
    program = Program.query.get(data['program_id'])

    # Log the outcome update
    log = ActivityLog(
        doctor_username=get_jwt_identity(),
        action=f"Added outcome for {client.first_name} {client.last_name} in {program.name}"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Outcome recorded successfully"}), 201

# ACTIVITY LOG
# View all activity logs
@main.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()
    result = [
        {
            "doctor": log.doctor_username,
            "action": log.action,
            "timestamp": log.timestamp.isoformat()
        }
        for log in logs
    ]
    return jsonify(result)