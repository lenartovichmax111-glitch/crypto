from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.vault import router as vault_router

app = FastAPI(title='DigitalVault API')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5500','http://127.0.0.1:5500'], allow_credentials=False, allow_methods=['*'], allow_headers=['*'])
app.include_router(auth_router, prefix='/api')
app.include_router(vault_router, prefix='/api')
