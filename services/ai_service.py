"""AI Analysis component for Kashef.
Extracts structured, verified pharmaceutical details from bilingual Arabic & English medicine packaging text.
Complies with clinical safety standards: No hallucinated diagnoses, no invented dosages.
"""
import re

AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

KW = {
    "dosage": [
        "الجرعة", "جرعة", "قرص", "أقراص", "اقراص", "كبسول", "كبسولات", "ملعقة", "شراب",
        "dose", "dosage", "tablet", "tablets", "capsule", "capsules", "every", "daily",
        "times a day", "hours", "ساعات", "يوميا", "يومياً", "مرات", "البالغين", "الأطفال",
        "adults", "children", "drops", "نقط", "مل", "ml", "mg"
    ],
    "warnings": [
        "تحذير", "تحذيرات", "لا تتجاوز", "لا تأخذ", "لا تستخدم", "خطر", "موانع الاستعمال", "موانع الاستخدام",
        "warning", "warnings", "do not exceed", "do not take", "do not use", "overdose", "contraindication",
        "جرعة زائدة", "يحظر", "توقف عن الاستخدام"
    ],
    "precautions": [
        "احتياط", "احتياطات", "استشر", "راجع", "حامل", "الحمل", "الرضاعة", "مرضى", "كبد", "كلى", "ضغط", "سكر",
        "تجنب", "كحول", "قيادة", "consult", "precaution", "precautions", "pregnant", "pregnancy",
        "breastfeeding", "nursing", "liver", "kidney", "avoid", "alcohol", "driving", "doctor", "physician", "طبيب", "صيدلي"
    ],
    "side_effects": [
        "آثار جانبية", "اعراض جانبية", "أعراض جانبية", "تأثيرات جانبية", "حساسية", "غثيان", "طفح", "دوخة", "نعاس", "صداع",
        "side effect", "side effects", "adverse", "allergic", "allergy", "nausea", "rash", "dizziness", "drowsiness", "headache"
    ],
    "storage": [
        "يحفظ", "حفظ", "درجة حرارة", "مكان جاف", "بعيدا عن متناول الأطفال", "بعيداً عن الضوء", "أشعة الشمس",
        "store", "storage", "keep in", "keep out of reach of children", "cool dry place", "below 25", "below 30", "°c", "celsius"
    ],
    "purpose": [
        "يستخدم", "دواعي الاستعمال", "دواعي الاستخدام", "لعلاج", "مسكن", "خافض", "للحمى", "للحرارة", "للألم", "لتخفيف", "مضاد",
        "used for", "indicated for", "indication", "indications", "relief of", "relieves", "treatment of", "pain", "fever", "headache", "anti-inflammatory", "antibiotic"
    ],
}

STRENGTH_PATTERN = re.compile(r"(\b\d+(?:[.,]\d+)?\s*(?:mg|mcg|g|ml|iu|مجم|ملغ|ملغم|مج|جم|غرام|مل)\b)", re.I)
TIMING_PATTERN = re.compile(r"(كل\s*\d+\s*(?:ساعات|ساعة)|every\s*\d+\s*hours?|\d+\s*(?:مرات|مرة)\s*(?:في|ب)?\s*(?:اليوم|يوميا|يومياً)|\d+\s*times?\s*(?:a|per)\s*day|once daily|twice daily|three times daily|قبل الأكل|بعد الأكل|مع الطعام|before meals?|after meals?|with food)", re.I)
AMOUNT_PATTERN = re.compile(r"(\d+\s*(?:إلى|الى|-|to)\s*\d+\s*(?:أقراص|اقراص|قرص|tablets?|capsules?)|(?:\d+)\s*(?:tablets?|capsules?|أقراص|اقراص|قرص|كبسولة|ملعقة|teaspoon|مل|ml)|قرصين|قرص واحد)", re.I)

COMMON_ACTIVE_SUBSTANCES = [
    ("Paracetamol", ["paracetamol", "acetaminophen", "باراسيتامول", "اسيتامينوفين"]),
    ("Ibuprofen", ["ibuprofen", "إيبوبروفين", "ايبوبروفين"]),
    ("Amoxicillin", ["amoxicillin", "أموكسيسيلين", "اموكسيسيلين"]),
    ("Cetirizine", ["cetirizine", "سيتريزين"]),
    ("Omeprazole", ["omeprazole", "أوميبرازول", "اوميبرازول"]),
    ("Metformin", ["metformin", "ميتفورمين"]),
    ("Aspirin", ["aspirin", "أسبرين", "اسبرين"]),
    ("Loratadine", ["loratadine", "لوراتادين"]),
    ("Azithromycin", ["azithromycin", "أزيثروميسين", "ازيثروميسين"]),
    ("Pantoprazole", ["pantoprazole", "بانتوبرازول"])
]

