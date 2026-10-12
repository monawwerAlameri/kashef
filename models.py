import json
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def utc_now():
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")        # user | pharmacist | admin
    is_active_user = db.Column(db.Boolean, default=True)
    font_size_pref = db.Column(db.String(20), default="normal")  # normal | medium | large | xlarge
    preferred_lang = db.Column(db.String(10), default="ar")
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    
    history = db.relationship("AnalysisHistory", foreign_keys="AnalysisHistory.user_id", backref="user", cascade="all, delete-orphan")
    feedbacks = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_pharmacist(self):
        return self.role == "pharmacist" or self.role == "admin"


class Medicine(db.Model):
    __tablename__ = "medicines"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    generic_name = db.Column(db.String(150))
    category = db.Column(db.String(100), default="General")
    description = db.Column(db.Text)
    source = db.Column(db.String(50), default="verified_catalog")  # verified_catalog | ocr_extracted
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    dosages = db.relationship("Dosage", backref="medicine", cascade="all, delete-orphan")
    warnings = db.relationship("MedWarning", backref="medicine", cascade="all, delete-orphan")
    qr_codes = db.relationship("QRCode", backref="medicine", cascade="all, delete-orphan")


class Dosage(db.Model):
    __tablename__ = "dosages"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(100))
    timing = db.Column(db.String(100))
    medicine_id = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=False)


class MedWarning(db.Model):
    __tablename__ = "warnings"
    id = db.Column(db.Integer, primary_key=True)
    side_effects = db.Column(db.Text)
    precautions = db.Column(db.Text)
    medicine_id = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=False)


class QRCode(db.Model):
    __tablename__ = "qr_codes"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), index=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=False)


class AnalysisHistory(db.Model):
    __tablename__ = "analysis_history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=True)
    extracted_text = db.Column(db.Text)
    result_json = db.Column(db.Text)
    detected_lang = db.Column(db.String(20), default="ara+eng")
    status = db.Column(db.String(30), default="completed")  # completed | needs_review | pharmacist_verified
    pharmacist_notes = db.Column(db.Text, nullable=True)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now, index=True)

    medicine = db.relationship("Medicine")
    reviewer = db.relationship("User", foreign_keys=[reviewed_by_id])

    @property
    def result(self):
        try:
            return json.loads(self.result_json) if self.result_json else None
        except ValueError:
            return None


class Feedback(db.Model):
    __tablename__ = "feedbacks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    category = db.Column(db.String(50), default="general")  # ocr_issue | parsing_error | suggestion | general
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="new")       # new | in_review | resolved
    admin_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now, index=True)


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    actor_name = db.Column(db.String(100), default="System")
    action = db.Column(db.String(50), nullable=False)     # role_changed | user_blocked | med_created | med_updated | med_deleted | setting_changed
    target_type = db.Column(db.String(50))                # user | medicine | setting | history
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utc_now, index=True)

    actor = db.relationship("User", foreign_keys=[actor_id])


class SystemSetting(db.Model):
    __tablename__ = "system_settings"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(60), unique=True, nullable=False, index=True)
    value = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
