from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import models, database, auth
from routers import scan, complaints, officers, shops, legal, chat
from websocket_manager import manager
import traceback

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Packaged Commodity Compliance & Food Safety API",
    description="Backend for Smart India Hackathon 2026 Project (SIH26197)",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_details = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print(f"Global Exception: {error_details}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "traceback": error_details}
    )

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable GZip compression
app.add_middleware(GZipMiddleware, minimum_size=500)

app.include_router(scan.router)
app.include_router(complaints.router)
app.include_router(officers.router)
app.include_router(shops.router)
app.include_router(legal.router)
app.include_router(chat.router)

@app.on_event("startup")
def startup_event():
    # Setup default officer for testing
    db = database.SessionLocal()
    officer = db.query(models.User).filter(models.User.username == "officer1").first()
    if not officer:
        hashed_pw = auth.get_password_hash("password123")
        new_officer = models.User(username="officer1", hashed_password=hashed_pw, role="officer")
        db.add(new_officer)
        db.commit()
        
    # Seed chat rules if empty
    if db.query(models.ChatRule).count() == 0:
        initial_rules = [
            models.ChatRule(keywords="mrp,over price,extra,charge", response_text="<b>Rule 18(2) of Legal Metrology (Packaged Commodities) Rules, 2011:</b> No retail dealer or other person including manufacturer, packer, importer and wholesale dealer shall make any sale of any commodity in packed form at a price exceeding the retail sale price (MRP) thereof."),
            models.ChatRule(keywords="expiry,date,mfg", response_text="<b>Rule 6 of Legal Metrology Rules:</b> Every package must clearly display the month and year of manufacture or packing, as well as the 'Best Before' or 'Use By' date. If it is missing, you can file a complaint."),
            models.ChatRule(keywords="weight,quantity,less", response_text="<b>Rule 19:</b> Short weight or volume is a strict offense. The declared Net Quantity on the package must exactly match the contents inside."),
            models.ChatRule(keywords="complaint,file,report", response_text="You can click on the <b>'Complaints'</b> tab at the bottom of the app to officially report the violation to the authorities. Upload a photo of the receipt and the product."),
            models.ChatRule(keywords="adulteration,food,spoiled", response_text="<b>FSSAI Act 2006:</b> Selling unsafe or sub-standard food is a severe offense. Please take clear photos of the product and file a 'Food Safety' complaint via the app immediately.")
        ]
        db.add_all(initial_rules)
        db.commit()
        
    db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API. Go to /docs to view the Swagger documentation."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
