from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import models, database, auth
from routers import scan, complaints, officers, shops
from websocket_manager import manager

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Packaged Commodity Compliance & Food Safety API",
    description="Backend for Smart India Hackathon 2026 Project (SIH26197)",
    version="1.0.0"
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
