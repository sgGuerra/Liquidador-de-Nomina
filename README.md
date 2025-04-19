# Sistema de Liquidación de Nómina - Guía Técnica

## Autores

- Santiago Alcaraz Durango
- Luis Carlos Guerra Herrera 
## Descripción General

### Propósito del sistema:
El sistema tiene como objetivo realizar la liquidación de salarios, bonificaciones, deducciones y novedades según la normativa laboral colombiana. Abarca el cálculo de salarios base, auxilio de transporte, horas extras, préstamos y otras deducciones, generando reportes detallados para cumplir con las obligaciones legales y laborales.

### Alcance:
El sistema cubre las siguientes áreas:
- Cálculo de variables salariales.
- Gestión de novedades legales (horas extras).
- Cálculo de préstamos y deducciones legales.
- Generación de reportes (PDF, Excel) con el desglose de salarios y cumplimiento de las normativas colombianas.


## Variables de Entrada

### Datos Base del Empleado:
1. **salario_base** (numérico, varía por cargo): Salario mensual base del empleado.
2. **auxilio_transporte** (numérico, según ley vigente): Auxilio de transporte, determinado por la ley actual.
3. **cargo** (texto, determina salario y bonificaciones): Cargo o puesto del empleado, utilizado para determinar su salario base y bonificaciones.

### Agenda y Novedades:
1. **horarios** (lista de días/horas laborales): Información de los días y horas laborales del empleado.
3. **horas_extras** (cantidad y tipo: diurnas/nocturnas/festivas): Detalles de horas extras trabajadas, clasificados según el tipo (diurnas, nocturnas, festivas).

### Deducciones:
1. **prestamos** (monto, cuotas, tasa de interés 6%): Préstamos del empleado, indicando el monto, el número de cuotas y la tasa de interés (6% anual).



## Variables de Salida

1. **salario_neto**: Salario del empleado después de aplicar las deducciones y bonos.
2. **desglose_pago**: Detalle de las horas extras, bonos, auxilio de transporte y deducciones.
3. **reporte_legal**: Reporte con el cumplimiento de las normativas laborales en el cálculo de la liquidación.



## Fórmulas y Cálculos

### Día de Trabajo:
Para calcular el valor de un día de trabajo:

$$
\text{valor dia} = \frac{\text{salario base}}{30}
$$



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

## Fondo de Solidaridad Pensional (FSP)

El **Fondo de Solidaridad Pensional (FSP)** es una deducción aplicada a trabajadores con ingresos superiores a un umbral establecido por ley, destinada a subsidiar pensiones de personas con menores ingresos. Su cálculo se rige por el **Estatuto Tributario (Ley 1819 de 2016)** y se actualiza anualmente según la **Unidad de Valor Tributario (UVT)**.  

A continuación, te explicamos cómo se calcula el FSP en 2025:

---

###  Umbrales y porcentajes

| **Rango de ingresos**       | **Porcentaje de deducción**  |
|-----------------------------|----------------------------:|
| Más de 4 UVT hasta 16 UVT   | 1% sobre el excedente       |
| Más de 16 UVT               | 2% sobre el excedente       |

---

### Pasos para calcular el FSP en 2025

#### 1. Obtener el valor de la UVT 2025  
- La **UVT** se ajusta anualmente según el **Índice de Precios al Consumidor (IPC)**.  
- En **2025**, 1 UVT = **$49,799 COP** *(ejemplo ilustrativo; para 2025, consulta el valor oficial en el **DIAN**).*
- **Ejemplo hipotético:** Supongamos que en **2025**, **1 UVT = $49,700 COP**.

---

#### 2. Calcular los umbrales en pesos  
- **4 UVT** = 4 × 49,700 = **198,800 COP**  
- **16 UVT** = 16 × 49,700 = **795,200 COP**  

---

#### 3. Aplicar los porcentajes según el salario  
Si el salario es **$1,000,000 COP** *(ejemplo):*
- **Excedente sobre 4 UVT:**  
  1,000,000 - 198,800  = **$801,200**  
- **Excedente sobre 16 UVT:**  
  1,000,000 - 795,200 = **$204,800**  

---

### Cálculo del FSP  
- **1% sobre (801,200 - 204,800):**  
  596,400 × 1% = **5,964 COP**  
- **2% sobre (204,800):**  
  204,800 × 2% = **4,096 COP**  

** Total FSP: 5,964 + 4,096 = $10,060 COP**  


## Especificaciones Técnicas

### Validación de Datos

- El sistema debe validar que los tipos de novedades sean correctos (por ejemplo, no se permiten ingresar horas extras negativas).
- Validación de sobre el tipo de horas extras y cargos

### Persistencia

- El sistema debe almacenar el historial de las liquidaciones por un periodo, según la Ley 527 de 1999.

### Interfaces

