from fastapi import FastAPI
from .database import crear_tablas
from .routers import auth_router, servicios, cliente_servicios

app = FastAPI(title="API Proyecto Final - Servicios", version="1.0.0")


crear_tablas()

# Incluir los routers
app.include_router(auth_router.router)
app.include_router(servicios.router)
app.include_router(cliente_servicios.router)

@app.get("/")
def inicio():
    return {"mensaje": "API de Servicios funcionando correctamente"}