import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, 'Password must be at least 6 characters'
    
    if not re.search(r'[a-z]', password):
        return False, 'Password must contain lowercase letters'
    
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain uppercase letters'
    
    if not re.search(r'[0-9]', password):
        return False, 'Password must contain numbers'
    
    return True, 'Password is valid'

def validate_username(username):
    """Validate username"""
    if len(username) < 3:
        return False, 'Username must be at least 3 characters'
    
    if len(username) > 30:
        return False, 'Username must be less than 30 characters'
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, 'Username can only contain letters, numbers, underscores and hyphens'
    
    return True, 'Username is valid'
