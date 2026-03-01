from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)  # Enable CORS

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resumes.db'
db = SQLAlchemy(app)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    skills = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Resume {self.name}>'

@app.route('/submit', methods=['POST'])
def submit_resume():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    skills = data.get('skills')

    # Validate data
    if not name or not email or not phone:
        return jsonify({'message': 'Missing required fields'}), 400

    new_resume = Resume(name=name, email=email, phone=phone, skills=skills)
    db.session.add(new_resume)
    db.session.commit()
    return jsonify({'message': 'Resume submitted successfully'}), 201

@app.route('/resumes', methods=['GET'])
def get_resumes():
    resumes = Resume.query.all()
    return jsonify([{'name': r.name, 'email': r.email, 'phone': r.phone, 'skills': r.skills} for r in resumes]), 200

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)