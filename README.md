
```markdown
# Proyecto de Obtención de Datos Históricos y Información de Acciones y Carga en Amazon Redshift

Este proyecto te permite obtener datos históricos de precios de acciones, así como información detallada de las empresas detrás de esas acciones, utilizando Python y cargarlos en una base de datos Amazon Redshift. A continuación, encontrarás una guía para utilizar este código de manera efectiva.

## Contenido

1. [Requisitos](#requisitos)
2. [Instrucciones de Configuración](#instrucciones-de-configuración)
3. [Origen de los Datos]
4. [Tipo de Datos]
5. [Finalidad del Proyecto]
6. [Ejecución del Código](#ejecución-del-código)
7. [Contribuciones](#contribuciones)
8. [Licencia](#licencia)

## Requisitos

Asegúrate de tener instalado lo siguiente antes de utilizar el código:

- Python 3
- Paquetes Python: `yfinance`, `pandas`, `configparser`, `psycopg2`
- Una base de datos Amazon Redshift configurada

## Instrucciones de Configuración

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/arturobritezadaime/Proyecto-yFinance-Redshift.git
   ```

2. Incorpora el archivo `config.ini` en la raíz del proyecto y configura tus credenciales y detalles de conexión de la siguiente manera:

   ```ini
   [fechas]
   fecha_inicio = yyyy-mm-dd
   
   [empresas]
   #lista = [["AAPL", "Apple"], ["GOOGL", "Alphabet"]] # Ejemplo corto
   lista =[["MMM", "3M"], ["AOS", "A. O. Smith"], ["ABT", "Abbott Laboratories"], ["ABBV", "AbbVie"], ["ABMD", "Abiomed"], ["ACN", "Accenture"], ["ATVI", "Activision Blizzard"], ["ADM", "ADM"], ["ADBE", "Adobe"], ["AAP", "Advance Auto Parts"], ["AMD", "Advanced Micro Devices"], ["AES", "AES Corp"], ["AFL", "Aflac"], ["A", "Agilent Technologies"], ["APD", "Air Products & Chemicals"]]

   [alpha_vantage]
   api_key = 'EJEMPLO_API_KEY'
   
   [redshift]
   user = ejemplo-user
   password = ejemplo-password 
   host = host.redshift.amazonaws.com
   port = 5439
   database = ejemplo-database
   ```

3. Configura tu nombre de usuario y dirección de correo electrónico en Git para que los commits tengan tu identidad:

   ```bash
   git config --global user.email "tucorreo@example.com"
   git config --global user.name "Arturo Britez Adaime"
   ```
## Origen de los Datos
Los datos se obtienen de dos fuentes principales:

Alpha Vantage: Proporciona información detallada de las empresas, como nombre, sector, industria, etc.
Yahoo Finance: Ofrece datos históricos de precios de acciones.
## Tipo de Datos
Información de Empresas (Dimensión Acciones): Incluye el símbolo de la acción, nombre de la empresa, sector, industria y otros detalles.
Datos Históricos de Precios (Hechos Precio Acciones): Contiene información sobre la apertura, cierre, máximo, mínimo, volumen, dividendos y divisiones de acciones.
## Finalidad del Proyecto
La finalidad de este proyecto es proporcionar una herramienta automatizada para obtener y almacenar datos históricos y detalles de empresas en una base de datos Redshift, facilitando el análisis y la toma de decisiones relacionadas con acciones financieras.
## Ejecución del Código

1. Ejecuta el script Python principal para obtener los datos históricos de precios de acciones y cargarlos en la base de datos Redshift:

   ```bash
   python main.py
   ```

2. Sigue las instrucciones y mensajes en la consola para monitorear el progreso y los resultados de la ejecución.
## Estructura del Proyecto
* Main.py: Script principal para la obtención de datos históricos y la carga en Amazon Redshift. Utiliza bibliotecas como yfinance, pandas, y requests. Coordina las operaciones con los módulos Carga.py y Conexion_Creacion_Tablas.py.

* Carga.py: Módulo encargado de la carga de diferentes tipos de datos en Amazon Redshift. Contiene funciones específicas para cargar datos de acciones, fechas y precios de acciones en las tablas correspondientes, gestionando la lógica de redondeo y la gestión de duplicados. Además, implementa el registro de eventos a través de logging para un seguimiento detallado.

* Conexion_Creacion_Tablas.py: Módulo para la conexión a Amazon Redshift y creación de tablas utilizando sentencias SQL definidas en Codigo_SQL.sql. Utiliza la biblioteca psycopg2 para la conexión a la base de datos.

* Codigo_SQL.sql: Contiene sentencias SQL para la creación de tablas en Amazon Redshift, definiendo las tablas para el área de staging (stock_data_staging), la Dimensión Fecha (Dim_Fecha), la Dimensión Acción (Dim_Accion), y la tabla de hechos (Fac_Precio_Acciones).
* Documentación principal del proyecto. Proporciona instrucciones detalladas sobre la configuración, ejecución del código y la estructura del proyecto.
## Contribuciones

Si deseas contribuir a este proyecto, siéntete libre de crear un pull request o informar sobre problemas. Apreciamos tu contribución.

## Licencia

Este proyecto está bajo la licencia [LICENSE](LICENSE).

¡Disfruta utilizando este código para obtener datos históricos de acciones y cargarlos en Amazon Redshift!

