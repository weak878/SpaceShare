from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Idea(db.Model):
    """Idea Model"""
    __tablename__ = 'ideas'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    likes_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tags = db.relationship('Tag', secondary='idea_tags', backref='ideas', lazy=True)
    collaborations = db.relationship('Collaboration', backref='idea', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='idea', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_details=False):
        """Convert idea to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'author': self.author.to_dict(),
            'likes_count': self.likes_count,
            'views_count': self.views_count,
            'tags': [tag.to_dict() for tag in self.tags],
            'collaborators_count': len(self.collaborations),
            'comments_count': len(self.comments),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_details:
            data['content'] = self.content
        return data
    
    def __repr__(self):
        return f'<Idea {self.title}>'

class Tag(db.Model):
    """Tag Model"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return f'<Tag {self.name}>'

# Association table for idea_tags
idea_tags = db.Table(
    'idea_tags',
    db.Column('idea_id', db.Integer, db.ForeignKey('ideas.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)
