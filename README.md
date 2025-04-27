🏥 Health Information System Backend
This is the backend for a basic Health Information System built as part of a Software Engineering Intern Task.
It allows doctors to manage clients, enroll them into health programs, track outcomes, and expose client profiles via a clean API.

Built with a focus on security, clean architecture, scalability, and testability.

🚀 Features Implemented
# User Authentication
Secure user registration and login
# JWT-based token authentication (via Flask-JWT-Extended)
Password hashing and validation (via Werkzeug Security)
# Client Management
Register new clients
List all registered clients
Search and retrieve individual client profiles
# Program Management
Create and list health programs (e.g., TB, Malaria, HIV)
# Client Enrollment
Enroll clients into one or multiple programs
# Program Outcomes
Record outcomes for clients under different programs
# Activity Logging
Log every major action (registrations, enrollments, outcomes) for auditability
# API Exposure
Client profiles are accessible via secure RESTful APIs

🛠 Technologies Used
Technology	Purpose
Flask	Web framework to build API routes and server
Flask-JWT-Extended	Handling secure user authentication via JWT tokens
SQLAlchemy	ORM for database modeling and interaction
Werkzeug Security	For hashing and checking user passwords securely
test.http	For testing API routes directly from a simple client

🔐 Security Considerations
Password Security: All user passwords are hashed using generate_password_hash() from Werkzeug.
JWT Authentication: All sensitive endpoints are protected with @jwt_required().
Data Validation: API expects well-formed JSON bodies.
Activity Logs: Track every significant doctor action.

🧪 Testing
I used test.http files (HTTP client files) to test all API endpoints interactively.
Endpoints tested include:
User registration and login
Client creation and retrieval
Program creation
Client enrollment into programs
Outcome recording
Activity logs retrieval

📈 How I Addressed the Challenge
Clean Code & Documentation: Clear function names, modular code with blueprints, thorough comments.
API First Approach: Designed endpoints first with RESTful practices.
Security Built-in: JWT authentication and password hashing were a priority.
Expandability: The system can easily add more modules like appointments, prescriptions, etc.
Testing: I tested all major flows and handled edge cases.
Simple yet Powerful: Even though the system is minimalistic, it demonstrates real-world backend architecture.

🌍 How to Run Locally
Clone the repository:

git clone [https://github.com/yourusername/health-information-system.git](https://github.com/MakiniFab/health-info-system-backend)
cd health-information-system
Create a virtual environment:

python3 -m venv venv
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Run the application:
flask run
Test APIs via test.http or tools like Postman.

🌟 What Could Be Added Next
API documentation (Swagger / Postman Collection)
Pagination for listing clients/programs
Unit and integration tests (pytest + Flask testing client)

Admin dashboard interface

Deployment to Render or Railway (with environment configs)

👨‍💻 Author
[Your Name]
Software Engineer passionate about backend architecture, clean API design, and secure systems.
