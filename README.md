# NetVelocityMeter

NetVelocityMeter - Herramienta de Medición de Velocidad de Internet

Uso:
  net_velocity_meter [OPCIONES]

Opciones:
  --verbose         Mostrar información detallada.
  --continuous INT  Realizar mediciones continuas con el número de mediciones especificado.
  --interval INT    Intervalo en segundos entre mediciones continuas (por defecto: 60).
  --output PATH     Guardar los resultados en un archivo CSV.
  --plot            Generar un gráfico de las mediciones.
  --connections STR Tipos de conexiones a medir (ej: wifi ethernet).

Descripción:
  NetVelocityMeter es una herramienta de línea de comandos que permite medir la velocidad de Internet y el ping. Puede ejecutarse en modo continuo para realizar mediciones automáticas a intervalos específicos. Los resultados pueden guardarse en un archivo CSV y se pueden generar gráficos utilizando la biblioteca Seaborn.

Opciones:
  --verbose
      Mostrar información detallada durante la ejecución del programa, incluyendo detalles de cada medición.

  --continuous INT
      Realizar mediciones continuas durante un número especificado de veces. Las mediciones se realizarán en intervalos definidos por la opción --interval. Si esta opción se omite, se realizará una sola medición.

  --interval INT
      Establecer el intervalo en segundos entre mediciones continuas. Por defecto, el intervalo es de 60 segundos.

  --output PATH
      Guardar los resultados de las mediciones en un archivo CSV. Se puede especificar la ruta del archivo de salida.

  --plot
      Generar un gráfico de las mediciones utilizando la biblioteca Seaborn. El gráfico mostrará las tendencias de velocidad y ping a lo largo del tiempo.

  --connections STR
      Especificar los tipos de conexiones a medir, separados por espacios. Por ejemplo: --connections wifi ethernet. Por defecto, se medirá la conexión por defecto.

Ejemplos:
  1. Realizar una medición única de velocidad y ping:
      net_velocity_meter

  2. Realizar 5 mediciones continuas cada 30 segundos y guardar los resultados en un archivo CSV:
      net_velocity_meter --continuous 5 --interval 30 --output results.csv

  3. Realizar mediciones en las conexiones Wi-Fi y Ethernet y generar un gráfico:
      net_velocity_meter --connections wifi ethernet --plot

     
