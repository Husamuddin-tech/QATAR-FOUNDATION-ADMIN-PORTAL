from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from models import db, Opportunity
from datetime import datetime

op_bp = Blueprint("opportunities", __name__, url_prefix="/api/opportunities")

ALLOWED = ["Technology", "Business", "Design", "Marketing", "Data Science", "Other"]


@op_bp.route("", methods=["GET"])
@login_required
def get_all():
    ops = Opportunity.query.filter_by(admin_id=current_user.id).all()
    return jsonify({"data": [o.to_dict() for o in ops]})


@op_bp.route("", methods=["POST"])
@login_required
def create():
    try:
        data = request.get_json()

        start_date = datetime.strptime(data["startDate"], "%Y-%m-%d").date()

        op = Opportunity(
            title=data["name"],
            duration=data["duration"],
            start_date=start_date,
            description=data["description"],
            skills=data["skills"],
            category=data["category"],
            future_opportunities=data["futureOpportunities"],
            max_applicants=data.get("maxApplicants"),
            admin_id=current_user.id,
        )

        db.session.add(op)
        db.session.commit()

        return jsonify({"data": op.to_dict()}), 201

    except:
        db.session.rollback()
        current_app.logger.error("Create error", exc_info=True)
        return jsonify({"error": "Server error"}), 500


@op_bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete(id):
    op = Opportunity.query.filter_by(id=id, admin_id=current_user.id).first()

    if not op:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(op)
    db.session.commit()

    return jsonify({"success": True})