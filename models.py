from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

# ==============================================================================
# 1. TABLA: res_partner (Clientes, Colegios, Proveedores y Contactos)
# ==============================================================================
class Partner(Base):
    __tablename__ = "res_partner"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    tipo_documento = Column(String(10), nullable=True) # 'nit', 'ci'
    numero_documento = Column(String(80), nullable=True)
    empresa_asociada = Column(String(255), nullable=True)
    es_cliente_uniformes = Column(Boolean, default=True)
    es_proveedor_textil = Column(Boolean, default=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    city = Column(String(120), nullable=True)
    street = Column(String(255), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==============================================================================
# 2. TABLA: product_template (Plantilla de Productos Textiles de Maquiser)
# ==============================================================================
class ProductTemplate(Base):
    __tablename__ = "product_template"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    tipo_producto_textil = Column(String(50), default="uniforme") # 'uniforme', 'tela', 'insumo', 'prenda_casual'
    composicion_textil = Column(String(255), nullable=True)
    tipo_tela = Column(String(50), nullable=True) # 'algodon', 'poliester', 'mezcla', 'gabardina', 'lana'
    gramaje = Column(Float, nullable=True)
    color_index = Column(Integer, nullable=True)
    list_price = Column(Float, nullable=False, default=0.0)
    standard_price = Column(Float, nullable=False, default=0.0)
    sale_ok = Column(Boolean, default=True)
    purchase_ok = Column(Boolean, default=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Tabla simple 'products' por compatibilidad con pruebas iniciales
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    image_url = Column(String, nullable=True)


# ==============================================================================
# 3. TABLA: insumo (Materias Primas: Telas, Hilos, Botones, Cierres)
# ==============================================================================
class Insumo(Base):
    __tablename__ = "insumo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    codigo_insumo = Column(String(50), unique=True, nullable=True)
    stock = Column(Float, nullable=False, default=0.0)
    stock_minimo = Column(Float, nullable=False, default=10.0)
    unidad_medida = Column(String(30), nullable=False, default="metros")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==============================================================================
# 4. TABLA: sales_order (Órdenes de Venta y Cotizaciones)
# ==============================================================================
class SalesOrder(Base):
    __tablename__ = "sales_order"

    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, nullable=False)
    state = Column(String(20), default="confirmed") # 'draft', 'cotizacion', 'confirmed', 'in_production', 'done', 'cancelled'
    date_order = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==============================================================================
# 5. TABLA: orden_produccion (Órdenes de Confección en Taller Textil)
# ==============================================================================
class OrdenProduccion(Base):
    __tablename__ = "orden_produccion"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_id = Column(Integer, nullable=True)
    product_tmpl_id = Column(Integer, nullable=False)
    cantidad_total = Column(Integer, nullable=False, default=1)
    fecha_inicio = Column(Date, server_default=func.current_date())
    fecha_fin = Column(Date, nullable=True)
    prioridad = Column(String(15), default="Media") # 'Urgente', 'Media', 'Baja'
    estado = Column(String(20), default="EnProceso") # 'Pendiente', 'EnProceso', 'Terminado', 'Cancelado'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
