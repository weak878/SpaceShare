from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/spaceshare')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'message': 'SpaceShare Backend is running!'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
