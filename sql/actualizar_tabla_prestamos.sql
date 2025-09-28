-- Agregar columnas para trazabilidad de deudas
ALTER TABLE prestamos
ADD COLUMN IF NOT EXISTS cuota_mensual float,
ADD COLUMN IF NOT EXISTS saldo_restante float,
ADD COLUMN IF NOT EXISTS estado varchar(20) default 'ACTIVO';

-- Actualizar registros existentes (si los hay) para que tengan saldo_restante = monto
UPDATE prestamos
SET saldo_restante = monto
WHERE saldo_restante IS NULL;

-- Calcular cuota mensual para préstamos existentes
-- Nota: Esta es una aproximación simple. En producción, se debería recalcular correctamente
UPDATE prestamos
SET cuota_mensual = CASE
    WHEN numero_de_cuotas > 0 THEN (monto * (1 + tasa_interes/100)) / numero_de_cuotas
    ELSE monto
END
WHERE cuota_mensual IS NULL;
