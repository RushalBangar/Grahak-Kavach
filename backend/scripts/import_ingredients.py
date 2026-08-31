import pandas as pd
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
import models
import math

def import_data():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    excel_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Ingredients_500_Products (1).xlsx')
    print(f"Reading {excel_path}...")
    
    df = pd.read_excel(excel_path)
    
    # Delete existing data if needed or just count
    if db.query(models.Ingredient).count() > 0:
        print("Data already exists in the database. Deleting old data...")
        db.query(models.Ingredient).delete()
        db.commit()
    
    ingredients = []
    for index, row in df.iterrows():
        # Handle nan values
        def clean_val(val):
            if pd.isna(val) or val == 'NaN':
                return None
            return str(val).strip()

        ins_code = clean_val(row.get('INS/E Code'))
        common_name = clean_val(row.get('Common Name'))
        
        # Skip if both are null
        if not ins_code and not common_name:
            continue
            
        ingredient = models.Ingredient(
            ins_code=ins_code,
            common_name=common_name,
            category=clean_val(row.get('Category')),
            risk_level=clean_val(row.get('Risk Level')),
            legal_status=clean_val(row.get('Legal Status in India')),
            health_concern=clean_val(row.get('Health Concern')),
            commonly_found_in=clean_val(row.get('Commonly Found In')),
            source=clean_val(row.get('Source'))
        )
        ingredients.append(ingredient)
    
    print(f"Inserting {len(ingredients)} ingredients into database...")
    db.add_all(ingredients)
    db.commit()
    print("Migration complete!")
    db.close()

if __name__ == "__main__":
    import_data()
