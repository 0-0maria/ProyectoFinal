from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_connection
from ..models import UsuarioRegistro, Token
from ..auth import hashear_password, verificar_password, crear_token
import psycopg 

router = APIRouter(tags=["Autenticación"])

@router.post("/registro")
def registrar_usuario(usuario: UsuarioRegistro):
    conn = get_connection()
    cur = conn.cursor()
    password_hash = hashear_password(usuario.password)
    try:
        cur.execute(
            "INSERT INTO usuarios (username, password_hash) VALUES (%s, %s) RETURNING id",
            (usuario.username, password_hash)
        )
        nuevo_id = cur.fetchone()["id"]
        conn.commit()
    except psycopg.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    finally:
        cur.close()
        conn.close()
    return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_id}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash FROM usuarios WHERE username = %s", (form_data.username,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    if not usuario or not verificar_password(form_data.password, usuario["password_hash"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token = crear_token({"sub": usuario["username"], "id": usuario["id"]})
    return {"access_token": token, "token_type": "bearer"}