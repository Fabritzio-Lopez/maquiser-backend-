import os
import json
import urllib.request
import logging
from typing import Optional

logger = logging.getLogger("slack_service")

# Obtener URL del webhook desde variables de entorno
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

def set_slack_webhook(url: str):
    """Actualiza la URL del webhook en tiempo de ejecución y persiste en .env"""
    global SLACK_WEBHOOK_URL
    SLACK_WEBHOOK_URL = url.strip()
    try:
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "SLACK_WEBHOOK_URL=" in content:
                import re
                content = re.sub(r'SLACK_WEBHOOK_URL=.*', f'SLACK_WEBHOOK_URL={url.strip()}', content)
            else:
                content += f"\nSLACK_WEBHOOK_URL={url.strip()}\n"
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(content)
    except Exception as e:
        logger.warning(f"No se pudo guardar webhook en .env: {e}")

def get_slack_webhook() -> str:
    """Retorna la URL actual del webhook"""
    return SLACK_WEBHOOK_URL

def is_slack_configured() -> bool:
    """Verifica si hay una URL válida configurada"""
    url = get_slack_webhook()
    return bool(url and url.startswith("https://hooks.slack.com/"))

def send_slack_message(text: str, blocks: Optional[list] = None) -> bool:
    """Envía un mensaje formateado a Slack mediante Webhook Entrante"""
    webhook_url = get_slack_webhook()
    if not webhook_url or not webhook_url.startswith("http"):
        logger.info(f"[Slack Simulado] {text}")
        return True # Retorna True para no bloquear el flujo si no está configurado

    payload = {"text": text}
    if blocks:
        payload["blocks"] = blocks

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "Maquiser-ERP/2.0"}
        )
        with urllib.request.urlopen(req, timeout=6) as response:
            return response.status in (200, 204)
    except Exception as e:
        logger.error(f"Error al enviar mensaje a Slack: {e}")
        return False

# ==============================================================================
# NOTIFICACIONES OFICIALES DEL FLUJO TEXTIL (GUÍA METODOLÓGICA PASO 3.2)
# ==============================================================================
def notify_slack_new_product(product_name: str, price: float, stock: int):
    """
    Función oficial especificada en el Paso 3.2 de la Guía Metodológica:
    Alerta al equipo cuando se registra una nueva prenda o producto textil.
    """
    text = (
        f"🧥 *Nuevo Producto Registrado en Maquiser SRL*\n"
        f"• *Producto:* {product_name}\n"
        f"• *Precio:* Bs. {price:.2f}\n"
        f"• *Stock Inicial:* {stock} unidades"
    )
    return send_slack_message(text)

def notify_slack_new_sale(partner_name: str, amount_total: float, state: str = "Confirmado", items_summary: str = ""):
    """Alerta sobre nueva cotización o pedido de confección generado"""
    detail = f"\n• *Detalle:* {items_summary}" if items_summary else ""
    text = (
        f"📋 *Nuevo Pedido / Cotización en Maquiser SRL*\n"
        f"• *Cliente:* {partner_name}\n"
        f"• *Monto Total:* Bs. {amount_total:,.2f}\n"
        f"• *Estado:* {state}{detail}\n"
        f"• *Origen:* Showroom 3D & Catálogo Web"
    )
    return send_slack_message(text)

def notify_slack_production_stage(order_name: str, product_name: str, stage_name: str, responsible: str = "Taller Central"):
    """Alerta de avance en el tablero Kanban de manufactura textil"""
    text = (
        f"🏭 *Actualización de Taller MRP - Maquiser SRL*\n"
        f"• *Lote de Confección:* {order_name} ({product_name})\n"
        f"• *Nueva Estación:* {stage_name}\n"
        f"• *Responsable:* {responsible}\n"
        f"• *Planta:* Cochabamba, Bolivia"
    )
    return send_slack_message(text)

def notify_slack_inventory_update(insumo_name: str, quantity: float, unit: str, is_low: bool = False):
    """Alerta de recepción de rollos o aviso de stock mínimo"""
    alert_header = "⚠️ *ALERTA: STOCK CRÍTICO DE MATERIA PRIMA*" if is_low else "🧵 *Nuevo Ingreso a Almacén Textil*"
    text = (
        f"{alert_header}\n"
        f"• *Insumo / Tela:* {insumo_name}\n"
        f"• *Stock Registrado:* {quantity} {unit}\n"
        f"• *Almacén:* Central de Telas y Avíos Maquiser SRL"
    )
    return send_slack_message(text)

def notify_slack_test_ping():
    """Mensaje de verificación de conexión"""
    text = (
        f"🚀 *¡Conexión Exitosa con Maquiser SRL Cloud ERP!*\n"
        f"• *Sistema:* FastAPI + React Three.js + Supabase PostgreSQL\n"
        f"• *Integración:* Slack Webhook (Paso 3.2 Guía Metodológica)\n"
        f"• *Estado:* Operativo y listo para recibir alertas en tiempo real."
    )
    return send_slack_message(text)
