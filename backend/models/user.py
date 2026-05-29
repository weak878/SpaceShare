from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import jwt

db = SQLAlchemy()

class User(db.Model):
    """User Model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ideas = db.relationship('Idea', backref='author', lazy=True, cascade='all, delete-orphan')
    collaborations = db.relationship('Collaboration', backref='user', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def to_dict(self, include_email=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat(),
            'ideas_count': len(self.ideas)
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'
