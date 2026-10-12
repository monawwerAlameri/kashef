import os
import json
import uuid
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, g, abort, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from models import (
    db, User, Medicine, Dosage, MedWarning,
    AnalysisHistory, Feedback, AuditLog, SystemSetting
)
from translations import TRANSLATIONS
from services.ocr_service import extract_text, check_ocr_status
from services.ai_service import analyze_text

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
db.init_app(app)

# ==============================================================================
# Helper Functions & Context Processors
# ==============================================================================

def get_lang():
    if g.get("user") and g.user.preferred_lang:
        return g.user.preferred_lang
    return session.get("lang", "ar")

def get_font_size():
    if g.get("user") and g.user.font_size_pref:
        return g.user.font_size_pref
    return session.get("font_size", "normal")

@app.context_processor
def inject_globals():
    lang = get_lang()
    font_size = get_font_size()
    tr = TRANSLATIONS.get(lang, TRANSLATIONS["ar"])
    
    # Safe translator fallback to English if missing in Arabic
    def t(key):
        return tr.get(key, TRANSLATIONS["en"].get(key, key))

    pending_reviews_count = 0
    new_feedbacks_count = 0
    if g.get("user"):
        if g.user.is_pharmacist:
            pending_reviews_count = AnalysisHistory.query.filter_by(status="needs_review").count()
        if g.user.is_admin:
            new_feedbacks_count = Feedback.query.filter_by(status="new").count()

    return dict(
        t=t,
        lang=lang,
        dir="rtl" if lang == "ar" else "ltr",
        user=g.get("user"),
        font_size=font_size,
        pending_reviews_count=pending_reviews_count,
        new_feedbacks_count=new_feedbacks_count
    )

@app.before_request
def load_user():
    uid = session.get("uid")
    if uid:
        user = db.session.get(User, uid)
        if user and user.is_active_user:
            g.user = user
        else:
            session.pop("uid", None)
            g.user = None
    else:
        g.user = None

def flash_t(key, category="info"):
    tr = TRANSLATIONS.get(get_lang(), TRANSLATIONS["ar"])
    flash(tr.get(key, TRANSLATIONS["en"].get(key, key)), category)

def log_audit(action, target_type, target_id=None, details=""):
    try:
        actor_id = g.user.id if g.get("user") else None
        actor_name = g.user.name if g.get("user") else "System"
        entry = AuditLog(
            actor_id=actor_id,
            actor_name=actor_name,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details
        )
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()

# ==============================================================================
# Role-Based Access Control (RBAC) Decorators
# ==============================================================================

