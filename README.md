
```markdown
# Proyecto de Obtención de Datos Históricos y Información de Acciones y Carga en Amazon Redshift

Este proyecto te permite obtener datos históricos de precios de acciones, así como información detallada de las empresas detrás de esas acciones, utilizando Python y cargarlos en una base de datos Amazon Redshift. A continuación, encontrarás una guía para utilizar este código de manera efectiva.

## Contenido

1. [Requisitos](#requisitos)
2. [Instrucciones de Configuración](#instrucciones-de-configuración)
3. [Ejecución del Código](#ejecución-del-código)
4. [Contribuciones](#contribuciones)
5. [Licencia](#licencia)

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

## Ejecución del Código

1. Ejecuta el script Python principal para obtener los datos históricos de precios de acciones y cargarlos en la base de datos Redshift:

   ```bash
   python main.py
   ```

2. Sigue las instrucciones y mensajes en la consola para monitorear el progreso y los resultados de la ejecución.

## Contribuciones

Si deseas contribuir a este proyecto, siéntete libre de crear un pull request o informar sobre problemas. Apreciamos tu contribución.

## Licencia

Este proyecto está bajo la licencia [LICENSE](LICENSE).

¡Disfruta utilizando este código para obtener datos históricos de acciones y cargarlos en Amazon Redshift!

