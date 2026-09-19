-- ============================================================
--  Base de datos: ProyectoMoanso
--  Convertida de SQL Server a PostgreSQL
--  Incluye: DDL (tablas, PKs, UKs, FKs) + datos (INSERT)
-- ============================================================

-- Si quieres crear la base de datos desde cero, descomenta:
-- CREATE DATABASE "ProyectoMoanso";
-- \c ProyectoMoanso

-- ============================================================
--  TABLAS (sin dependencias primero)
-- ============================================================

CREATE TABLE Ubigeo (
    codigo_ubigeo   INTEGER         NOT NULL,
    provincia       VARCHAR(25)     NOT NULL,
    distrito        VARCHAR(25)     NOT NULL,
    departamento    VARCHAR(25)     NOT NULL,
    estado_ubigeo   BOOLEAN         NOT NULL,
    CONSTRAINT pk_ubigeo PRIMARY KEY (codigo_ubigeo)
);

CREATE TABLE Rubro (
    id_rubro        SERIAL          NOT NULL,
    nombre          VARCHAR(100)    NOT NULL,
    descripcion     VARCHAR(100),
    estado_rubro    BOOLEAN         NOT NULL,
    CONSTRAINT pk_rubro PRIMARY KEY (id_rubro)
);

CREATE TABLE Marca (
    id_marca        SERIAL          NOT NULL,
    nombre          VARCHAR(100)    NOT NULL,
    pais_origen     VARCHAR(100),
    fecha_fundacion DATE,
    descripcion     VARCHAR(50),
    estado_marca    BOOLEAN         NOT NULL,
    CONSTRAINT pk_marca PRIMARY KEY (id_marca)
);

CREATE TABLE TipoUnidad (
    id_tipo_unidad  SERIAL          NOT NULL,
    nombre          VARCHAR(50)     NOT NULL,
    descripcion     VARCHAR(50),
    estado_tipounidad BOOLEAN       NOT NULL,
    CONSTRAINT pk_tipo_unidad PRIMARY KEY (id_tipo_unidad)
);

CREATE TABLE TipoGasto (
    id_tipo_gasto   SERIAL          NOT NULL,
    nombre          VARCHAR(100)    NOT NULL,
    descripcion     VARCHAR(200),
    estado_tipogasto BOOLEAN        NOT NULL,
    CONSTRAINT pk_tipo_gasto PRIMARY KEY (id_tipo_gasto)
);

CREATE TABLE ProductoCategoria (
    id_categoria    SERIAL          NOT NULL,
    nombre          VARCHAR(100)    NOT NULL,
    descripcion     VARCHAR(200),
    estado_categoria BOOLEAN        NOT NULL,
    CONSTRAINT pk_producto_categoria PRIMARY KEY (id_categoria)
);

-- ============================================================

CREATE TABLE Direccion (
    id_direccion            SERIAL          NOT NULL,
    codigo_ubigeo           INTEGER         NOT NULL,
    direccion_detallada     VARCHAR(200)    NOT NULL,
    referencia              VARCHAR(50),
    descripcion             VARCHAR(50),
    estado_direccion        BOOLEAN         NOT NULL,
    CONSTRAINT pk_direccion PRIMARY KEY (id_direccion),
    CONSTRAINT fk_direccion_ubigeo FOREIGN KEY (codigo_ubigeo)
        REFERENCES Ubigeo (codigo_ubigeo)
);

CREATE TABLE SubtipoUnidad (
    id_subtipo_unidad   SERIAL          NOT NULL,
    id_tipo_unidad      INTEGER         NOT NULL,
    nombre              VARCHAR(50)     NOT NULL,
    descripcion         VARCHAR(50),
    estado_subtipounidad BOOLEAN        NOT NULL,
    CONSTRAINT pk_subtipo_unidad PRIMARY KEY (id_subtipo_unidad),
    CONSTRAINT fk_subtipo_tipo_unidad FOREIGN KEY (id_tipo_unidad)
        REFERENCES TipoUnidad (id_tipo_unidad)
);

