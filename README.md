# Sistema de Liquidación de Nómina - Guía Técnica

## Descripción General

### Propósito del sistema:
El sistema tiene como objetivo realizar la liquidación de salarios, bonificaciones, deducciones y novedades según la normativa laboral colombiana. Abarca el cálculo de salarios base, auxilio de transporte, horas extras, incapacidades, préstamos y otras deducciones, generando reportes detallados para cumplir con las obligaciones legales y laborales.

### Alcance:
El sistema cubre las siguientes áreas:
- Cálculo de variables salariales.
- Gestión de novedades legales (incapacidades, calamidad doméstica, festivos, ausencias, etc.).
- Cálculo de préstamos y ahorros.
- Generación de reportes (PDF, Excel) con el desglose de salarios y cumplimiento de las normativas colombianas.

---

## Variables de Entrada

### Datos Base del Empleado:
1. **salario_base** (numérico, varía por cargo): Salario mensual base del empleado.
2. **auxilio_transporte** (numérico, según ley vigente): Auxilio de transporte, determinado por la ley actual.
3. **cargo** (texto, determina salario y bonificaciones): Cargo o puesto del empleado, utilizado para determinar su salario base y bonificaciones.

### Agenda y Novedades:
1. **horarios** (lista de días/horas laborales): Información de los días y horas laborales del empleado.
2. **novedades** (lista con tipo, fechas y horas afectadas): Incluye tipos de novedades como incapacidad, calamidad, festivos, ausencias, entre otras.
3. **horas_extras** (cantidad y tipo: diurnas/nocturnas/festivas): Detalles de horas extras trabajadas, clasificados según el tipo (diurnas, nocturnas, festivas).

### Deducciones:
1. **prestamos** (monto, cuotas, tasa de interés 6%): Préstamos del empleado, indicando el monto, el número de cuotas y la tasa de interés (6% anual).
2. **ahorros** (monto fijo o porcentual): Ahorros del empleado, que pueden ser un monto fijo o un porcentaje de su salario.

---

## Variables de Salida

1. **salario_neto**: Salario del empleado después de aplicar las deducciones y bonos.
2. **desglose_pago**: Detalle de las horas extras, bonos, auxilio de transporte y deducciones.
3. **reporte_legal**: Reporte con el cumplimiento de las normativas laborales en el cálculo de la liquidación.

---

## Fórmulas y Cálculos

### Día de Trabajo:
Para calcular el valor de un día de trabajo:

$$
\text{valor dia} = \frac{\text{salario base}}{30}
$$

---

## Incapacidad y Calamidad

### Salario por incapacidad:
Para calcular el salario por incapacidad:

$$
\text{salario} = \text{días de incapacidad} \times \text{valor dia}
$$

## Préstamos

### Cálculo de cuota mensual

```math
cuota\_mensual = \frac{monto\_prestamo \times (1 + 0.06)}{cuotas\_restantes}
```

Esto permite calcular la cuota mensual a descontar del salario, considerando el interés del 6% anual.

## Horas Extras

### Para calcular el pago por horas extras:

#### Diurnas
```math
valor\_hora\_extra = valor\_hora \times 1.25
```

#### Nocturnas
```math
valor\_hora\_extra = valor\_hora \times 1.75
```

#### Festivas
```math
valor\_hora\_extra = valor\_hora \times 2.5
```

### Cálculo del valor de la hora
```math
valor\_hora = \frac{salario\_base}{240}
```
Esto supone una jornada de 8 horas diarias y 30 días laborales al mes.

## Flujo del Proceso

1. **Carga de agenda inicial (horarios base):** Establecer los días y horas laborales del empleado.
2. **Registro de novedades:** Se validan los tipos de novedades (incapacidad, festivo, etc.) y las fechas/horas afectadas.
3. **Ajuste de agenda por festivos:** Los festivos son identificados y compensados automáticamente, ya sea con pago doble o con tiempo compensatorio.
4. **Aprobación manual de horas extras:** El supervisor valida y aprueba las horas extras a través de una interfaz.
5. **Cálculo automático de salario, bonos y deducciones:** El sistema calcula el salario neto considerando las horas extras, bonificaciones y deducciones.
6. **Generación de reportes:** El sistema genera un reporte detallado (PDF/Excel) que incluye todos los cálculos realizados, destacando el cumplimiento de las normativas legales.

## Consideraciones Legales Explícitas