def login_required(f):
    @wraps(f)
    def decorated_fn(*args, **kwargs):
        if not g.get("user"):
            flash_t("f_login_req", "warning")
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated_fn

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_fn(*args, **kwargs):
            if g.user.role not in allowed_roles and not g.user.is_admin:
                flash_t("f_denied", "danger")
                return redirect(url_for("dashboard"))
            return f(*args, **kwargs)
        return decorated_fn
    return decorator

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_fn(*args, **kwargs):
        if not g.user.is_admin:
            flash_t("f_denied", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated_fn

def pharmacist_required(f):
    @wraps(f)
    @login_required
    def decorated_fn(*args, **kwargs):
        if not g.user.is_pharmacist:
            flash_t("f_denied", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated_fn

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# ==============================================================================
# Internationalization & Display Preference Routes
# ==============================================================================

@app.route("/set-lang/<code>")
def set_lang(code):
    if code in TRANSLATIONS:
        session["lang"] = code
        if g.get("user"):
            g.user.preferred_lang = code
            db.session.commit()
    return redirect(request.referrer or url_for("index"))

@app.route("/set-font-size/<size>")
def set_font_size(size):
    if size in ["normal", "medium", "large", "xlarge"]:
        session["font_size"] = size
        if g.get("user"):
            g.user.font_size_pref = size
            db.session.commit()
    return redirect(request.referrer or url_for("index"))

# ==============================================================================
# Public & Information Pages
# ==============================================================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/help")
def help_page():
    return render_template("help.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        flash_t("f_saved", "info")
        return redirect(url_for("login"))
    return render_template("forgot_password.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name", "").strip() or (g.user.name if g.get("user") else "Guest")
        email = request.form.get("email", "").strip() or (g.user.email if g.get("user") else "")
        category = request.form.get("category", "general")
        message = request.form.get("message", "").strip()
        
        if not message:
            flash_t("f_empty_text", "warning")
            return redirect(url_for("feedback"))

        fb = Feedback(
            user_id=g.user.id if g.get("user") else None,
            name=name,
            email=email,
            category=category,
            message=message,
            status="new"
        )
        db.session.add(fb)
        db.session.commit()
        flash_t("feedback_success", "success")
        return redirect(url_for("feedback"))
    return render_template("feedback.html")

# ==============================================================================
# Authentication (Login / Register / Logout)
# ==============================================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if g.get("user"):
        if g.user.is_admin:
            return redirect(url_for("admin_dashboard"))
        elif g.user.is_pharmacist:
            return redirect(url_for("pharmacist_reviews"))
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash_t("f_login_failed", "danger")
        elif not user.is_active_user:
            flash_t("f_blocked", "danger")
        else:
            session["uid"] = user.id
            session["lang"] = user.preferred_lang
            session["font_size"] = user.font_size_pref
            log_audit("user_login", "user", user.id, f"User {user.email} logged in")
            
            if user.is_admin:
                return redirect(url_for("admin_dashboard"))
            elif user.is_pharmacist:
                return redirect(url_for("pharmacist_reviews"))
            return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if g.get("user"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        pw = request.form.get("password", "")
        pw_confirm = request.form.get("confirm", "")
        agreed = request.form.get("agree_terms")

        if not agreed:
            flash_t("f_denied", "warning")
        elif len(pw) < 6:
            flash_t("f_pw_short", "danger")
        elif pw != pw_confirm:
            flash_t("f_pw_mismatch", "danger")
        elif User.query.filter_by(email=email).first():
            flash_t("f_email_exists", "danger")
        else:
            new_user = User(
                name=name,
                email=email,
                password_hash=generate_password_hash(pw),
                role="user",
                preferred_lang=get_lang()
            )
            db.session.add(new_user)
            db.session.commit()
            log_audit("user_registered", "user", new_user.id, f"Registered: {email}")
            flash_t("f_registered", "success")
            return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    uid = session.pop("uid", None)
    if uid:
        log_audit("user_logout", "user", uid, "Logged out")
    flash_t("f_logged_out", "info")
    return redirect(url_for("index"))

# ==============================================================================
# Patient / User Application Area
# ==============================================================================

@app.route("/dashboard")
@login_required
def dashboard():
    user_scans = AnalysisHistory.query.filter_by(user_id=g.user.id)
    total = user_scans.count()
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    week_count = user_scans.filter(AnalysisHistory.created_at >= one_week_ago).count()
    recent_scans = user_scans.order_by(AnalysisHistory.created_at.desc()).limit(5).all()
    verified_meds_count = Medicine.query.count()
    last_scan = recent_scans[0] if recent_scans else None

    return render_template(
        "dashboard.html",
        total=total,
        week=week_count,
        recent=recent_scans,
        meds=verified_meds_count,
        last=last_scan
    )

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    ocr_diag = check_ocr_status(app.config.get("TESSERACT_CMD", ""))
    
    if request.method == "POST":
        file = request.files.get("image")
        if not file or not file.filename:
            flash_t("f_no_image", "warning")
            return redirect(url_for("upload"))

        if not allowed_file(file.filename):
            flash_t("f_invalid_file", "danger")
            return redirect(url_for("upload"))

        # Save temporary file with sanitized UUID
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        saved_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(saved_path)

        # Execute OCR extraction
        text, err_code, _ = extract_text(
            saved_path,
            langs=app.config.get("OCR_LANGS", "ara+eng"),
            tesseract_cmd=app.config.get("TESSERACT_CMD", "")
        )

        # Enforce Privacy Requirement R5: Delete image immediately after OCR
        if app.config.get("DELETE_IMAGE_AFTER_OCR", True) and os.path.exists(saved_path):
            try:
                os.remove(saved_path)
            except Exception:
                pass

        if err_code == "ocr_missing":
            flash_t("f_ocr_missing", "warning")
            # If OCR engine missing, provide safe demo fallback text so the pipeline is fully testable
            text = (
                "Panadol Extra 500 mg / 65 mg Tablets\n"
                "Paracetamol, Caffeine\n"
                "الجرعة: 1-2 قرص كل 4 إلى 6 ساعات عند اللزوم.\n"
                "تحذير: لا تتجاوز 8 أقراص خلال 24 ساعة. تجنب الاستخدام مع أدوية باراسيتامول أخرى.\n"
                "دواعي الاستعمال: لتسكين الصداع، آلام الأسنان، وخفض الحرارة.\n"
                "يحفظ في درجة حرارة أقل من 25 درجة مئوية بعيداً عن متناول الأطفال."
            )
            history_item = AnalysisHistory(
                user_id=g.user.id,
                extracted_text=text,
                detected_lang="demo_sample",
                status="completed"
            )
            db.session.add(history_item)
            db.session.commit()
            return redirect(url_for("extracted", hid=history_item.id))

        if err_code:
            flash_t("f_" + err_code, "danger")
            return redirect(url_for("upload"))

        if not text.strip():
            flash_t("f_no_text", "warning")
            return redirect(url_for("upload"))

        history_item = AnalysisHistory(
            user_id=g.user.id,
            extracted_text=text,
            detected_lang="tesseract_ocr",
            status="completed"
        )
        db.session.add(history_item)
        db.session.commit()
        return redirect(url_for("extracted", hid=history_item.id))

    return render_template("upload.html", ocr_diag=ocr_diag)

@app.route("/sample-scan/<sample_name>")
@login_required
def sample_scan(sample_name):
    """Safe pre-packaged medical packaging samples for instant testing."""
    samples = {
        "paracetamol": (
            "Paracetamol 500 mg Tablets\n"
            "باراسيتامول 500 مجم أقراص\n"
            "المادة الفعالة: Paracetamol 500mg\n"
            "دواعي الاستعمال: لتسكين الآلام الخفيفة والمتوسطة وخفض الحمى والصداع.\n"
            "الجرعة: قرص إلى قرصين كل 6 ساعات عند الحاجة. لا تتجاوز 8 أقراص يومياً.\n"
            "التحذيرات: لا تتناول أدوية أخرى تحتوي على الباراسيتامول في نفس الوقت تجنباً للتسمم الكبدي.\n"
            "الاحتياطات: استشر الطبيب لمرضى الكبد والكلى والحوامل.\n"
            "الآثار الجانبية: نادرة عند الالتزام بالجرعة، قد يحدث طفح جلدي تحسسي.\n"
            "يحفظ في مكان جاف وبارد تحت 25°C بعيداً عن متناول الأطفال."
        ),
        "amoxicillin": (
            "Amoxicillin 250 mg / 5 ml Oral Suspension\n"
            "أموكسيسيلين 250 مجم / 5 مل شراب معلق\n"
            "مضاد حيوي واسع المجال\n"
            "الجرعة: ملعقة 5 مل كل 8 ساعات لمدة 7 أيام حسب تعليمات الطبيب.\n"
            "تحذير: أكمل كورس العلاج كاملاً ولا تتوقف عند زوال الأعراض.\n"
            "الاحتياطات: يحظر استخدامه لمن يعانون من حساسية البنسلين.\n"
            "الآثار الجانبية: قد يسبب غثيان أو إسهال خفيف أو طفح جلدي.\n"
            "الحفظ: يحفظ المسحوق الجاف تحت 25 درجة مئوية، وبعد التحضير يحفظ في الثلاجة لمدة 7 أيام."
        )
    }
    
    text = samples.get(sample_name, samples["paracetamol"])
    item = AnalysisHistory(
        user_id=g.user.id,
        extracted_text=text,
        detected_lang="demo_verified_sample",
        status="completed"
    )
    db.session.add(item)
    db.session.commit()
    flash_t("f_saved", "success")
    return redirect(url_for("extracted", hid=item.id))

def get_own_history(hid):
    """Enforces horizontal authorization: users only access their own history."""
    item = db.session.get(AnalysisHistory, hid) or abort(404)
    if item.user_id != g.user.id and not g.user.is_admin and not g.user.is_pharmacist:
        abort(403)
    return item

@app.route("/extracted/<int:hid>")
@login_required
def extracted(hid):
    h = get_own_history(hid)
    return render_template("extracted.html", h=h)

@app.route("/analyze/<int:hid>", methods=["POST"])
@login_required
def analyze(hid):
    h = get_own_history(hid)
    text = request.form.get("text", "").strip()
    if not text:
        flash_t("f_empty_text", "warning")
        return redirect(url_for("extracted", hid=hid))

    h.extracted_text = text
    structured_result = analyze_text(text)
    h.result_json = json.dumps(structured_result, ensure_ascii=False)

    med_name = (structured_result.get("name") or "Unspecified Medicine")[:150]
    
    # Check if this medicine exists in catalog; link if so
    med = Medicine.query.filter_by(name=med_name).first()
    if not med and structured_result.get("found_any"):
        med = Medicine(
            name=med_name,
            generic_name=structured_result.get("active_ingredient", ""),
            description=structured_result.get("purpose", ""),
            source="ocr_extracted"
        )
        if structured_result.get("dosage_amount") or structured_result.get("timing"):
            med.dosages.append(Dosage(
                amount=structured_result.get("dosage_amount", ""),
                timing=structured_result.get("timing", "")
            ))
        if structured_result.get("side_effects") or structured_result.get("precautions"):
            med.warnings.append(MedWarning(
                side_effects="\n".join(structured_result.get("side_effects", [])),
                precautions="\n".join(structured_result.get("precautions", []))
            ))
        db.session.add(med)
        db.session.flush()

    if med:
        h.medicine_id = med.id

    db.session.commit()
    return redirect(url_for("result", hid=h.id))

@app.route("/result/<int:hid>")
@login_required
def result(hid):
    h = get_own_history(hid)
    if not h.result:
        return redirect(url_for("extracted", hid=hid))
    return render_template("result.html", h=h, r=h.result)

@app.route("/request-review/<int:hid>", methods=["POST"])
@login_required
def request_review(hid):
    h = get_own_history(hid)
    h.status = "needs_review"
    db.session.commit()
    flash_t("review_requested", "info")
    return redirect(url_for("result", hid=hid))

@app.route("/history")
@login_required
def history():
    q = request.args.get("q", "").strip()
    query = AnalysisHistory.query.filter_by(user_id=g.user.id)
    if q:
        query = query.filter(AnalysisHistory.extracted_text.ilike(f"%{q}%"))
    items = query.order_by(AnalysisHistory.created_at.desc()).all()
    return render_template("history.html", items=items, search_query=q)

@app.route("/history/<int:hid>/delete", methods=["POST"])
@login_required
def history_delete(hid):
    h = get_own_history(hid)
    db.session.delete(h)
    db.session.commit()
    log_audit("history_delete", "history", hid, f"Deleted scan record #{hid}")
    flash_t("f_deleted", "success")
    return redirect(request.referrer or url_for("history"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        lang_pref = request.form.get("preferred_lang", "ar")
        font_size = request.form.get("font_size_pref", "normal")
        new_password = request.form.get("new_password", "")

        if name:
            g.user.name = name
        if lang_pref in TRANSLATIONS:
            g.user.preferred_lang = lang_pref
            session["lang"] = lang_pref
        if font_size in ["normal", "medium", "large", "xlarge"]:
            g.user.font_size_pref = font_size
            session["font_size"] = font_size

        if new_password:
            if len(new_password) < 6:
                flash_t("f_pw_short", "danger")
                return redirect(url_for("profile"))
            g.user.password_hash = generate_password_hash(new_password)

        db.session.commit()
        flash_t("f_saved", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html")

# ==============================================================================
# Pharmacist Portal & Clinical Reviews
# ==============================================================================

@app.route("/pharmacist/reviews")
@pharmacist_required
def pharmacist_reviews():
    status_filter = request.args.get("status", "all")
    query = AnalysisHistory.query
    if status_filter == "pending":
        query = query.filter_by(status="needs_review")
    elif status_filter == "verified":
        query = query.filter_by(status="pharmacist_verified")
    
    items = query.order_by(AnalysisHistory.created_at.desc()).limit(100).all()
    return render_template("pharmacist/reviews.html", items=items, active_filter=status_filter)

@app.route("/pharmacist/review/<int:hid>", methods=["POST"])
@pharmacist_required
def pharmacist_submit_review(hid):
    h = db.session.get(AnalysisHistory, hid) or abort(404)
    status = request.form.get("status", "pharmacist_verified")
    notes = request.form.get("notes", "").strip()

    h.status = status
    h.pharmacist_notes = notes
    h.reviewed_by_id = g.user.id
    h.reviewed_at = datetime.now(timezone.utc)

    db.session.commit()
    log_audit("pharmacist_review", "history", hid, f"Pharmacist reviewed scan #{hid} with status {status}")
    flash_t("f_saved", "success")
    return redirect(request.referrer or url_for("pharmacist_reviews"))

# ==============================================================================
# Administration Control Panel & Sidebar Modules
# ==============================================================================

@app.route("/admin")
@admin_required
def admin_dashboard():
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    chart_data = [
        AnalysisHistory.query.filter(
            AnalysisHistory.created_at >= d,
            AnalysisHistory.created_at < d + timedelta(days=1)
        ).count()
        for d in days
    ]

    ocr_status = check_ocr_status(app.config.get("TESSERACT_CMD", ""))

    return render_template(
        "admin/dashboard.html",
        users_count=User.query.count(),
        scans_count=AnalysisHistory.query.count(),
        meds_count=Medicine.query.count(),
        today_scans=AnalysisHistory.query.filter(AnalysisHistory.created_at >= today).count(),
        open_feedbacks=Feedback.query.filter_by(status="new").count(),
        recent_scans=AnalysisHistory.query.order_by(AnalysisHistory.created_at.desc()).limit(6).all(),
        chart_labels=[d.strftime("%d/%m") for d in days],
        chart_data=chart_data,
        ocr_status=ocr_status
    )

@app.route("/admin/users")
@admin_required
def admin_users():
    q = request.args.get("q", "").strip()
    role_filter = request.args.get("role", "")
    query = User.query
    if q:
        query = query.filter((User.name.ilike(f"%{q}%")) | (User.email.ilike(f"%{q}%")))
    if role_filter:
        query = query.filter_by(role=role_filter)
    
    users = query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", items=users, search_query=q, role_filter=role_filter)

@app.route("/admin/users/<int:uid>/role", methods=["POST"])
@admin_required
def admin_user_change_role(uid):
    target_user = db.session.get(User, uid) or abort(404)
    new_role = request.form.get("role", "user")

    if target_user.id == g.user.id and new_role != "admin":
        flash_t("f_self", "warning")
        return redirect(url_for("admin_users"))

    if new_role in ["user", "pharmacist", "admin"]:
        old_role = target_user.role
        target_user.role = new_role
        db.session.commit()
        log_audit("role_change", "user", uid, f"Changed role of {target_user.email} from {old_role} to {new_role}")
        flash_t("f_saved", "success")

    return redirect(url_for("admin_users"))

@app.route("/admin/users/<int:uid>/toggle-active", methods=["POST"])
@admin_required
def admin_user_toggle_active(uid):
    target_user = db.session.get(User, uid) or abort(404)
    if target_user.id == g.user.id:
        flash_t("f_self", "warning")
        return redirect(url_for("admin_users"))

    target_user.is_active_user = not target_user.is_active_user
    db.session.commit()
    log_audit("status_change", "user", uid, f"Toggled active status for {target_user.email} to {target_user.is_active_user}")
    flash_t("f_saved", "success")
    return redirect(url_for("admin_users"))

@app.route("/admin/users/<int:uid>/delete", methods=["POST"])
@admin_required
def admin_user_delete(uid):
    target_user = db.session.get(User, uid) or abort(404)
    if target_user.id == g.user.id:
        flash_t("f_self", "warning")
        return redirect(url_for("admin_users"))

    user_email = target_user.email
    db.session.delete(target_user)
    db.session.commit()
    log_audit("user_delete", "user", uid, f"Permanently deleted user {user_email}")
    flash_t("f_deleted", "success")
    return redirect(url_for("admin_users"))

@app.route("/admin/medicines", methods=["GET", "POST"])
@admin_required
def admin_medicines():
    if request.method == "POST":
        f = request.form
        name = f.get("name", "").strip()
        generic = f.get("generic_name", "").strip()
        category = f.get("category", "General").strip()
        desc = f.get("description", "").strip()
        
        if not name:
            flash_t("f_empty_text", "warning")
            return redirect(url_for("admin_medicines"))

        m = Medicine(
            name=name,
            generic_name=generic,
            category=category,
            description=desc,
            source="verified_catalog"
        )
        if f.get("amount") or f.get("timing"):
            m.dosages.append(Dosage(amount=f.get("amount", ""), timing=f.get("timing", "")))
        if f.get("side_effects") or f.get("precautions"):
            m.warnings.append(MedWarning(side_effects=f.get("side_effects", ""), precautions=f.get("precautions", "")))
        
        db.session.add(m)
        db.session.commit()
        log_audit("med_create", "medicine", m.id, f"Added verified medicine: {m.name}")
        flash_t("f_saved", "success")
        return redirect(url_for("admin_medicines"))

    items = Medicine.query.order_by(Medicine.id.desc()).all()
    return render_template("admin/medicines.html", items=items)

@app.route("/admin/medicines/<int:mid>/edit", methods=["POST"])
@admin_required
def admin_medicine_edit(mid):
    m = db.session.get(Medicine, mid) or abort(404)
    f = request.form
    m.name = f.get("name", m.name).strip()
    m.generic_name = f.get("generic_name", m.generic_name).strip()
    m.category = f.get("category", m.category).strip()
    m.description = f.get("description", m.description).strip()

    if m.dosages:
        m.dosages[0].amount = f.get("amount", "")
        m.dosages[0].timing = f.get("timing", "")
    else:
        m.dosages.append(Dosage(amount=f.get("amount", ""), timing=f.get("timing", "")))

    if m.warnings:
        m.warnings[0].side_effects = f.get("side_effects", "")
        m.warnings[0].precautions = f.get("precautions", "")
    else:
        m.warnings.append(MedWarning(side_effects=f.get("side_effects", ""), precautions=f.get("precautions", "")))

    db.session.commit()
    log_audit("med_update", "medicine", mid, f"Updated medicine #{mid} {m.name}")
    flash_t("f_saved", "success")
    return redirect(url_for("admin_medicines"))

@app.route("/admin/medicines/<int:mid>/delete", methods=["POST"])
@admin_required
def admin_medicine_delete(mid):
    m = db.session.get(Medicine, mid) or abort(404)
    name = m.name
    AnalysisHistory.query.filter_by(medicine_id=mid).update({"medicine_id": None})
    db.session.delete(m)
    db.session.commit()
    log_audit("med_delete", "medicine", mid, f"Deleted medicine {name}")
    flash_t("f_deleted", "success")
    return redirect(url_for("admin_medicines"))

@app.route("/admin/analyses")
@app.route("/admin/history")
@admin_required
def admin_history():
    q = request.args.get("q", "").strip()
    query = AnalysisHistory.query
    if q:
        query = query.filter(AnalysisHistory.extracted_text.ilike(f"%{q}%"))
    items = query.order_by(AnalysisHistory.created_at.desc()).limit(300).all()
    return render_template("admin/history.html", items=items, search_query=q)

@app.route("/admin/feedback")
@admin_required
def admin_feedback():
    items = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template("admin/feedback.html", items=items)

@app.route("/admin/feedback/<int:fid>/status", methods=["POST"])
@admin_required
def admin_feedback_status(fid):
    fb = db.session.get(Feedback, fid) or abort(404)
    status = request.form.get("status", "resolved")
    admin_notes = request.form.get("admin_notes", "").strip()
    
    fb.status = status
    if admin_notes:
        fb.admin_notes = admin_notes
    db.session.commit()
    log_audit("feedback_status", "feedback", fid, f"Set feedback #{fid} to {status}")
    flash_t("f_saved", "success")
    return redirect(url_for("admin_feedback"))

@app.route("/admin/audit-log")
@admin_required
def admin_audit_log():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(200).all()
    return render_template("admin/audit_log.html", items=logs)

@app.route("/admin/settings", methods=["GET", "POST"])
@admin_required
def admin_settings():
    if request.method == "POST":
        for key in ["max_upload_size_mb", "allow_demo_fallback", "allow_guest_scan"]:
            val = request.form.get(key, "")
            setting = SystemSetting.query.filter_by(key=key).first()
            if not setting:
                setting = SystemSetting(key=key, value=val)
                db.session.add(setting)
            else:
                setting.value = val
        db.session.commit()
        log_audit("settings_update", "settings", None, "Updated system settings")
        flash_t("f_saved", "success")
        return redirect(url_for("admin_settings"))

    settings = {s.key: s.value for s in SystemSetting.query.all()}
    ocr_diag = check_ocr_status(app.config.get("TESSERACT_CMD", ""))
    return render_template("admin/settings.html", settings=settings, ocr_diag=ocr_diag)

# ==============================================================================
# Error Handlers
# ==============================================================================

@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", code=403, msg="Access Forbidden / غير مصرح بالوصول"), 403

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, msg="Page Not Found / الصفحة غير موجودة"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500, msg="Server Error / خطأ في الخادم"), 500

# ==============================================================================
# Database Seeder (Roles, Default Accounts, and Catalog)
# ==============================================================================

def seed_database():
    db.create_all()

    # 1. Admin Account
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        admin = User(
            name="System Admin",
            email=app.config.get("ADMIN_EMAIL", "admin@kashef.com"),
            role="admin",
            password_hash=generate_password_hash(app.config.get("ADMIN_PASSWORD", "Admin@123")),
            preferred_lang="ar"
        )
        db.session.add(admin)

    # 2. Pharmacist Account (Actor with specialized clinical access)
    pharma = User.query.filter_by(role="pharmacist").first()
    if not pharma:
        pharma = User(
            name="Dr. Sarah (Pharmacist)",
            email="pharmacist@kashef.com",
            role="pharmacist",
            password_hash=generate_password_hash("Pharma@123"),
            preferred_lang="ar"
        )
        db.session.add(pharma)

    # 3. Patient / General User Account
    user = User.query.filter_by(email="user@kashef.com").first()
    if not user:
        user = User(
            name="Mohammed Ali (Patient)",
            email="user@kashef.com",
            role="user",
            password_hash=generate_password_hash("User@123"),
            preferred_lang="ar",
            font_size_pref="normal"
        )
        db.session.add(user)

    # 4. Reference Medicines in Library
    if not Medicine.query.first():
        med1 = Medicine(
            name="Paracetamol 500 mg",
            generic_name="Paracetamol",
            category="Analgesic / Antipyretic",
            description="Relieves mild to moderate pain and reduces fever.",
            source="verified_catalog"
        )
        med1.dosages.append(Dosage(amount="1 to 2 tablets", timing="Every 4 to 6 hours as needed (Max 8 tablets/day)"))
        med1.warnings.append(MedWarning(
            side_effects="Rare allergic skin reactions. Safe at recommended doses.",
            precautions="Do not take with other paracetamol products; avoid alcohol; caution in severe liver or kidney impairment."
        ))
        db.session.add(med1)

        med2 = Medicine(
            name="Amoxicillin 500 mg",
            generic_name="Amoxicillin",
            category="Antibiotic (Penicillin group)",
            description="Used for bacterial infections of the respiratory tract, ear, and throat.",
            source="verified_catalog"
        )
        med2.dosages.append(Dosage(amount="1 capsule (500mg)", timing="Every 8 hours for 7-10 days"))
        med2.warnings.append(MedWarning(
            side_effects="Diarrhea, nausea, stomach upset, or skin rashes.",
            precautions="Strictly contraindicated in individuals allergic to penicillin. Complete full prescribed course."
        ))
        db.session.add(med2)

    db.session.commit()

with app.app_context():
    seed_database()

if __name__ == "__main__":
    app.run(debug=True)