CREATE TABLE Conductor (
    id_conductor        SERIAL          NOT NULL,
    dni                 CHAR(8)         NOT NULL,
    nombre1             VARCHAR(50)     NOT NULL,
    nombre2             VARCHAR(50),
    apellido1           VARCHAR(50)     NOT NULL,
    apellido2           VARCHAR(50),
    licencia_conducir   VARCHAR(20)     NOT NULL,
    telefono            VARCHAR(20),
    correo              VARCHAR(100),
    direccion           VARCHAR(200),
    fecha_nacimiento    DATE,
    estado_conductor    BOOLEAN         NOT NULL,
    CONSTRAINT pk_conductor PRIMARY KEY (id_conductor),
    CONSTRAINT uq_conductor_dni UNIQUE (dni)
);

CREATE TABLE Unidad (
    id_unidad           SERIAL          NOT NULL,
    placa               VARCHAR(20)     NOT NULL,
    id_tipo_unidad      INTEGER         NOT NULL,
    id_subtipo_unidad   INTEGER,
    id_marca            INTEGER         NOT NULL,
    modelo              VARCHAR(50),
    anio                INTEGER,                    -- "año" renombrado a "anio" (evita conflicto)
    peso_tara           NUMERIC(10,2),
    peso_maximo         NUMERIC(10,2),
    estado_unidad       BOOLEAN         NOT NULL,
    CONSTRAINT pk_unidad PRIMARY KEY (id_unidad),
    CONSTRAINT uq_unidad_placa UNIQUE (placa),
    CONSTRAINT fk_unidad_tipo FOREIGN KEY (id_tipo_unidad)
        REFERENCES TipoUnidad (id_tipo_unidad),
    CONSTRAINT fk_unidad_subtipo FOREIGN KEY (id_subtipo_unidad)
        REFERENCES SubtipoUnidad (id_subtipo_unidad),
    CONSTRAINT fk_unidad_marca FOREIGN KEY (id_marca)
        REFERENCES Marca (id_marca)
);

CREATE TABLE Cliente (
    id_cliente              SERIAL          NOT NULL,
    razon_social            VARCHAR(150)    NOT NULL,
    ruc                     CHAR(11)        NOT NULL,
    telefono                VARCHAR(20),
    correo                  VARCHAR(100),
    contacto                VARCHAR(100),
    id_rubro                INTEGER         NOT NULL,
    id_direccion_domicilio  INTEGER,
    estado_cliente          BOOLEAN         NOT NULL,
    CONSTRAINT pk_cliente PRIMARY KEY (id_cliente),
    CONSTRAINT uq_cliente_ruc UNIQUE (ruc),
    CONSTRAINT fk_cliente_rubro FOREIGN KEY (id_rubro)
        REFERENCES Rubro (id_rubro),
    CONSTRAINT fk_cliente_direccion FOREIGN KEY (id_direccion_domicilio)
        REFERENCES Direccion (id_direccion)
);

CREATE TABLE ConductorUnidad (
    id_conductor_unidad SERIAL          NOT NULL,
    id_conductor        INTEGER         NOT NULL,
    id_unidad           INTEGER         NOT NULL,
    fecha_asignacion    TIMESTAMP       NOT NULL,
    fecha_fin           TIMESTAMP,
    estado_asignacion   BOOLEAN         NOT NULL,
    CONSTRAINT pk_conductor_unidad PRIMARY KEY (id_conductor_unidad),
    CONSTRAINT fk_cu_conductor FOREIGN KEY (id_conductor)
        REFERENCES Conductor (id_conductor),
    CONSTRAINT fk_cu_unidad FOREIGN KEY (id_unidad)
        REFERENCES Unidad (id_unidad)
);

