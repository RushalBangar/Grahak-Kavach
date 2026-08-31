import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
import models

def seed_chat_rules():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    rules = [
        {
            "keywords": "mrp,price,cost,overcharge,extra money,more than mrp",
            "response_text": "<b>Rule 18(2) of Legal Metrology (Packaged Commodities) Rules, 2011:</b> No retail dealer or other person including manufacturer, packer, importer and wholesale dealer shall make any sale of any commodity in packed form at a price exceeding the retail sale price (MRP) thereof. If a shop charges you more than MRP, you can file a complaint in our app."
        },
        {
            "keywords": "weight,less weight,quantity,underweight,measure",
            "response_text": "Under the Legal Metrology Act, selling products with less weight than declared on the package is an offense. Please ensure the scale is zeroed before weighing, and if you suspect tampering, file a 'Legal Metrology' complaint using this app."
        },
        {
            "keywords": "expire,expired,use by,expiry date,spoiled,bad food,rotten,fungus",
            "response_text": "Selling expired food is a severe violation of the Food Safety and Standards Authority of India (FSSAI) regulations. Do not consume it. Please file a 'Food Safety' complaint immediately with a photo of the expiry date."
        },
        {
            "keywords": "complaint,complain,report,how to file,where to report",
            "response_text": "You can file a complaint right here in the Grahak Kavach app! Just go to the 'Complaints' tab, select the violation type (Legal Metrology or Food Safety), and submit the details along with any photos."
        },
        {
            "keywords": "adulteration,adulterated,mixed,impure,fake,duplicate",
            "response_text": "Food adulteration is strictly prohibited under the FSSAI Act, 2006. If you suspect your food is adulterated (e.g. water in milk, brick powder in spices), please file a Food Safety complaint. Authorities will collect samples for laboratory testing."
        },
        {
            "keywords": "hello,hi,hey,help,start,namaste",
            "response_text": "Hello! I am the Grahak Kavach AI Assistant. I can help you understand your rights regarding MRP, expiry dates, weights and measures, and food adulteration. Ask me a question!"
        }
    ]
    
    # Clear existing rules to prevent duplicates if run multiple times
    db.query(models.ChatRule).delete()
    
    for rule_data in rules:
        rule = models.ChatRule(**rule_data)
        db.add(rule)
        
    db.commit()
    print("Chat rules seeded successfully!")

if __name__ == "__main__":
    seed_chat_rules()
