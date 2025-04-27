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
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

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
    client = Client(name=data['name'], age=data['age'])
    db.session.add(client)
    db.session.commit()

    # Log the client registration
    log = ActivityLog(doctor_username=get_jwt_identity(), action=f"Registered client {client.name}")
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Client registered"}), 201

# List all clients
@main.route('/clients', methods=['GET'])
@jwt_required()
def list_clients():
    clients = Client.query.all()
    result = [{"id": c.id, "name": c.name, "age": c.age} for c in clients]
    return jsonify(result)

# Retrieve a specific client by ID
@main.route('/clients/<int:id>', methods=['GET'])
@jwt_required()
def get_client(id):
    client = Client.query.get_or_404(id)
    enrolled_programs = [p.name for p in client.programs]
    outcomes = [{"program": o.program.name, "outcome": o.outcome, "notes": o.notes} for o in client.outcomes]
    return jsonify({
        "name": client.name,
        "age": client.age,
        "programs": enrolled_programs,
        "outcomes": outcomes
    })

# PROGRAM
# Create a new program
@main.route('/programs', methods=['POST'])
@jwt_required()
def create_program():
    data = request.get_json()
    program = Program(name=data['name'])
    db.session.add(program)
    db.session.commit()
    return jsonify({"message": "Program created"}), 201

# List all programs
@main.route('/programs', methods=['GET'])
@jwt_required()
def list_programs():
    programs = Program.query.all()
    result = [{"id": p.id, "name": p.name} for p in programs]
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
    log = ActivityLog(doctor_username=get_jwt_identity(), action=f"Enrolled {client.name} in {program.name}")
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": f"{client.name} enrolled in {program.name}"}), 200

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

    # Log the outcome update
    client = Client.query.get(data['client_id'])
    program = Program.query.get(data['program_id'])
    log = ActivityLog(
        doctor_username=get_jwt_identity(),
        action=f"Updated outcome for {client.name} in {program.name}"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Outcome recorded"}), 201

# ACTIVITY LOG
# View all activity logs (doctor actions)
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
