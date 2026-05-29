from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import jwt
import os

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
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def generate_token(self):
        """Generate JWT token"""
        from config import Config
        payload = {
            'user_id': self.id,
            'email': self.email,
            'username': self.username
        }
        token = jwt.encode(
            payload,
            Config.JWT_SECRET_KEY,
            algorithm=Config.JWT_ALGORITHM
        )
        return token
    
    def to_dict(self, include_email=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat(),
            'ideas_count': len(self.ideas) if self.ideas else 0
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'

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
            'author': self.author.to_dict() if self.author else {},
            'likes_count': self.likes_count,
            'views_count': self.views_count,
            'tags': [tag.to_dict() for tag in self.tags] if self.tags else [],
            'collaborators_count': len(self.collaborations) if self.collaborations else 0,
            'comments_count': len(self.comments) if self.comments else 0,
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

class Collaboration(db.Model):
    """Collaboration Model"""
    __tablename__ = 'collaborations'
    
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
            'user': self.user.to_dict() if self.user else {},
            'role': self.role,
            'status': self.status,
            'contribution': self.contribution,
            'joined_at': self.joined_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Collaboration {self.user.username} on Idea {self.idea_id}>'

class Comment(db.Model):
    """Comment Model"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    idea_id = db.Column(db.Integer, db.ForeignKey('ideas.id'), nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    replies = db.relationship(
        'Comment',
        backref=db.backref('parent', remote_side=[id]),
        cascade='all, delete-orphan'
    )
    
    def to_dict(self, include_replies=True):
        data = {
            'id': self.id,
            'content': self.content,
            'author': self.author.to_dict() if self.author else {},
            'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_replies and self.replies:
            data['replies'] = [reply.to_dict(include_replies=False) for reply in self.replies]
        return data
    
    def __repr__(self):
        return f'<Comment by {self.author.username} on Idea {self.idea_id}>'

# Association table for idea_tags
idea_tags = db.Table(
    'idea_tags',
    db.Column('idea_id', db.Integer, db.ForeignKey('ideas.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)