CREATE TABLE ProgramacionViaje (
    id_viaje                SERIAL          NOT NULL,
    id_tracto               INTEGER         NOT NULL,
    id_carreta              INTEGER         NOT NULL,
    id_conductor_unidad     INTEGER         NOT NULL,
    id_direccion_origen     INTEGER         NOT NULL,
    id_direccion_destino    INTEGER         NOT NULL,
    fecha_programado        TIMESTAMP       NOT NULL,
    id_cliente              INTEGER         NOT NULL,
    estado_viaje            BOOLEAN         NOT NULL,
    CONSTRAINT pk_programacion_viaje PRIMARY KEY (id_viaje),
    CONSTRAINT fk_pv_tracto FOREIGN KEY (id_tracto)
        REFERENCES Unidad (id_unidad),
    CONSTRAINT fk_pv_carreta FOREIGN KEY (id_carreta)
        REFERENCES Unidad (id_unidad),
    CONSTRAINT fk_pv_conductor_unidad FOREIGN KEY (id_conductor_unidad)
        REFERENCES ConductorUnidad (id_conductor_unidad),
    CONSTRAINT fk_pv_origen FOREIGN KEY (id_direccion_origen)
        REFERENCES Direccion (id_direccion),
    CONSTRAINT fk_pv_destino FOREIGN KEY (id_direccion_destino)
        REFERENCES Direccion (id_direccion),
    CONSTRAINT fk_pv_cliente FOREIGN KEY (id_cliente)
        REFERENCES Cliente (id_cliente)
);

CREATE TABLE GuiaTransportista (
    id_guia_transportista   SERIAL          NOT NULL,
    numero_guia             VARCHAR(50)     NOT NULL,
    id_viaje                INTEGER         NOT NULL,
    guias_remitente         VARCHAR(500),
    peso_total              NUMERIC(10,2)   NOT NULL,
    estado_guia             BOOLEAN         NOT NULL,
    CONSTRAINT pk_guia_transportista PRIMARY KEY (id_guia_transportista),
    CONSTRAINT uq_guia_numero UNIQUE (numero_guia),
    CONSTRAINT uq_guia_viaje UNIQUE (id_viaje),
    CONSTRAINT fk_gt_viaje FOREIGN KEY (id_viaje)
        REFERENCES ProgramacionViaje (id_viaje)
);

CREATE TABLE ViajeRealizado (
    id_viaje_realizado      SERIAL          NOT NULL,
    id_guia_transportista   INTEGER         NOT NULL,
    flete                   NUMERIC(10,2)   NOT NULL,
    fecha_llegada           TIMESTAMP       NOT NULL,
    observaciones           VARCHAR(200),
    estado_viaje_realizado  BOOLEAN         NOT NULL,
    CONSTRAINT pk_viaje_realizado PRIMARY KEY (id_viaje_realizado),
    CONSTRAINT uq_vr_guia UNIQUE (id_guia_transportista),
    CONSTRAINT fk_vr_guia FOREIGN KEY (id_guia_transportista)
        REFERENCES GuiaTransportista (id_guia_transportista)
);

CREATE TABLE Factura (
    id_factura          SERIAL          NOT NULL,
    numero_factura      VARCHAR(50)     NOT NULL,
    id_viaje_realizado  INTEGER         NOT NULL,
    monto_total         NUMERIC(10,2)   NOT NULL,
    estado_factura      BOOLEAN         NOT NULL,
    CONSTRAINT pk_factura PRIMARY KEY (id_factura),
    CONSTRAINT uq_factura_numero UNIQUE (numero_factura),
    CONSTRAINT uq_factura_viaje UNIQUE (id_viaje_realizado),
    CONSTRAINT fk_factura_viaje FOREIGN KEY (id_viaje_realizado)
        REFERENCES ViajeRealizado (id_viaje_realizado)
);

CREATE TABLE PresupuestoViaje (
    id_presupuesto      SERIAL          NOT NULL,
    id_viaje            INTEGER         NOT NULL,
    monto_total         NUMERIC(10,2)   NOT NULL,
    fecha_registro      TIMESTAMP       NOT NULL,
    estado_presupuesto  BOOLEAN         NOT NULL,
    CONSTRAINT pk_presupuesto_viaje PRIMARY KEY (id_presupuesto),
    CONSTRAINT uq_presupuesto_viaje UNIQUE (id_viaje),
    CONSTRAINT fk_pres_viaje FOREIGN KEY (id_viaje)
        REFERENCES ProgramacionViaje (id_viaje)
);

