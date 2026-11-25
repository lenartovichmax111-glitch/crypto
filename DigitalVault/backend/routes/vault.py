from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field
from routes.auth import current_user
from services.storage import connect

router = APIRouter()

class Note(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    ciphertext: str = Field(min_length=1, max_length=100000)

@router.get('/notes')
def notes(authorization: str = Header(default='')):
    uid = current_user(authorization)
    with connect() as db:
        rows = db.execute('SELECT id,title,ciphertext,created_at FROM notes WHERE user_id=? ORDER BY id DESC', (uid,)).fetchall()
    return [dict(row) for row in rows]

@router.post('/notes', status_code=201)
def add_note(note: Note, authorization: str = Header(default='')):
    uid = current_user(authorization)
    with connect() as db:
        cur = db.execute('INSERT INTO notes(user_id,title,ciphertext) VALUES (?,?,?)', (uid, note.title, note.ciphertext))
        return {'id': cur.lastrowid}

@router.delete('/notes/{note_id}')
def delete_note(note_id: int, authorization: str = Header(default='')):
    uid = current_user(authorization)
    with connect() as db:
        cur = db.execute('DELETE FROM notes WHERE id=? AND user_id=?', (note_id, uid))
        if not cur.rowcount:
            raise HTTPException(404, 'Note not found')
    return {'message': 'Deleted'}
