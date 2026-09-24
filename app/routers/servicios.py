from fastapi import APIRouter, HTTPException, Depends
from ..database import get_connection
from ..models import ServicioCreate
from ..auth import obtener_usuario_actual

router = APIRouter(prefix="/servicios", tags=["Servicios"])

@router.get("/", dependencies=[Depends(obtener_usuario_actual)])
def listar_servicios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, precio FROM servicios ORDER BY id")
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

@router.post("/", dependencies=[Depends(obtener_usuario_actual)])
def crear_servicio(servicio: ServicioCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO servicios (nombre, precio) VALUES (%s, %s) RETURNING id",
        (servicio.nombre, servicio.precio)
    )
    nuevo_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return {"mensaje": "Servicio creado", "id": nuevo_id}

@router.put("/{id}", dependencies=[Depends(obtener_usuario_actual)])
def actualizar_servicio(id: int, servicio: ServicioCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE servicios SET nombre = %s, precio = %s WHERE id = %s",
        (servicio.nombre, servicio.precio, id)
    )
    filas = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if filas == 0:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"mensaje": "Servicio actualizado"}

@router.delete("/{id}", dependencies=[Depends(obtener_usuario_actual)])
def eliminar_servicio(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM servicios WHERE id = %s", (id,))
    filas = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if filas == 0:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"mensaje": "Servicio eliminado"}