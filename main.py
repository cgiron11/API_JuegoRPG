from fastapi import FastAPI
from routes.clase_routes import router as clase_router
from routes.personaje_routes import router as personaje_router
from routes.inventario_routes import router as inventario_router
from routes.items_routes import router as items_router
from routes.Asigno_routes import router as asigno_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(clase_router)
app.include_router(personaje_router)
app.include_router(inventario_router)
app.include_router(items_router)
app.include_router(asigno_router)

