import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
import models
from routers.chat import chat_endpoint
import schemas

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Seed database
if db.query(models.ChatRule).count() == 0:
    initial_rules = [
        models.ChatRule(keywords="mrp,over price,extra,charge", response_text="<b>Rule 18(2) of Legal Metrology (Packaged Commodities) Rules, 2011:</b> No retail dealer or other person including manufacturer, packer, importer and wholesale dealer shall make any sale of any commodity in packed form at a price exceeding the retail sale price (MRP) thereof."),
    ]
    db.add_all(initial_rules)
    db.commit()

query = schemas.ChatQuery(message="They charged me over mrp")
response = chat_endpoint(query, db)
print("Response:", response)

db.close()
