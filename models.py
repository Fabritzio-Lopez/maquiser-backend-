from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

# ==============================================================================
# MODELO PRINCIPAL: Catálogo Textil de Maquiser SRL (Tabla oficial en Supabase)
# ==============================================================================
class ProductTemplate(Base):
    """
    Mapeo de la tabla 'product_template' de Supabase.
    Contiene la ficha técnica textil (tipo de prenda, tela, composición, precios).
    """
    __tablename__ = "product_template"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    tipo_producto_textil = Column(String(50), nullable=True)
    composicion_textil = Column(String(100), nullable=True)
    tipo_tela = Column(String(100), nullable=True)
    gramaje = Column(Float, nullable=True)
    list_price = Column(Float, nullable=False, default=0.0)
    standard_price = Column(Float, nullable=True, default=0.0)
    sale_ok = Column(Boolean, default=True)
    purchase_ok = Column(Boolean, default=True)
    active = Column(Boolean, default=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==============================================================================
# MODELO SECUNDARIO: Tabla simple 'products' (por compatibilidad o pruebas MVP)
# ==============================================================================
class Product(Base):
    """
    Mapeo de la tabla básica 'products' (id, name, price, stock, image_url).
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    image_url = Column(String, nullable=True)
