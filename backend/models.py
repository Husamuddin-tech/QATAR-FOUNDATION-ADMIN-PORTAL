from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Admin(UserMixin, db.Model):
    """Admin user model"""

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(512), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Efficient relationship loading
    opportunities = db.relationship(
        "Opportunity",
        backref="creator",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    # -------------------------
    # 🔐 Auth Helpers
    # -------------------------
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password, method="scrypt")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # -------------------------
    # 📦 Serialization
    # -------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Admin {self.email}>"


class Opportunity(db.Model):
    """Opportunity model"""

    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)

    # FIXED: proper date type
    start_date = db.Column(db.Date, nullable=False, index=True)

    description = db.Column(db.Text, nullable=False)

    # Store as JSON array (validated in service layer)
    skills = db.Column(db.JSON, nullable=False)

    category = db.Column(db.String(50), nullable=False, index=True)

    future_opportunities = db.Column(db.Text, nullable=False)

    max_applicants = db.Column(db.Integer, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Foreign Key
    admin_id = db.Column(
        db.Integer,
        db.ForeignKey("admins.id"),
        nullable=False,
        index=True,
    )

    # -------------------------
    # 🔒 Constraints
    # -------------------------
    __table_args__ = (
        CheckConstraint(
            "category IN ('Technology','Business','Design','Marketing','Data Science','Other')",
            name="check_valid_category",
        ),
    )

    # -------------------------
    # 📦 Serialization
    # -------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "start_date": self.start_date.isoformat()
            if self.start_date
            else None,
            "description": self.description,
            "skills": self.skills,
            "category": self.category,
            "future_opportunities": self.future_opportunities,
            "max_applicants": self.max_applicants,
            "created_at": self.created_at.isoformat()
            if self.created_at
            else None,
            "updated_at": self.updated_at.isoformat()
            if self.updated_at
            else None,
        }

    def __repr__(self):
        return f"<Opportunity {self.title}>"