from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Collaboration(db.Model):
    """Collaboration Model - Users joining ideas"""
    __tablename__ = 'collaborations'
    
    ROLE_CHOICES = ['contributor', 'reviewer', 'lead']
    STATUS_CHOICES = ['pending', 'active', 'completed', 'cancelled']
    
    id = db.Column(db.Integer, primary_key=True)
    idea_id = db.Column(db.Integer, db.ForeignKey('ideas.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    role = db.Column(db.String(20), default='contributor', nullable=False)
    status = db.Column(db.String(20), default='active', nullable=False)
    contribution = db.Column(db.Text, nullable=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'idea_id': self.idea_id,
            'user': self.user.to_dict(),
            'role': self.role,
            'status': self.status,
            'contribution': self.contribution,
            'joined_at': self.joined_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Collaboration {self.user.username} on Idea {self.idea_id}>'