def _clean_lines(text):
    out = []
    normalized = text.translate(AR_DIGITS)
    for ln in re.split(r"[\n\r]+|(?<=[.؛;!])\s+", normalized):
        ln = ln.strip(" -•*.:\t\r\n")
        if len(ln) >= 2:
            out.append(ln)
    return out

def _matches_any(line, category):
    lower_line = line.lower()
    return any(keyword.lower() in lower_line for keyword in KW[category])

def analyze_text(text):
    """
    Analyzes raw packaging text and returns structured medical cards.
    Missing elements are explicitly flagged as empty / not detected.
    """
    lines = _clean_lines(text or "")
    
    result = {
        "name": "",
        "active_ingredient": "",
        "strength": "",
        "purpose": "",
        "dosage_amount": "",
        "timing": "",
        "dosage_lines": [],
        "instructions": [],
        "warnings": [],
        "precautions": [],
        "side_effects": [],
        "storage": [],
        "found_any": False,
        "source": "packaging_ocr",
        "completeness": 0
    }

    if not lines:
        return result

    joined_text = " ".join(lines)
    lower_joined = joined_text.lower()

    # 1. Identify Active Ingredient
    for generic_name, synonyms in COMMON_ACTIVE_SUBSTANCES:
        if any(syn in lower_joined for syn in synonyms):
            result["active_ingredient"] = generic_name
            break

    # 2. Identify Strength
    strength_match = STRENGTH_PATTERN.search(joined_text)
    if strength_match:
        result["strength"] = strength_match.group(1).strip()

    # 3. Identify Name
    # Prioritize first lines containing strength or meaningful brand keywords
    for ln in lines[:6]:
        if STRENGTH_PATTERN.search(ln) and len(ln) < 80:
            result["name"] = ln
            break
    if not result["name"]:
        for ln in lines[:4]:
            if re.search(r"[A-Za-z\u0600-\u06FF]{3,}", ln) and len(ln) < 70:
                result["name"] = ln
                break
    if not result["name"] and lines:
        result["name"] = lines[0][:80]

    # 4. Classify each line
    for ln in lines:
        if ln == result["name"]:
            continue

        classified = False

        if _matches_any(ln, "warnings"):
            result["warnings"].append(ln)
            classified = True
        elif _matches_any(ln, "side_effects"):
            result["side_effects"].append(ln)
            classified = True
        elif _matches_any(ln, "precautions"):
            result["precautions"].append(ln)
            classified = True
        elif _matches_any(ln, "storage"):
            result["storage"].append(ln)
            classified = True
        elif _matches_any(ln, "purpose") and not result["purpose"]:
            result["purpose"] = ln
            classified = True
        elif _matches_any(ln, "dosage"):
            result["dosage_lines"].append(ln)
            classified = True

        if not classified and len(ln) > 15:
            # Check if it has valuable instructions
            result["instructions"].append(ln)

    # 5. Extract Timing & Dosage Amount via Regex
    timing_match = TIMING_PATTERN.search(joined_text)
    if timing_match:
        result["timing"] = timing_match.group(1).strip()

    amount_match = AMOUNT_PATTERN.search(joined_text)
    if amount_match:
        result["dosage_amount"] = amount_match.group(1).strip()

    # Deduplicate lists preserving order
    for key in ["warnings", "precautions", "side_effects", "storage", "instructions", "dosage_lines"]:
        seen = set()
        deduped = []
        for item in result[key]:
            if item not in seen:
                seen.add(item)
                deduped.append(item)
        result[key] = deduped

    # Calculate indicators
    has_details = any([
        result["dosage_lines"],
        result["dosage_amount"],
        result["timing"],
        result["warnings"],
        result["precautions"],
        result["side_effects"],
        result["purpose"],
        result["storage"]
    ])
    result["found_any"] = has_details

    # Calculate completeness score (0 to 100%)
    fields_checked = [
        bool(result["name"]),
        bool(result["strength"] or result["active_ingredient"]),
        bool(result["dosage_amount"] or result["timing"] or result["dosage_lines"]),
        bool(result["purpose"]),
        bool(result["warnings"] or result["precautions"]),
        bool(result["storage"])
    ]
    result["completeness"] = int((sum(fields_checked) / len(fields_checked)) * 100)

    return result
