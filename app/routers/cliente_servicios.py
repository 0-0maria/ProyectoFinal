from fastapi import APIRouter, HTTPException, Depends
from ..database import get_connection
from ..models import ClienteServicioCreate
from ..auth import obtener_usuario_actual

router = APIRouter(prefix="/cliente-servicios", tags=["Cliente Servicios"])

@router.get("/", dependencies=[Depends(obtener_usuario_actual)])
def listar_cliente_servicios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, idservicio, fecha, cliente FROM cliente_servicios ORDER BY id")
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

@router.post("/", dependencies=[Depends(obtener_usuario_actual)])
def crear_cliente_servicio(cs: ClienteServicioCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM servicios WHERE id = %s", (cs.idservicio,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="El servicio indicado no existe")
        
    cur.execute(
        "INSERT INTO cliente_servicios (idservicio, fecha, cliente) VALUES (%s, %s, %s) RETURNING id",
        (cs.idservicio, cs.fecha, cs.cliente)
    )
    nuevo_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return {"mensaje": "Solicitud de servicio registrada", "id": nuevo_id}

@router.put("/{id}", dependencies=[Depends(obtener_usuario_actual)])
def actualizar_cliente_servicio(id: int, cs: ClienteServicioCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE cliente_servicios SET idservicio = %s, fecha = %s, cliente = %s WHERE id = %s",
        (cs.idservicio, cs.fecha, cs.cliente, id)
    )
    filas = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if filas == 0:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"mensaje": "Registro actualizado"}

@router.delete("/{id}", dependencies=[Depends(obtener_usuario_actual)])
def eliminar_cliente_servicio(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cliente_servicios WHERE id = %s", (id,))
    filas = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if filas == 0:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"mensaje": "Registro eliminado"}