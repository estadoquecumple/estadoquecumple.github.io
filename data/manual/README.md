# Importaciones manuales del Laboratorio Territorial

El pipeline nunca sustituye una fuente ausente con cifras simuladas. Descargue únicamente archivos oficiales, conserve el nombre original y registre URL, fecha, vigencia y SHA-256.

Ubicaciones reconocidas:

- `population.xlsx`: proyecciones municipales DANE 2018–2042. Debe contener código DIVIPOLA, año y población.
- `dnp_typologies_2026.xlsx`: base y diccionario DNP; siete tipologías municipales/distritales y tres departamentales.
- `dnp_idf_2024.xlsx`: resultados oficiales del Índice de Desempeño Fiscal, vigencia 2024.
- `dnp_mdm.xlsx`: edición oficial más reciente metodológicamente comparable.

Ejecute `python scripts/territorial/fetch_all.py --offline` para procesar lo disponible y mantener `manual-required` en lo ausente. Los rechazos se escriben en `data/rejected/`; no se imputan silenciosamente. SisPT/TerriData solo se incorpora cuando exista una descarga estable, nunca mediante automatización de Power BI.
