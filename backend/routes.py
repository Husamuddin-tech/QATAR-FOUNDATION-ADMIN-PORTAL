from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Admin, Opportunity
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
import secrets
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
opportunities_bp = Blueprint('opportunities', __name__, url_prefix='/api/opportunities')

# Store password reset tokens temporarily (in production, use Redis or database)
password_reset_tokens = {}

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength (minimum 8 characters)"""
    return len(password) >= 8

# ===== AUTHENTICATION ROUTES =====

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User signup - US-1.1"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')
        
        # Validation
        if not name or not email or not password or not confirm_password:
            return jsonify({'error': 'All fields are required'}), 400
        
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not validate_password(password):
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        # Check if email already exists
        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new admin
        admin = Admin(full_name=name, email=email)
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Account created successfully',
            'user': admin.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Signup failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login - US-1.2"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        remember_me = data.get('rememberMe', False)
        
        # Validation
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        admin = Admin.query.filter_by(email=email).first()
        
        # Generic error message to prevent email enumeration
        if not admin or not admin.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Login user
        login_user(admin, remember=remember_me)
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'user': admin.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/forgot', methods=['POST'])
def forgot_password():
    """Password reset request - US-1.3"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        email = data.get('email', '').strip()
        
        if not email or not is_valid_email(email):
            return jsonify({'error': 'Valid email is required'}), 400
        
        # Always return success to prevent email enumeration
        success_response = {
            'status': 'success',
            'message': 'If an account with this email exists, a password reset link has been sent.'
        }
        
        # Check if email exists
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            # Generate unique token with 1-hour expiration
            token = secrets.token_urlsafe(32)
            expiration_time = datetime.utcnow() + timedelta(hours=1)
            
            password_reset_tokens[token] = {
                'email': email,
                'admin_id': admin.id,
                'expires_at': expiration_time
            }
            
            # Log the reset link to console (in production, send via email)
            reset_link = f"http://localhost:5000/reset-password?token={token}"
            print(f"\n{'='*50}")
            print(f"PASSWORD RESET LINK for {email}:")
            print(f"{reset_link}")
            print(f"Valid for 1 hour until: {expiration_time}")
            print(f"{'='*50}\n")
        
        return jsonify(success_response), 200
        
    except Exception as e:
        return jsonify({'error': f'Password reset request failed: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout"""
    try:
        logout_user()
        return jsonify({
            'status': 'success',
            'message': 'Logged out successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': f'Logout failed: {str(e)}'}), 500


# ===== OPPORTUNITY ROUTES =====

@opportunities_bp.route('', methods=['GET'])
@login_required
def get_opportunities():
    """View all opportunities for current user - US-2.1"""
    try:
        # Query opportunities belonging to current user
        opportunities = Opportunity.query.filter_by(admin_id=current_user.id).all()
        
        output = [op.to_dict() for op in opportunities]
        
        return jsonify({
            'status': 'success',
            'data': output,
            'count': len(output)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch opportunities: {str(e)}'}), 500


@opportunities_bp.route('', methods=['POST'])
@login_required
def create_opportunity():
    """Add a new opportunity - US-2.2"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        # Required fields
        title = data.get('name', '').strip()
        duration = data.get('duration', '').strip()
        start_date = data.get('startDate', '').strip()
        description = data.get('description', '').strip()
        skills = data.get('skills', [])
        category = data.get('category', '').strip()
        future_opportunities = data.get('futureOpportunities', '').strip()
        max_applicants = data.get('maxApplicants')
        
        # Validation
        if not all([title, duration, start_date, description, category, future_opportunities]):
            return jsonify({'error': 'All required fields must be filled'}), 400
        
        if not isinstance(skills, list) or len(skills) == 0:
            return jsonify({'error': 'At least one skill is required'}), 400
        
        # Define allowed categories
        allowed_categories = ['Technology', 'Business', 'Design', 'Marketing', 'Healthcare', 'Education']
        if category not in allowed_categories:
            return jsonify({'error': f'Invalid category. Allowed: {", ".join(allowed_categories)}'}), 400
        
        try:
            max_applicants = int(max_applicants) if max_applicants else 0
        except (ValueError, TypeError):
            max_applicants = 0
        
        # Create new opportunity
        opportunity = Opportunity(
            title=title,
            duration=duration,
            start_date=start_date,
            description=description,
            skills=skills,
            category=category,
            future_opportunities=future_opportunities,
            max_applicants=max_applicants,
            admin_id=current_user.id
        )
        
        db.session.add(opportunity)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Opportunity created successfully',
            'data': opportunity.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create opportunity: {str(e)}'}), 500


@opportunities_bp.route('/<int:opp_id>', methods=['GET'])
@login_required
def get_opportunity_details(opp_id):
    """Get opportunity details - US-2.3"""
    try:
        opportunity = Opportunity.query.filter_by(
            id=opp_id,
            admin_id=current_user.id
        ).first()
        
        if not opportunity:
            return jsonify({'error': 'Opportunity not found'}), 404
        
        return jsonify({
            'status': 'success',
            'data': opportunity.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch opportunity: {str(e)}'}), 500


@opportunities_bp.route('/<int:opp_id>/edit', methods=['PUT', 'POST'])
@login_required
def edit_opportunity(opp_id):
    """Edit an opportunity - US-2.5"""
    try:
        opportunity = Opportunity.query.filter_by(
            id=opp_id,
            admin_id=current_user.id
        ).first()
        
        if not opportunity:
            return jsonify({'error': 'Opportunity not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        # Update fields
        if 'name' in data:
            opportunity.title = data.get('name', '').strip()
        if 'duration' in data:
            opportunity.duration = data.get('duration', '').strip()
        if 'startDate' in data:
            opportunity.start_date = data.get('startDate', '').strip()
        if 'description' in data:
            opportunity.description = data.get('description', '').strip()
        if 'skills' in data:
            skills = data.get('skills', [])
            if isinstance(skills, list) and len(skills) > 0:
                opportunity.skills = skills
        if 'category' in data:
            opportunity.category = data.get('category', '').strip()
        if 'futureOpportunities' in data:
            opportunity.future_opportunities = data.get('futureOpportunities', '').strip()
        if 'maxApplicants' in data:
            try:
                opportunity.max_applicants = int(data.get('maxApplicants', 0)) or 0
            except (ValueError, TypeError):
                pass
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Opportunity updated successfully',
            'data': opportunity.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update opportunity: {str(e)}'}), 500


@opportunities_bp.route('/<int:opp_id>', methods=['DELETE'])
@login_required
def delete_opportunity(opp_id):
    """Delete an opportunity - US-2.6"""
    try:
        opportunity = Opportunity.query.filter_by(
            id=opp_id,
            admin_id=current_user.id
        ).first()
        
        if not opportunity:
            return jsonify({'error': 'Opportunity not found'}), 404
        
        db.session.delete(opportunity)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Opportunity deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete opportunity: {str(e)}'}), 500
