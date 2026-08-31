from fastapi import APIRouter, File, UploadFile
import pytesseract
from PIL import Image
import io
import schemas
from fastapi import Depends
import auth
import database
from sqlalchemy.orm import Session
import models
router = APIRouter(
    prefix="/api/scan",
    tags=["scan"]
)

@router.post("/analyze", response_model=schemas.ScanResult)
async def analyze_label(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # Read the uploaded image
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    
    # Perform OCR using pytesseract
    try:
        extracted_text = pytesseract.image_to_string(image)
    except Exception as e:
        extracted_text = ""
        
    if not extracted_text or not extracted_text.strip():
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Please scan a valid product label. No text was detected.")
        
    import re
    text_lower = extracted_text.lower()
    
    # Rule-Based Engine for Legal Metrology (Packaged Commodities) Rules, 2011
    # 1. Manufacturer / Packer Details
    has_manufacturer = bool(re.search(r'(manufactured|packed|marketed|mktd|mfd)\s*(by|for)?', text_lower))
    
    # 2. Net Quantity (Checking for standard units: g, kg, ml, L, unit, piece, U, N)
    has_qty = bool(re.search(r'(net\s*(wt\.?|weight|qty|quantity)|vol\.?|volume)?\s*:?\s*\d+(\.\d+)?\s*(g|kg|ml|l|ltr|pcs|pieces?|units?|u|n)\b', text_lower))
    
    # 3. Month & Year of Manufacture/Packaging/Import
    has_date = bool(re.search(r'(mfg|pkd|manufactured|packed|use\s*by|exp|expiry)\s*(date|d)?\s*:?\s*\d{1,4}[/\-\.]\d{1,4}([/\-\.]\d{1,4})?', text_lower))
    
    # 4. MRP (inclusive of all taxes)
    has_mrp = bool(re.search(r'mrp\s*(rs\.?|₹|inr)?\s*:?\s*\d+(\.\d+)?', text_lower))
    
    # 5. Consumer Care Details
    has_consumer_care = bool(re.search(r'(consumer\s*care|customer\s*care|customercare|feedback|complaints|toll\s*free|email|ph\.?|tel\.?)', text_lower))
    
    missing_fields = []
    if not has_manufacturer: missing_fields.append("Manufacturer/Packer Details")
    if not has_qty: missing_fields.append("Net Quantity")
    if not has_date: missing_fields.append("Mfg/Expiry Date")
    if not has_mrp: missing_fields.append("MRP")
    if not has_consumer_care: missing_fields.append("Consumer Care Info")
    
    is_compliant = len(missing_fields) == 0
    
    details_msg = "Compliant with Legal Metrology (Packaged Commodities) Rules."
    if not is_compliant:
        details_msg = f"Non-Compliant. Missing: {', '.join(missing_fields)}."
    
    import models
    # Food Safety check using Supabase database
    found_harmful = []
    
    ingredients = db.query(models.Ingredient).all()
    
    for ing in ingredients:
        matched = False
        # Check by Common Name
        if ing.common_name and ing.common_name.lower() in text_lower:
            matched = True
            
        # Check by INS Code
        if not matched and ing.ins_code:
            codes = [c.strip().lower() for c in ing.ins_code.split('/')]
            for c in codes:
                if c and c in text_lower:
                    matched = True
                    break
                    
        if matched and ing.risk_level in ["Caution", "Harmful"]:
            alert_msg = f"{ing.common_name} ({ing.risk_level})"
            if ing.health_concern:
                alert_msg += f" - {ing.health_concern}"
            found_harmful.append(alert_msg)
    
    health_score = "A"
    if len(found_harmful) > 0:
        health_score = "C" if len(found_harmful) > 1 else "B"

    return schemas.ScanResult(
        extracted_text=extracted_text,
        legal_metrology={
            "is_compliant": is_compliant,
            "details": details_msg
        },
        food_safety={
            "health_score": health_score,
            "harmful_ingredients": found_harmful
        }
    )

@router.get("/barcode/{barcode}", dependencies=[Depends(auth.verify_api_signature), Depends(auth.verify_captcha)])
def scan_barcode(barcode: str):
    import urllib.request
    import json
    
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'GrahakKavach/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
        if data.get('status') == 1:
            product = data.get('product', {})
            return {
                "found": True,
                "product_name": product.get('product_name', 'Unknown'),
                "brand": product.get('brands', 'Unknown'),
                "ingredients_text": product.get('ingredients_text', ''),
                "nutriscore_grade": product.get('nutriscore_grade', 'unknown').upper(),
                "nova_group": product.get('nova_group', 'unknown'),
                "image_url": product.get('image_url', '')
            }
        else:
            return {"found": False, "message": "Product not found in Open Food Facts database."}
    except Exception as e:
        return {"found": False, "message": f"Error verifying barcode: {str(e)}"}
