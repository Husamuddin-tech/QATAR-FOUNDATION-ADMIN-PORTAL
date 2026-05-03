import os
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from config import config
from models import db, Admin
from routes import auth_bp, opportunities_bp

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, static_folder='sky', static_url_path='')
    
    # Load configuration
    app.config.from_object(config.get(config_name, config['development']))
    
    # Enable CORS for development
    CORS(app, supports_credentials=True, origins=['*'])
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(opportunities_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Serve the main HTML file
    @app.route('/', methods=['GET'])
    def index():
        return app.send_static_file('admin.html')
    
    # Basic route for testing
    @app.route('/api', methods=['GET'])
    def api_info():
        return {'message': 'CertifyMe Backend API is running'}, 200
    
    # Health check route
    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'healthy'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