CREATE TABLE DetallePresupuesto (
    id_detalle_presupuesto      SERIAL          NOT NULL,
    id_presupuesto              INTEGER         NOT NULL,
    id_tipo_gasto               INTEGER         NOT NULL,
    monto_estimado              NUMERIC(10,2)   NOT NULL,
    estado_detallepresupuesto   BOOLEAN,
    CONSTRAINT pk_detalle_presupuesto PRIMARY KEY (id_detalle_presupuesto),
    CONSTRAINT fk_dp_presupuesto FOREIGN KEY (id_presupuesto)
        REFERENCES PresupuestoViaje (id_presupuesto),
    CONSTRAINT fk_dp_tipo_gasto FOREIGN KEY (id_tipo_gasto)
        REFERENCES TipoGasto (id_tipo_gasto)
);

CREATE TABLE ProductoTransportado (
    id_producto_transportado    SERIAL          NOT NULL,
    id_guia_transportista       INTEGER         NOT NULL,
    id_categoria                INTEGER         NOT NULL,
    descripcion_producto        VARCHAR(200)    NOT NULL,
    cantidad                    INTEGER         NOT NULL,
    peso                        NUMERIC(10,2)   NOT NULL,
    estado_producto             BOOLEAN         NOT NULL,
    CONSTRAINT pk_producto_transportado PRIMARY KEY (id_producto_transportado),
    CONSTRAINT fk_pt_guia FOREIGN KEY (id_guia_transportista)
        REFERENCES GuiaTransportista (id_guia_transportista),
    CONSTRAINT fk_pt_categoria FOREIGN KEY (id_categoria)
        REFERENCES ProductoCategoria (id_categoria)
);

-- ============================================================
--  DATOS
-- ============================================================

-- Ubigeo
INSERT INTO Ubigeo (codigo_ubigeo, provincia, distrito, departamento, estado_ubigeo) VALUES
(130101, 'Trujillo', 'Trujillo',         'La Libertad', TRUE),
(130102, 'Trujillo', 'El Porvenir',      'La Libertad', TRUE),
(130103, 'Trujillo', 'Florencia de Mora','La Libertad', TRUE),
(130104, 'Trujillo', 'La Esperanza',     'La Libertad', TRUE),
(130107, 'Trujillo', 'Moche',            'La Libertad', TRUE);

-- Rubro
INSERT INTO Rubro (id_rubro, nombre, descripcion, estado_rubro) OVERRIDING SYSTEM VALUE VALUES
(1, 'Agroindustria', 'Empresas que exportan productos agrícolas', TRUE),
(2, 'Construcción',  'Empresas del rubro de infraestructura y materiales', TRUE),
(3, 'Minería',       'Mineras que requieren transporte de materiales', TRUE);
SELECT setval('rubro_id_rubro_seq', 3);

-- Marca
INSERT INTO Marca (id_marca, nombre, pais_origen, fecha_fundacion, descripcion, estado_marca) OVERRIDING SYSTEM VALUE VALUES
(1, 'Volvo',        'Suecia',   '1927-04-14', 'Marca de camiones pesados', TRUE),
(2, 'Scania',       'Suecia',   '1891-12-01', 'Camiones para carga pesada', TRUE),
(3, 'Mercedes-Benz','Alemania', '1926-07-29', 'Vehículos y tractos', TRUE);
SELECT setval('marca_id_marca_seq', 3);

-- TipoUnidad
INSERT INTO TipoUnidad (id_tipo_unidad, nombre, descripcion, estado_tipounidad) OVERRIDING SYSTEM VALUE VALUES
(1, 'Tracto',  'Unidad motora para remolque', TRUE),
(2, 'Carreta', 'Unidad de carga remolcada',   TRUE);
SELECT setval('tipounidad_id_tipo_unidad_seq', 2);

-- TipoGasto
INSERT INTO TipoGasto (id_tipo_gasto, nombre, descripcion, estado_tipogasto) OVERRIDING SYSTEM VALUE VALUES
(1, 'Combustible',  'Gasto por consumo de diésel en ruta', TRUE),
(2, 'Peajes',       'Gastos por uso de autopistas',        TRUE),
(3, 'Viáticos',     'Gastos del conductor durante el viaje', TRUE),
(4, 'Mantenimiento','Revisión y reparación de unidades',   TRUE);
SELECT setval('tipogasto_id_tipo_gasto_seq', 4);

