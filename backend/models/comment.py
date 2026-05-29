from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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
    
    # Self-referential relationship for replies
    replies = db.relationship(
        'Comment',
        backref=db.backref('parent', remote_side=[id]),
        cascade='all, delete-orphan'
    )
    
    def to_dict(self, include_replies=True):
        data = {
            'id': self.id,
            'content': self.content,
            'author': self.author.to_dict(),
            'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_replies and self.replies:
            data['replies'] = [reply.to_dict(include_replies=False) for reply in self.replies]
        return data
    
    def __repr__(self):
        return f'<Comment by {self.author.username} on Idea {self.idea_id}>'
