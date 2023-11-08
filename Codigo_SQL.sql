--La compresión "Raw" es una elección adecuada para un área de staging en Amazon Redshift, 
--ya que permite una carga rápida y un acceso eficiente a los datos sin la necesidad de aplicar compresión adicional. 
-- Crear el esquema de área de staging si aún no existe

--CREATE SCHEMA IF NOT EXISTS arturo_b_a_coderhouse;
--BEGIN;
-- Crear la tabla de staging para los datos de acciones
CREATE TABLE IF NOT EXISTS arturo_b_a_coderhouse.stock_data_staging
(
    "Date" DATE ENCODE RAW, -- Almacena la fecha en su forma original (Raw)
    Symbol VARCHAR(10) ENCODE RAW, -- Almacena el símbolo en su forma original (Raw)
    "Open" DECIMAL(12, 6) ENCODE RAW, -- Almacena el precio de apertura en su forma original (Raw)
    High DECIMAL(12, 6) ENCODE RAW, -- Almacena el precio máximo en su forma original (Raw)
    Low DECIMAL(12, 6) ENCODE RAW, -- Almacena el precio mínimo en su forma original (Raw)
    "Close" DECIMAL(12, 6) ENCODE RAW, -- Almacena el precio de cierre en su forma original (Raw)
    Volume BIGINT ENCODE RAW, -- Almacena el volumen en su forma original (Raw)
    Dividends DECIMAL(12, 6) ENCODE RAW, -- Almacena los dividendos en su forma original (Raw)
    Stock_Splits DECIMAL(12, 6) ENCODE RAW -- Almacena las divisiones de acciones en su forma original (Raw)
);
COMMIT
-- Crear la tabla de la Dimensión Fecha
--BEGIN
-- Intenta eliminar la tabla si ya existe, sin generar un error si no existe.
--DROP TABLE IF EXISTS arturo_b_a_coderhouse.Dim_Fecha;
-- Crea la tabla de la Dimensión Fecha.
CREATE TABLE IF NOT EXISTS arturo_b_a_coderhouse.Dim_Fecha
(
    Fecha DATE ENCODE az64 DISTKEY, -- Almacena la fecha con codificación az64
    Dia INTEGER ENCODE az64, -- Almacena el día con codificación az64
    Mes INTEGER ENCODE az64, -- Almacena el mes con codificación az64
    Anio INTEGER ENCODE az64, -- Almacena el año con codificación az64
    PRIMARY KEY(Fecha)
) SORTKEY (Fecha);
-- Confirma la transacción.
COMMIT

-- Crear la tabla de la Dimensión Acción 
--BEGIN
-- Intenta eliminar la tabla si ya existe, sin generar un error si no existe.
--DROP TABLE IF EXISTS arturo_b_a_coderhouse.Dim_Accion;
-- Crea la tabla de la Dimensión Acción.
CREATE TABLE IF NOT EXISTS arturo_b_a_coderhouse.Dim_Accion
(
    ID_Accion       INT NOT NULL DISTKEY,
    Simbolo_Accion  VARCHAR(10),
    Nombre_Empresa  VARCHAR(100) ENCODE lzo, -- Almacena el nombre de la empresa con compresión lzo
    Sector          VARCHAR(100) ENCODE lzo, -- Almacena el sector con compresión lzo
    Industria       VARCHAR(100) ENCODE lzo, -- Almacena la industria con compresión lzo
    Otros_Detalles  VARCHAR(512) ENCODE lzo, -- Almacena otros detalles con compresión lzo
    PRIMARY KEY (ID_Accion)
)

SORTKEY (ID_Accion); -- Utilizar el símbolo de la acción como clave de ordenación, ya que es comúnmente utilizada para buscar información específica de una acción en las consultas
-- Confirma la transacción.
COMMIT

-- Crear la tabla de hechos
--BEGIN;
-- Intenta eliminar la tabla si ya existe, sin generar un error si no existe.
--DROP TABLE IF EXISTS arturo_b_a_coderhouse.Fac_Precio_Acciones;
-- Crea la tabla de hechos.
CREATE TABLE IF NOT EXISTS arturo_b_a_coderhouse.Fac_Precio_Acciones
(
    ID_Precio INT IDENTITY(1,1),
    Fecha DATE, -- Clave Foránea a la Dimensión Fecha
    ID_Accion INTEGER DISTKEY,
    Precio_Apertura DECIMAL(10, 2) ENCODE az64, -- Almacena el precio de apertura con codificación az64
    Precio_Maximo DECIMAL(10, 2) ENCODE az64, -- Almacena el precio máximo con codificación az64
    Precio_Minimo DECIMAL(10, 2) ENCODE az64, -- Almacena el precio mínimo con codificación az64
    Precio_Cierre DECIMAL(10, 2) , -- Almacena el precio de cierre
    Volumen BIGINT ENCODE az64, -- Almacena el volumen con codificación az64
    Dividendos DECIMAL(10, 2) ENCODE az64, -- Almacena los dividendos con codificación az64
    Divisiones_de_Acciones DECIMAL(10, 2) ENCODE az64, -- Almacena las divisiones de acciones con codificación az64
    PRIMARY KEY(ID_Precio)
)
SORTKEY(Fecha, ID_Accion);-- Utiliza Fecha, ID_Accion como clave de ordenación

-- Confirma la transacción.
COMMIT

-- Crear Crear la restricción  Dim_Fecha y Fac_Precio_Acciones
--BEGIN;
-- Crear la restricción de clave foránea entre Dim_Fecha y Fac_Precio_Acciones
ALTER TABLE arturo_b_a_coderhouse.Fac_Precio_Acciones
ADD CONSTRAINT fk_fecha
FOREIGN KEY (Fecha)
REFERENCES arturo_b_a_coderhouse.Dim_Fecha (Fecha);
COMMIT
-- Crear Crear la restricción  Dim_Accion y Fac_Precio_Acciones
--BEGIN;
-- Crear la restricción de clave foránea entre Dim_Accion y Fac_Precio_Acciones
ALTER TABLE arturo_b_a_coderhouse.Fac_Precio_Acciones
ADD CONSTRAINT fk_id_accion
FOREIGN KEY (ID_Accion)
REFERENCES arturo_b_a_coderhouse.Dim_Accion (ID_Accion);
COMMIT