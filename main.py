from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

# NOTA: No utilizamos 'models.Base.metadata.create_all(bind=engine)'
# porque las tablas ya existen en Supabase. FastAPI solo consulta e inserta datos.

app = FastAPI(
    title="API de Catálogo de Productos - Supabase",
    version="1.0.0",
    description="Servicio Backend conectado a PostgreSQL en Supabase"
)

# Habilitar CORS para permitir peticiones desde React (Vercel) o navegador local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raíz informativo
@app.get("/", tags=["General"])
def root():
    return {
        "status": "online",
        "message": "API conectada exitosamente a Supabase",
        "docs": "/docs"
    }

# ==============================================================================
# 1. ENDPOINTS PRINCIPALES: Tabla 'products' (Tu tabla actual en Supabase)
# ==============================================================================
@app.get(
    "/api/v1/products",
    response_model=List[schemas.ProductResponse],
    tags=["Productos"]
)
def list_products(db: Session = Depends(get_db)):
    """
    Obtiene todos los productos de la tabla 'products' en Supabase.
    """
    try:
        return db.query(models.Product).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error consultando Supabase: {str(e)}"
        )

@app.post(
    "/api/v1/products",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Productos"]
)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo producto en la tabla 'products' de Supabase.
    """
    try:
        nuevo_producto = models.Product(**product.model_dump())
        db.add(nuevo_producto)
        db.commit()
        db.refresh(nuevo_producto)
        return nuevo_producto
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error guardando en Supabase: {str(e)}"
        )

@app.get(
    "/api/v1/products/{product_id}",
    response_model=schemas.ProductResponse,
    tags=["Productos"]
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto específico por su ID.
    """
    producto = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    return producto


# ==============================================================================
# 2. ENDPOINTS AVANZADOS: Catálogo Textil ('product_template')
# ==============================================================================
@app.get(
    "/api/v1/textile-templates",
    response_model=List[schemas.ProductTemplateResponse],
    tags=["Catálogo Textil ERP"]
)
def list_textile_templates(db: Session = Depends(get_db)):
    """
    Obtiene las fichas técnicas textiles de 'product_template' si ejecutaste el script completo.
    """
    try:
        return db.query(models.ProductTemplate).filter(models.ProductTemplate.active == True).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La tabla 'product_template' aún no ha sido creada en Supabase. Ejecuta el script SQL de la guía."
        )