- El sistema debe ofrecer una interfaz grafica web.


  
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
```



## Documentación para la ejecución del programa y pruebas unitarias

### Pasos para ejecutar el programa `main.py` desde la terminal de Windows:

1. **Abrir la terminal de Windows**:
  - Presiona `Win + R`, escribe `cmd` y presiona `Enter`.

2. **Navegar al directorio del proyecto**:
  - Utiliza el comando `cd` para cambiar al directorio donde se encuentra el archivo `main.py`. Por ejemplo:
    ```sh
    cd d:\Documentos\Programación\Proyectos\Liquidador-de-Nomina
    ```

3. **Ejecutar el programa**:
  - Una vez en el directorio correcto, ejecuta el programa con el siguiente comando:
    ```
    python src/view/console/main.py
    ```

### Pasos para ejecutar las pruebas unitarias `test_nomina.py`:

1. **Abrir la terminal de Windows**:
  - Presiona `Win + R`, escribe `cmd` y presiona `Enter`.

2. **Navegar al directorio del proyecto**:
  - Utiliza el comando `cd` para cambiar al directorio donde se encuentra el archivo `test_nomina.py`. Por ejemplo:
    ```sh
    cd d:\Documentos\Programación\Proyectos Pycharm\Liquidador de Nomina\Liquidador-de-Nomina
    ```

3. **Ejecutar las pruebas unitarias**:
  - Asegúrate de tener `unittest` disponible. Es parte de la biblioteca estándar de Python, por lo que no necesitas instalar nada adicional.
  - Una vez en el directorio correcto, ejecuta las pruebas unitarias con el siguiente comando:
    ```sh
    python test/test_nomina.py
    ```
  - `unittest` buscará y ejecutará las pruebas definidas en `test_nomina.py` y mostrará los resultados en la terminal.


## Arquitectura del Proyecto

El proyecto está organizado en una estructura de carpetas que facilita la separación de responsabilidades y la mantenibilidad del código. A continuación se describe la organización de los módulos y las bibliotecas utilizadas:

#### Estructura de Carpetas

```
Liquidador-de-Nomina/
│
├── src/
│   ├── model/
│   │   ├── calculo_nomina.py
│   │   ├── excepciones.py
│   │   └── __init__.py
│   ├── view/
│   |    ├── console/
│   |        ├── main.py
│   |        └── __init__.py
|   |
│   └── __init__.py
│   
│
├── test/
│   ├── test_nomina.py
│   └── __init__.py
│
├── .gitignore
├── LICENSE.txt
├── Liquidador-de-Nómina.xlsx
├── README.md
└── requirements.txt

```

#### Descripción de Carpetas y Archivos

- **src/**: Contiene el código fuente del proyecto.
  - **model/**: Incluye la lógica de negocio y las clases principales.
    - `calculo_nomina.py`: Contiene la clase `Nomina` y las funciones para calcular el salario, horas extras, bonificaciones, etc.
    - `excepciones.py`: Define las excepciones personalizadas utilizadas en el proyecto.
  - **view/**: Contiene las interfaces de usuario.
    - **console/**: Incluye la interfaz de consola para interactuar con el usuario.
      - `main.py`: Implementa la lógica de la consola para la entrada y salida de datos.
- **test/**: Contiene las pruebas unitarias.
  - `test_nomina.py`: Incluye las pruebas unitarias para la clase `Nomina` y sus métodos.
- `README.md`: Documentación del proyecto.
- `requirements.txt`: Lista de dependencias y bibliotecas necesarias para ejecutar el proyecto.

### Bibliotecas Usadas

- **unittest**: Biblioteca estándar de Python para realizar pruebas unitarias.
- **sys**: Biblioteca estándar de Python para manipular el entorno de ejecución.

### Dependencias

El proyecto no tiene dependencias externas adicionales a las bibliotecas estándar de Python. Todas las funcionalidades se implementan utilizando las bibliotecas estándar y el código propio del proyecto(por el momento).

### Organización de Módulos

- **model**: Contiene la lógica y las clases.
- **view**: Contiene las interfaces de usuario, en este caso, una interfaz de consola.
- **test**: Contiene las pruebas unitarias para asegurar la calidad del código.

Esta organización modular permite una fácil extensión y mantenimiento del proyecto, asegurando que cada componente tenga una responsabilidad clara y definida.


Perfecto, entonces actualizo el `README.md` para que la instrucción de ejecución sea clara con la nueva ruta del archivo principal (`src/view/console/GUI.py`). Aquí tienes la versión actualizada:

---

# Liquidador de Nómina (Kivy)

Aplicación gráfica desarrollada en **Python + Kivy** para calcular la nómina de un empleado según diferentes parámetros como salario base, horas extras, tipo de hora, préstamos, cuotas e intereses.

---

## Requisitos

- Python 3.7 o superior
- Kivy (`pip install kivy`)
---

## Instrucciones para ejecutar

1. **Clona o descarga el proyecto**

2. **Instala las dependencias**

```bash
pip install kivy
```

3. **Ejecuta la aplicación**

Desde la raíz del proyecto, corre:

```bash
python src/view/GUI/GUI.py
```

---


## Autores interfaz

- Mileidy Vanegas
- Miguel Martínez
---