-- ProductoCategoria
INSERT INTO ProductoCategoria (id_categoria, nombre, descripcion, estado_categoria) OVERRIDING SYSTEM VALUE VALUES
(1, 'Frutas',                   'Productos agrícolas como mango, plátano, etc.', TRUE),
(2, 'Minerales',                'Concentrado de cobre, zinc, etc.',              TRUE),
(3, 'Materiales de Construcción','Cemento, fierro, ladrillo, etc.',              TRUE);
SELECT setval('productocategoria_id_categoria_seq', 3);

-- Direccion
INSERT INTO Direccion (id_direccion, codigo_ubigeo, direccion_detallada, referencia, descripcion, estado_direccion) OVERRIDING SYSTEM VALUE VALUES
(1, 130101, 'Av. América Sur 1234',                         'Frente al Mall Aventura',  'Oficina Central',   TRUE),
(2, 130107, 'Z.i. Parque Industrial Sur Car.Industrial 15176','Espaldas de Terrapuerto','Almacén Carranza',  TRUE),
(3, 130107, 'Car.Industrial A Laredo Nro. Fnd. Barrio Nuevo','A una cuadra de VOLVO',   'Planta DAMPER',     TRUE);
SELECT setval('direccion_id_direccion_seq', 3);

-- SubtipoUnidad
INSERT INTO SubtipoUnidad (id_subtipo_unidad, id_tipo_unidad, nombre, descripcion, estado_subtipounidad) OVERRIDING SYSTEM VALUE VALUES
(1, 1, 'Tracto Americano',      'Ideal para distancias largas', TRUE),
(2, 2, 'Plataforma Paletizada', 'Para contenedores grandes',    TRUE);
SELECT setval('subtipounidad_id_subtipo_unidad_seq', 2);

-- Conductor
INSERT INTO Conductor (id_conductor, dni, nombre1, nombre2, apellido1, apellido2, licencia_conducir, telefono, correo, direccion, fecha_nacimiento, estado_conductor) OVERRIDING SYSTEM VALUE VALUES
(1, '44781234', 'Juan',  'Carlos', 'Ramirez',   'Ortega',   'AII-B',  '923456789', 'juan.ramirez@correo.com',   'Av. Húsares de Junín 789, Trujillo',        '1985-07-21', TRUE),
(2, '45678123', 'Pedro', NULL,     'Mendoza',   'Vega',     'AII-C',  '934567812', 'pedro.mendoza@correo.com',  'Urbanización Santa María, Mz H Lote 9',     '1990-03-12', TRUE),
(3, '46231987', 'Luis',  'Alberto','Fernández', 'Quispe',   'AII-A',  '945678123', 'luis.fernandez@correo.com', 'Jr. Los Laureles 123, Cajamarca',           '1987-11-03', TRUE),
(4, '47125896', 'María', 'Elena',  'Salazar',   'Huamán',   'AI',     '956781234', 'maria.salazar@correo.com',  'Av. América Sur 456, Trujillo',             '1992-05-18', TRUE),
(5, '48963217', 'Carlos',NULL,     'Gutiérrez', 'Paredes',  'AIII-B', '967812345', 'carlos.gutierrez@correo.com','Urbanización El Molino, Mz B Lote 7',      '1983-09-26', TRUE),
(6, '47891236', 'Ana',  'Lucía',   'Ramos',     'Espinoza', 'AII-B',  '978123456', 'ana.ramos@correo.com',      'Calle Las Flores 890, Piura',               '1988-02-14', TRUE),
(7, '49984321', 'José', 'Manuel',  'Chávez',    'Ortega',   'AII-C',  '989654321', 'jose.chavez@correo.com',    'Av. Miraflores 300, Chiclayo',              '1991-07-30', TRUE);
SELECT setval('conductor_id_conductor_seq', 7);

-- Rubro (ya insertado arriba, se omite)

-- Cliente
INSERT INTO Cliente (id_cliente, razon_social, ruc, telefono, correo, contacto, id_rubro, id_direccion_domicilio, estado_cliente) OVERRIDING SYSTEM VALUE VALUES
(1, 'DANPER',       '20481234561', '044123456', 'contacto@agroexport.com',       'Lucía Torres', 1, 3, TRUE),
(2, 'ALICORP S.A.C','20481234562', '044765432', 'contacto@alicorpexport.com',    'Carlos Rivas',  1, 2, TRUE);
SELECT setval('cliente_id_cliente_seq', 2);

