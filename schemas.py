from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date

# ==============================================================================
# ESQUEMAS: CLIENTES / COLEGIOS (PARTNERS)
# ==============================================================================
class PartnerBase(BaseModel):
    name: str
    is_company: Optional[bool] = True
    tipo_cliente: Optional[str] = "colegio"
    email: Optional[str] = None
    phone: Optional[str] = None
    nit_ci: Optional[str] = None
    ciudad: Optional[str] = "Cochabamba"

class PartnerCreate(PartnerBase):
    pass

class PartnerResponse(PartnerBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# ESQUEMAS: PRODUCTOS TEXTILES
# ==============================================================================
class ProductTemplateBase(BaseModel):
    name: str
    tipo_producto_textil: Optional[str] = "uniforme_escolar"
    composicion_textil: Optional[str] = None
    tipo_tela: Optional[str] = None
    gramaje: Optional[float] = None
    list_price: float
    standard_price: Optional[float] = 0.0
    stock: Optional[int] = 0
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


# Esquema simple products
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


# ==============================================================================
# ESQUEMAS: VENTAS Y PEDIDOS
# ==============================================================================
class SaleOrderBase(BaseModel):
    name: str
    partner_id: Optional[int] = None
    partner_name: str
    amount_total: float
    state: Optional[str] = "borrador"
    notes: Optional[str] = None

class SaleOrderCreate(BaseModel):
    partner_name: str
    amount_total: float
    notes: Optional[str] = None
    state: Optional[str] = "confirmado"

class SaleOrderStatusUpdate(BaseModel):
    state: str

class SaleOrderResponse(SaleOrderBase):
    id: int
    date_order: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# ESQUEMAS: PRODUCCIÓN EN TALLER (MRP)
# ==============================================================================
class ProductionOrderBase(BaseModel):
    name: str
    product_name: str
    partner_name: Optional[str] = None
    quantity: int = 1
    state: Optional[str] = "corte"
    date_planned: Optional[date] = None
    responsible: Optional[str] = "Taller Central Maquiser"

class ProductionOrderCreate(BaseModel):
    product_name: str
    partner_name: Optional[str] = None
    quantity: int = 1
    state: Optional[str] = "corte"

class ProductionOrderStatusUpdate(BaseModel):
    state: str

class ProductionOrderResponse(ProductionOrderBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# ESQUEMAS: INVENTARIO DE MATERIAS PRIMAS
# ==============================================================================
class StockItemBase(BaseModel):
    name: str
    category: Optional[str] = "tela_rollo"
    stock_quantity: float
    min_quantity: Optional[float] = 10.0
    unit_measure: Optional[str] = "metros"
    location: Optional[str] = "Almacén Central"

class StockItemCreate(StockItemBase):
    pass

class StockAddRequest(BaseModel):
    quantity: float

class StockItemResponse(StockItemBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# ESQUEMAS: AUTENTICACIÓN Y ROLES (RBAC)
# ==============================================================================
class LoginRequest(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    id: int
    username: str
    name: str
    email: str
    role: str
    role_name: str
    title: str
    avatar_color: str
    allowed_tabs: List[str]
    can_edit_production: bool
    can_edit_inventory: bool
    can_manage_sales: Optional[bool] = False
    can_manage_users: Optional[bool] = False

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile


# ==============================================================================
# ESQUEMA: MÉTRICAS DEL DASHBOARD EJECUTIVO (KPIS)
# ==============================================================================
class DashboardKPIs(BaseModel):
    total_sales_bs: float
    active_production_orders: int
    low_stock_alerts: int
    total_partners: int
    total_products_stock: int


# ==============================================================================
# ESQUEMAS: INTEGRACIÓN CON SLACK (PASO 3.2 GUÍA METODOLÓGICA)
# ==============================================================================
class SlackWebhookConfig(BaseModel):
    webhook_url: str

class SlackStatusResponse(BaseModel):
    configured: bool
    webhook_url: Optional[str] = None
    channel: Optional[str] = "#notificaciones-maquiser"
    events: List[str] = []

