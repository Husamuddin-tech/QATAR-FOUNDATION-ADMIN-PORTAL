from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    """Admin user model"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship: One Admin can have many Opportunities
    opportunities = db.relationship('Opportunity', backref='creator', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password, method='scrypt')
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Opportunity(db.Model):
    """Opportunity model"""
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.JSON, nullable=False)  # Store as JSON array
    category = db.Column(db.String(50), nullable=False)
    future_opportunities = db.Column(db.Text, nullable=False)
    max_applicants = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Key linking to the Admin table
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False, index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'duration': self.duration,
            'start_date': self.start_date,
            'description': self.description,
            'skills': self.skills,
            'category': self.category,
            'future_opportunities': self.future_opportunities,
            'max_applicants': self.max_applicants,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
