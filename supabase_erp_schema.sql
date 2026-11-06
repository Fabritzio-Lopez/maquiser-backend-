-- ==============================================================================
-- SISTEMA CLOUD ERP TEXTIL - MAQUISER SRL
-- SCRIPT DDL COMPLETO PARA SUPABASE (POSTGRESQL)
-- ==============================================================================

-- 1. TABLA DE CLIENTES, COLEGIOS Y EMPRESAS (CRM / PARTNERS)
CREATE TABLE IF NOT EXISTS res_partner (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    is_company BOOLEAN DEFAULT TRUE,
    tipo_cliente VARCHAR(50) DEFAULT 'colegio', -- 'colegio', 'empresa_industrial', 'particular', 'proveedor'
    email VARCHAR(255),
    phone VARCHAR(50),
    nit_ci VARCHAR(50),
    ciudad VARCHAR(100) DEFAULT 'Cochabamba',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABLA DE PRODUCTOS TEXTILES Y CONFECCIÓN (CATÁLOGO)
CREATE TABLE IF NOT EXISTS product_template (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tipo_producto_textil VARCHAR(50) DEFAULT 'uniforme_escolar', -- 'uniforme_escolar', 'industrial', 'camisa', 'materia_prima'
    composicion_textil VARCHAR(100),
    tipo_tela VARCHAR(100),
    gramaje NUMERIC(6,2),
    list_price NUMERIC(10,2) NOT NULL DEFAULT 0.0,
    standard_price NUMERIC(10,2) NOT NULL DEFAULT 0.0,
    stock INTEGER DEFAULT 0,
    sale_ok BOOLEAN DEFAULT TRUE,
    purchase_ok BOOLEAN DEFAULT TRUE,
    active BOOLEAN DEFAULT TRUE,
    image_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. TABLA DE PEDIDOS DE VENTA Y COTIZACIONES
CREATE TABLE IF NOT EXISTS sale_order (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE, -- Ej: PED-2026-001
    partner_id INTEGER REFERENCES res_partner(id),
    partner_name VARCHAR(255) NOT NULL,
    date_order TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    amount_total NUMERIC(12,2) NOT NULL DEFAULT 0.0,
    state VARCHAR(50) DEFAULT 'borrador', -- 'borrador', 'confirmado', 'en_produccion', 'entregado', 'cancelado'
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. TABLA DE LÍNEAS DE PEDIDO DE VENTA
CREATE TABLE IF NOT EXISTS sale_order_line (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES sale_order(id) ON DELETE CASCADE,
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    price_unit NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(12,2) NOT NULL
);

-- 5. TABLA DE PRODUCCIÓN Y TALLER TEXTIL (MRP)
CREATE TABLE IF NOT EXISTS mrp_production (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE, -- Ej: OP-2026-101
    product_name VARCHAR(255) NOT NULL,
    partner_name VARCHAR(255),
    quantity INTEGER NOT NULL DEFAULT 1,
    state VARCHAR(50) DEFAULT 'corte', -- 'corte', 'confeccion', 'bordado', 'control_calidad', 'terminado'
    date_planned DATE DEFAULT CURRENT_DATE,
    responsible VARCHAR(100) DEFAULT 'Maestro Cortador / Taller Central',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. TABLA DE INVENTARIO DE MATERIAS PRIMAS Y TELAS
CREATE TABLE IF NOT EXISTS stock_item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50) DEFAULT 'materia_prima', -- 'tela_rollo', 'avio', 'insumo'
    stock_quantity NUMERIC(10,2) NOT NULL DEFAULT 0,
    min_quantity NUMERIC(10,2) NOT NULL DEFAULT 10,
    unit_measure VARCHAR(20) DEFAULT 'metros', -- 'metros', 'unidades', 'conos', 'rollos'
    location VARCHAR(100) DEFAULT 'Almacén Central Quillacollo',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- DATOS SEMILLA REALISTAS DE MAQUISER SRL
-- ==============================================================================

-- Clientes e Instituciones
INSERT INTO res_partner (name, is_company, tipo_cliente, email, phone, nit_ci, ciudad)
VALUES
    ('Colegio Alemán Federico Froebel', TRUE, 'colegio', 'administracion@froebel.edu.bo', '+591 4 4251234', '1029384021', 'Cochabamba'),
    ('Colegio San Agustín', TRUE, 'colegio', 'finanzas@sanagustin.edu.bo', '+591 4 4298765', '1928374012', 'Cochabamba'),
    ('Minera San Cristóbal S.A.', TRUE, 'empresa_industrial', 'compras@minerasancristobal.com', '+591 2 2779988', '3029182019', 'Potosí'),
    ('Constructora Boliviana del Valle SRL', TRUE, 'empresa_industrial', 'logistica@cbv.bo', '+591 4 4112233', '4019283011', 'Cochabamba'),
    ('Unidad Educativa La Salle', TRUE, 'colegio', 'secretaria@lasalle.edu.bo', '+591 4 4301122', '5029182012', 'Cochabamba')
ON CONFLICT DO NOTHING;

-- Catálogo de Prendas
INSERT INTO product_template (name, tipo_producto_textil, composicion_textil, tipo_tela, gramaje, list_price, standard_price, stock, active)
VALUES
    ('Uniforme Escolar Completo Varón (Blazer + Pantalón)', 'uniforme_escolar', '65% Poliéster / 35% Algodón', 'Gabardina Sarga', 245.0, 160.00, 95.00, 65, TRUE),
    ('Uniforme Escolar Completo Mujer (Blazer + Falda Tablas)', 'uniforme_escolar', '65% Poliéster / 35% Algodón', 'Gabardina Sarga', 245.0, 155.00, 90.00, 50, TRUE),
    ('Overol Industrial Térmico Ignífugo 3M', 'industrial', '100% Algodón Tratado FR', 'Ripstop Ignífugo', 290.0, 195.00, 115.00, 42, TRUE),
    ('Camisa Institucional Oxford Manga Larga', 'camisa', '80% Algodón / 20% Poliéster', 'Popelina Oxford', 125.0, 85.00, 45.00, 120, TRUE),
    ('Chaleco de Seguridad Reflectivo Bicolor', 'industrial', '100% Poliéster de Alta Visibilidad', 'Tejido Malla Fluorescente', 130.0, 65.00, 30.00, 90, TRUE)
ON CONFLICT DO NOTHING;

-- Pedidos de Venta
INSERT INTO sale_order (name, partner_id, partner_name, amount_total, state, notes)
VALUES
    ('PED-2026-001', 1, 'Colegio Alemán Federico Froebel', 19200.00, 'en_produccion', '120 uniformes completos para secundaria con escudo bordado'),
    ('PED-2026-002', 3, 'Minera San Cristóbal S.A.', 39000.00, 'en_produccion', '200 overoles ignífugos con cinta reflectiva 3M para cuadrilla mina'),
    ('PED-2026-003', 2, 'Colegio San Agustín', 12750.00, 'confirmado', '150 camisas institucionales bordadas'),
    ('PED-2026-004', 4, 'Constructora Boliviana del Valle SRL', 5850.00, 'entregado', '90 chalecos de seguridad entregados en obra Sacaba')
ON CONFLICT DO NOTHING;

-- Órdenes de Confección en Taller (MRP)
INSERT INTO mrp_production (name, product_name, partner_name, quantity, state, date_planned, responsible)
VALUES
    ('OP-2026-101', 'Uniforme Escolar Completo Varón', 'Colegio Alemán Federico Froebel', 120, 'corte', CURRENT_DATE + 3, 'Taller de Corte Central'),
    ('OP-2026-102', 'Overol Industrial Térmico Ignífugo 3M', 'Minera San Cristóbal S.A.', 200, 'confeccion', CURRENT_DATE + 5, 'Línea 2 de Confección Pesada'),
    ('OP-2026-103', 'Camisa Institucional Oxford', 'Colegio San Agustín', 150, 'bordado', CURRENT_DATE + 2, 'Máquina Bordadora Tajima 12 Cabezas'),
    ('OP-2026-104', 'Chaleco de Seguridad Reflectivo', 'Constructora Boliviana del Valle SRL', 90, 'terminado', CURRENT_DATE, 'Control de Calidad / Empaque')
ON CONFLICT DO NOTHING;

-- Inventario de Materias Primas
INSERT INTO stock_item (name, category, stock_quantity, min_quantity, unit_measure, location)
VALUES
    ('Rollo Tela Gabardina Sarga Azul Marino 65/35', 'tela_rollo', 850.0, 200.0, 'metros', 'Bodega 1 - Estante A'),
    ('Rollo Tela Ripstop Ignífugo Naranja Industrial', 'tela_rollo', 420.0, 150.0, 'metros', 'Bodega 1 - Estante C'),
    ('Rollo Tela Popelina Oxford Blanca', 'tela_rollo', 95.0, 150.0, 'metros', 'Bodega 1 - Estante B'), -- ALERTA STOCK BAJO
    ('Cinta Reflectiva Microprismática 3M Scotchlite (5cm)', 'avio', 620.0, 200.0, 'metros', 'Bodega Insumos - Gaveta 4'),
    ('Botones de Nácar 4 Orificios (Caja 1000 u.)', 'avio', 14.0, 5.0, 'cajas', 'Bodega Insumos - Gaveta 1'),
    ('Conos de Hilo Industrial Poliéster 100/2 Azul', 'insumo', 38.0, 10.0, 'conos', 'Taller Confección')
ON CONFLICT DO NOTHING;