-- Unidad
INSERT INTO Unidad (id_unidad, placa, id_tipo_unidad, id_subtipo_unidad, id_marca, modelo, anio, peso_tara, peso_maximo, estado_unidad) OVERRIDING SYSTEM VALUE VALUES
(1, 'T5A-874', 1, 1, 1, 'FH16',             2022, 8000.00, 42000.00, TRUE),
(2, 'C9G-312', 2, 2, 1, 'Plataforma Larga', 2021, 3500.00, 30000.00, TRUE),
(3, 'T1C-7D1', 1, 1, 3, 'FP23',             2024, 8400.00, 42000.00, TRUE),
(4, 'T4C-7F2', 1, 1, 1, 'FA5V',             2025, 8200.00, 42000.00, TRUE),
(5, 'T5A-5V1', 2, 2, 2, 'BS15',             2024, 4200.00, 43200.00, TRUE);
SELECT setval('unidad_id_unidad_seq', 5);

-- ConductorUnidad
INSERT INTO ConductorUnidad (id_conductor_unidad, id_conductor, id_unidad, fecha_asignacion, fecha_fin, estado_asignacion) OVERRIDING SYSTEM VALUE VALUES
(1, 1, 1, '2025-07-01 19:45:29', '2025-07-07 20:05:50', FALSE),
(2, 2, 2, '2025-07-04 19:46:11', NULL,                  TRUE);
SELECT setval('conductorunidad_id_conductor_unidad_seq', 2);

-- ProgramacionViaje
INSERT INTO ProgramacionViaje (id_viaje, id_tracto, id_carreta, id_conductor_unidad, id_direccion_origen, id_direccion_destino, fecha_programado, id_cliente, estado_viaje) OVERRIDING SYSTEM VALUE VALUES
(1, 2, 1, 1, 1, 1, '2025-07-07 20:05:50', 1, TRUE);
SELECT setval('programacionviaje_id_viaje_seq', 1);

-- GuiaTransportista
INSERT INTO GuiaTransportista (id_guia_transportista, numero_guia, id_viaje, guias_remitente, peso_total, estado_guia) OVERRIDING SYSTEM VALUE VALUES
(1, 'GT-001-TRUJILLO', 1, 'GR-89451, GR-89452', 11000.00, TRUE);
SELECT setval('guiatransportista_id_guia_transportista_seq', 1);

-- ViajeRealizado
INSERT INTO ViajeRealizado (id_viaje_realizado, id_guia_transportista, flete, fecha_llegada, observaciones, estado_viaje_realizado) OVERRIDING SYSTEM VALUE VALUES
(1, 1, 8000.00, '2025-07-07 20:55:03', 'Se realizo correctamente', TRUE);
SELECT setval('viajerealizado_id_viaje_realizado_seq', 1);

-- Factura
INSERT INTO Factura (id_factura, numero_factura, id_viaje_realizado, monto_total, estado_factura) OVERRIDING SYSTEM VALUE VALUES
(1, 'VGI-909', 1, 8200.00, TRUE);
SELECT setval('factura_id_factura_seq', 1);

-- PresupuestoViaje
INSERT INTO PresupuestoViaje (id_presupuesto, id_viaje, monto_total, fecha_registro, estado_presupuesto) OVERRIDING SYSTEM VALUE VALUES
(1, 1, 4000.00, '2025-07-07 00:00:00', TRUE);
SELECT setval('presupuestoviaje_id_presupuesto_seq', 1);

-- DetallePresupuesto
INSERT INTO DetallePresupuesto (id_detalle_presupuesto, id_presupuesto, id_tipo_gasto, monto_estimado, estado_detallepresupuesto) OVERRIDING SYSTEM VALUE VALUES
(1, 1, 1, 2000.00, TRUE),
(2, 1, 2,  500.00, TRUE);
SELECT setval('detallepresupuesto_id_detalle_presupuesto_seq', 2);
