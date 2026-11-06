from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# ==============================================================================
# ESQUEMAS PARA CATÁLOGO TEXTIL (Tabla 'product_template' en Supabase)
# ==============================================================================
class ProductTemplateBase(BaseModel):
    name: str
    tipo_producto_textil: Optional[str] = "uniforme_escolar"
    composicion_textil: Optional[str] = None
    tipo_tela: Optional[str] = None
    gramaje: Optional[float] = None
    list_price: float
    standard_price: Optional[float] = 0.0
    sale_ok: Optional[bool] = True
    purchase_ok: Optional[bool] = True
    active: Optional[bool] = True
    image_url: Optional[str] = None

class ProductTemplateCreate(ProductTemplateBase):
    pass

class ProductTemplateResponse(ProductTemplateBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# ESQUEMAS PARA TABLA BÁSICA (Tabla 'products')
# ==============================================================================
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
