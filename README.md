# Monitor ejecución presupuestaria (experimento)

## Instalación

1. Crear un `virtualenv`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Bajar datos: `wget -O SIDIF.PROGRAMAS.2011.csv "https://www.google.com/fusiontables/exporttable?query=select+*+from+1VgJStdD87j8tJ4-Ngn_HiRPU7c3YqxrcaoIvqQ"`
4. Modificar parámetros de conexión a la DB (variable `DB_CONNECTION_STRING` en `import_csv.py`)
5. Importar datos a la DB: `python import_csv.py`

## Ejecutar el server OLAP

  slicer serve --debug slicer.ini

## Consultas de ejemplo

 - http://localhost:5000/cube/ejecucion/aggregate?drilldown=fecha@monthly&cut=fecha@monthly:2011|jurisdiccion:Poder%20Legislativo%20Nacional
 - http://localhost:5000/cube/ejecucion/aggregate?drilldown=fecha@monthly:month
 - http://localhost:5000/cube/ejecucion/aggregate?drilldown=fecha@monthly:month&cut=jurisdiccion:Poder%20Legislativo%20Nacional
 - http://localhost:5000/cube/ejecucion/aggregate?drilldown=fecha@monthly:month&cut=jurisdiccion:Poder%20Legislativo%20Nacional|saf:Defensoria%20del%20Pueblo
