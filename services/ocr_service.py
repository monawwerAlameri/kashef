"""OCR Service for Kashef: Image enhancement and Arabic/English text extraction."""
import os
import shutil
from PIL import Image, ImageOps, ImageFilter

# Common Windows and Linux Tesseract paths
CANDIDATE_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\a\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
    "/usr/bin/tesseract",
    "/usr/local/bin/tesseract"
]

def find_tesseract(custom_cmd=""):
    """Locate tesseract binary if available."""
    if custom_cmd and os.path.isfile(custom_cmd):
        return custom_cmd
    path_in_env = shutil.which("tesseract")
    if path_in_env:
        return path_in_env
    for candidate in CANDIDATE_PATHS:
        if os.path.isfile(candidate):
            return candidate
    return None

def check_ocr_status(custom_cmd=""):
    """Check if OCR engine is operational and return diagnostic dict."""
    binary = find_tesseract(custom_cmd)
    available = binary is not None
    languages = []
    if available:
        try:
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = binary
            languages = pytesseract.get_languages(config="")
        except Exception:
            pass
    return {
        "available": available,
        "binary_path": binary or "Not detected",
        "languages": languages,
        "supports_arabic": "ara" in languages if languages else False,
        "supports_english": "eng" in languages if languages else False
    }

def enhance_image(img):
    """Enhance packaging photo contrast, sharpness, and resolution for OCR accuracy."""
    img = ImageOps.exif_transpose(img).convert("L")
    if max(img.size) < 1600:
        factor = 1600 / max(img.size)
        img = img.resize((int(img.width * factor), int(img.height * factor)), Image.Resampling.LANCZOS)
    img = ImageOps.autocontrast(img)
    return img.filter(ImageFilter.SHARPEN)

def extract_text(path, langs="ara+eng", tesseract_cmd=""):
    """
    Extracts text from image.
    Returns: (text, error_code, is_demo_fallback)
    error_code: None | 'ocr_missing' | 'bad_image' | 'no_text'
    """
    try:
        import pytesseract
    except ImportError:
        return "", "ocr_missing", False

    binary = find_tesseract(tesseract_cmd)
    if not binary:
        return "", "ocr_missing", False

    try:
        pytesseract.pytesseract.tesseract_cmd = binary
        with Image.open(path) as raw_img:
            img = enhance_image(raw_img)
            # Try combined languages, fallback to eng if ara missing
            try:
                text = pytesseract.image_to_string(img, lang=langs, config="--psm 6").strip()
            except pytesseract.TesseractError:
                text = pytesseract.image_to_string(img, lang="eng", config="--psm 6").strip()

        if not text:
            return "", "no_text", False

        return text, None, False

    except pytesseract.TesseractNotFoundError:
        return "", "ocr_missing", False
    except Exception:
        return "", "bad_image", False