- **Ley 52 de 1975 (Festivos):** El pago por trabajo en festivos debe ser el doble del salario regular o con compensación de tiempo.
- **Decreto 1072 de 2015 (Auxilio de Transporte):** El auxilio de transporte se debe descontar proporcionalmente durante las incapacidades.
- **Código Sustantivo del Trabajo (Art. 134):** La calamidad doméstica debe ser tratada con 5 días de salario pagos.
- **Intereses por Préstamos:** El interés por los préstamos no puede superar el 6% anual, de acuerdo con el Art. 884 del Código de Comercio.

## Especificaciones Técnicas

### Validación de Datos

- El sistema debe validar que los tipos de novedades sean correctos (por ejemplo, no se permiten vacaciones en días festivos).
- Validación de la duración de las incapacidades, asegurando que no se computen días festivos o no laborales.

### Persistencia

- El sistema debe almacenar el historial de las liquidaciones por un periodo mínimo de 10 años, según la Ley 527 de 1999.

### Interfaces

- El sistema debe ofrecer una API para integración con sistemas contables externos, permitiendo el intercambio de datos para la contabilidad y la auditoría.

# Fondo de Solidaridad Pensional (FSP)

El **Fondo de Solidaridad Pensional (FSP)** es una deducción aplicada a trabajadores con ingresos superiores a un umbral establecido por ley, destinada a subsidiar pensiones de personas con menores ingresos. Su cálculo se rige por el **Estatuto Tributario (Ley 1819 de 2016)** y se actualiza anualmente según la **Unidad de Valor Tributario (UVT)**.  

A continuación, te explicamos cómo se calcula el FSP en 2025:

---

##  Umbrales y porcentajes

| **Rango de ingresos**       | **Porcentaje de deducción**  |
|-----------------------------|----------------------------:|
| Más de 4 UVT hasta 16 UVT   | 1% sobre el excedente       |
| Más de 16 UVT               | 2% sobre el excedente       |

---

## Pasos para calcular el FSP en 2025

### 1. Obtener el valor de la UVT 2025  
- La **UVT** se ajusta anualmente según el **Índice de Precios al Consumidor (IPC)**.  
- En **2025**, 1 UVT = **$49,799 COP** *(ejemplo ilustrativo; para 2025, consulta el valor oficial en el **DIAN**).*
- **Ejemplo hipotético:** Supongamos que en **2025**, **1 UVT = $49,700 COP**.

---

### 2. Calcular los umbrales en pesos  
- **4 UVT** = 4 × 49,700 = **198,800 COP**  
- **16 UVT** = 16 × 49,700 = **795,200 COP**  

---

### 3. Aplicar los porcentajes según el salario  
Si el salario es **$1,000,000 COP** *(ejemplo):*
- **Excedente sobre 4 UVT:**  
  1,000,000 - 198,800  = **$801,200**  
- **Excedente sobre 16 UVT:**  
  1,000,000 - 795,200 = **$204,800**  

---

## Cálculo del FSP  
- **1% sobre (801,200 - 204,800):**  
  596,400 × 1% = **5,964 COP**  
- **2% sobre (204,800):**  
  204,800 × 2% = **4,096 COP**  

** Total FSP: 5,964 + 4,096 = $10,060 COP**  

---
  
## Ejemplo de Caso de Uso

**Empleado con las siguientes características:**
- Salario base: $3,000,000
- Auxilio de transporte: $140,000
- 2 días de incapacidad
- 1 préstamo de $1,000,000 con 6% de interés y 12 cuotas
- 5 horas extras diurnas

### Cálculo paso a paso

#### Valor del día
```math
valor\_día = \frac{salario\_base}{30} = \frac{3,000,000}{30} = 100,000
```

#### Salario por incapacidad (2 días)
```math
salario\_incapacidad = días\_incapacidad \times valor\_día = 2 \times 100,000 = 200,000
```

#### Deducción por auxilio de transporte durante la incapacidad
```math
deducción\_auxilio = \frac{auxilio\_transporte}{30} \times días\_incapacidad = \frac{140,000}{30} \times 2 = 9,333.33
```

#### Cuota mensual de préstamo
```math
cuota\_mensual = \frac{monto\_prestamo \times (1 + 0.06)}{cuotas\_restantes} = \frac{1,000,000 \times 1.06}{12} = 88,333.33
```

#### Horas extras diurnas (5 horas)
```math
valor\_hora = \frac{salario\_base}{240} = \frac{3,000,000}{240} = 12,500
```
```math
valor\_hora\_extra = valor\_hora \times 1.25 = 12,500 \times 1.25 = 15,625
```
```math
total\_horas\_extras = 5 \times 15,625 = 78,125
```

#### Salario neto
```math
salario\_neto = 3,000,000 - 200,000 - 9,333.33 - 88,333.33 + 78,125 = 2,780,458.34
