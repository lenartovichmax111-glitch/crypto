import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pwdlib import PasswordHash
from services.storage import connect

router = APIRouter()
password_hash = PasswordHash.recommended()
SECRET = os.environ.get('JWT_SECRET')
if not SECRET:
    raise RuntimeError('Set JWT_SECRET environment variable before starting the server')

class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=200)

@router.post('/register', status_code=201)
def register(data: Credentials):
    try:
        with connect() as db:
            db.execute('INSERT INTO users(username,password_hash) VALUES (?,?)', (data.username, password_hash.hash(data.password)))
    except __import__('sqlite3').IntegrityError:
        raise HTTPException(409, 'Username already exists')
    return {'message': 'Account created'}

@router.post('/login')
def login(data: Credentials):
    with connect() as db:
        user = db.execute('SELECT * FROM users WHERE username=?', (data.username,)).fetchone()
    if not user or not password_hash.verify(data.password, user['password_hash']):
        raise HTTPException(401, 'Invalid credentials')
    token = jwt.encode({'sub': str(user['id']), 'exp': datetime.now(timezone.utc) + timedelta(minutes=30)}, SECRET, algorithm='HS256')
    return {'access_token': token, 'token_type': 'bearer'}

def current_user(authorization: str):
    if not authorization.startswith('Bearer '):
        raise HTTPException(401, 'Bearer token required')
    try:
        payload = jwt.decode(authorization[7:], SECRET, algorithms=['HS256'])
        return int(payload['sub'])
    except (jwt.PyJWTError, ValueError, KeyError):
        raise HTTPException(401, 'Invalid or expired token')
