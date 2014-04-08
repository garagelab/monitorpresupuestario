# encoding: utf-8
import sys
import unicodecsv
import dataset

DB_CONNECTION_STRING = 'postgresql://manuel@localhost:5432/presupuesto'
CSV_FNAME = 'SIDIF.PROGRAMAS.2011.csv'

db = dataset.connect(DB_CONNECTION_STRING)
table = db['presupuesto_csv']

QUERY = """
create table jurisdiccion as
select distinct on ("Jurisdiccion ID") "Jurisdiccion ID"::integer as id, "Jurisdiccion" as nombre from presupuesto_csv;

create table caracter as
select distinct on ("Caracter ID") "Caracter ID"::integer as id, "Caracter" as nombre from presupuesto_csv;

create table programa as
select distinct on ("Programa ID") "Programa ID"::integer as id, "Programa" as nombre from presupuesto_csv;

create table saf as
select distinct on ("SAF ID") "SAF ID"::integer as id, "SAF" as nombre from presupuesto_csv;

alter table jurisdiccion add primary key (id);
alter table caracter add primary key (id);
alter table programa add primary key (id);
alter table saf add primary key (id);

create table ejecucion as
select
  id,
  to_date("Fecha", 'MM/DD/YY') as fecha,
  "URL",
  "Jurisdiccion ID"::integer as jurisdiccion_id,
  "SAF ID"::integer as saf_id,
  "Caracter ID"::integer as caracter_id,
  "Programa ID"::integer as programa_id,
  "Dia"::integer as dia,
  "Semana"::integer as semana,
  CASe WHEN "Dif Pagado" <> '*****' THEN "Dif Pagado"::float ELSE NULL END as dif_pagado,
  CASE WHEN "Dif Credito Vigente" <> '*****' THEN "Dif Credito Vigente"::float ELSE NULL END as dif_credito_vigente,
  CASE WHEN "Por Pagado" <> '*****' THEN "Por Pagado"::float ELSE NULL END as por_pagado,
  CASE WHEN "Credito Vigente" <> '*****' THEN "Credito Vigente"::float ELSE NULL END as credito_vigente,
  CASE WHEN "Dif Devengado" <> '*****' THEN "Dif Devengado"::float ELSE NULL END as dif_devengado,
  CASE WHEN "Flotante" <> '*****' THEN "Flotante"::float ELSE NULL END as flotante,
  CASE WHEN "Comprometido" <> '*****' THEN "Comprometido"::float ELSE NULL END as comprometido,
  CASE WHEN "Credito Vigente -1s" <> '*****' THEN "Credito Vigente -1s"::float ELSE NULL END as credito_vigente_semana_anterior,
  CASE WHEN "Pagado -1s" <> '*****' THEN "Pagado -1s"::float ELSE NULL END as pagado_semana_anterior,
  CASE WHEN "Credito 2010" <> '*****' THEN "Credito 2010"::float ELSE NULL END as credito_2010,
  CASE WHEN "Pagado" <> '*****' THEN "Pagado"::float ELSE NULL END as pagado,
  CASE WHEN "Por Flotante" <> '*****' THEN "Por Flotante"::float ELSE NULL END as por_flotante,
  CASE WHEN "Dif Comprometido" <> '*****' THEN "Dif Comprometido"::float ELSE NULL END as dif_comprometido,
  CASE WHEN "Por Sobrejecucion" <> '*****' THEN "Por Sobrejecucion"::float ELSE NULL END as por_sobrejecucion,
  CASE WHEN "Devengado -1s" <> '*****' THEN "Devengado -1s"::float ELSE NULL END as devengado_semana_anterior,
  CASE WHEN "Credito 2011" <> '*****' THEN "Credito 2011"::float ELSE NULL END as credito_2011,
  CASE WHEN "Devengado" <> '*****' THEN "Devengado"::float ELSE NULL END as devengado,
  CASE WHEN "Por Ejecutado" <> '*****' THEN "Por Ejecutado"::float ELSE NULL END as por_ejecutado,
  CASE WHEN "Cargos" <> '*****' THEN "Cargos"::float ELSE NULL END as cargos,
  CASE WHEN "Comprometido -1s" <> '*****' THEN "Comprometido -1s"::float ELSE NULL END as comprometido_semana_anterior
from presupuesto_csv;

alter table ejecucion add constraint jurisdiccion_fkey foreign key (jurisdiccion_id) references jurisdiccion (id);
alter table ejecucion add constraint saf_fkey foreign key (saf_id) references saf (id);
alter table ejecucion add constraint programa_fkey foreign key (programa_id) references programa (id);
alter table ejecucion add constraint caracter_fkey foreign key (caracter_id) references caracter (id);
alter table ejecucion add primary key (id);
"""

r = unicodecsv.DictReader(open(CSV_FNAME))

print >>sys.stderr, "Importando %s a la base de datos" % (CSV_FNAME)
for p in r:
    table.insert(p)

print >>sys.stderr, "Normalizando tablas"
db.query(QUERY)

print >>sys.stderr, "Listo."
