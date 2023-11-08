-- Eliminar la restricción de clave foránea entre Dim_Fecha y Fac_Precio_Acciones
ALTER TABLE arturo_b_a_coderhouse.Fac_Precio_Acciones
DROP CONSTRAINT fk_fecha;
COMMIT

-- Eliminar la restricción de clave foránea entre Dim_Accion y Fac_Precio_Acciones
ALTER TABLE arturo_b_a_coderhouse.Fac_Precio_Acciones
DROP CONSTRAINT fk_id_accion;
COMMIT

-- Eliminar la tabla Fac_Precio_Acciones si existe
DROP TABLE IF EXISTS arturo_b_a_coderhouse.Fac_Precio_Acciones;
COMMIT

-- Eliminar la tabla Dim_Fecha si existe
DROP TABLE IF EXISTS arturo_b_a_coderhouse.Dim_Fecha;
COMMIT

-- Eliminar la tabla Dim_Accion si existe
DROP TABLE IF EXISTS arturo_b_a_coderhouse.Dim_Accion;
COMMIT
-- Eliminar la tabla stock_data_staging si existe
DROP TABLE IF EXISTS arturo_b_a_coderhouse.stock_data_staging;
COMMIT