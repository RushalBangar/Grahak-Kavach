from fastapi import APIRouter, File, UploadFile
import pytesseract
from PIL import Image
import io
from .. import schemas

router = APIRouter(
    prefix="/api/scan",
    tags=["scan"]
)

@router.post("/analyze", response_model=schemas.ScanResult)
async def analyze_label(file: UploadFile = File(...)):
    # Read the uploaded image
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    
    # Perform OCR using pytesseract
    try:
        extracted_text = pytesseract.image_to_string(image)
    except Exception as e:
        extracted_text = "OCR Failed or Tesseract not installed."
        
    # TODO: In a production app, implement real NLP / AI logic to parse the text.
    # For now, we mock the analysis based on whether certain keywords appear.
    
    text_lower = extracted_text.lower()
    
    # Mocked Legal Metrology check
    has_mrp = "mrp" in text_lower or "rs" in text_lower
    has_qty = "net qty" in text_lower or "net weight" in text_lower or "ml" in text_lower or "g" in text_lower
    has_date = "mfg" in text_lower or "date" in text_lower or "exp" in text_lower
    
    is_compliant = has_mrp and has_qty and has_date
    
    # Mocked Food Safety check
    # Check for some common harmful ingredients in our mocked database
    harmful_db = ["tartrazine", "msg", "high fructose corn syrup", "aspartame"]
    found_harmful = [ing for ing in harmful_db if ing in text_lower]
    
    health_score = "A"
    if len(found_harmful) > 0:
        health_score = "C" if len(found_harmful) > 1 else "B"

    return schemas.ScanResult(
        extracted_text=extracted_text,
        legal_metrology={
            "is_compliant": is_compliant,
            "details": f"Found MRP: {has_mrp}, Qty: {has_qty}, Date: {has_date}"
        },
        food_safety={
            "health_score": health_score,
            "harmful_ingredients": found_harmful
        }
    )
