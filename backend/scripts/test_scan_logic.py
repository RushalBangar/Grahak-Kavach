import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
import models

def test_scan():
    db = SessionLocal()
    
    text_lower = "ingredients: sugar, water, tartrazine, and e102."
    
    ingredients = db.query(models.Ingredient).all()
    print(f"Total ingredients in DB: {len(ingredients)}")
    
    found_harmful = []
    
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
                    
        if matched:
            print(f"Matched {ing.common_name} with risk {ing.risk_level}")
            if ing.risk_level in ["Caution", "Danger"]:
                alert_msg = f"{ing.common_name} ({ing.risk_level})"
                if ing.health_concern:
                    alert_msg += f" - {ing.health_concern}"
                found_harmful.append(alert_msg)
                
    print(f"Harmful found: {found_harmful}")
    
if __name__ == "__main__":
    test_scan()
