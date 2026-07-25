# Indexación de Estado que Cumple

La URL canónica vigente es `https://estadoquecumple.github.io/`. El sitemap es
`https://estadoquecumple.github.io/sitemap-index.xml`.

## Google Search Console

1. Agregar una propiedad de prefijo de URL para `https://estadoquecumple.github.io/`.
2. Elegir la verificación mediante archivo HTML y descargar el archivo que entrega Google.
3. Copiar ese archivo, sin renombrarlo ni modificarlo, a `public/googleXXXXXXXXXXXX.html`. El nombre mostrado aquí es solo el patrón de ubicación, no un token utilizable.
4. Ejecutar `npm run build`.
5. Publicar el resultado mediante GitHub Pages.
6. Comprobar que el archivo abre en `https://estadoquecumple.github.io/googleXXXXXXXXXXXX.html`.
7. Completar la verificación en Search Console.
8. Enviar `sitemap-index.xml`.
9. Solicitar inspección e indexación de la portada, `/cams/`, `/estado-que-cumple/`, el documento publicado y el Laboratorio Territorial.

No se debe retirar el archivo después de verificar. La auditoría comprueba que cualquier archivo real que coincida con el patrón de Google se copie intacto a `dist/`.

## Bing Webmaster Tools

Bing permite importar una propiedad ya verificada en Google Search Console. También puede agregarse directamente la URL y enviar el mismo sitemap. La importación y la validación son acciones manuales en las cuentas del propietario.

## IndexNow

1. Crear una clave real en el servicio elegido y guardarla como secreto `INDEXNOW_KEY`.
2. Ejecutar localmente `npm run indexnow:prepare` con `INDEXNOW_KEY` definido.
3. Publicar el archivo generado en la raíz del sitio.
4. Tras el despliegue, ejecutar manualmente el workflow **Notify IndexNow** o `npm run indexnow:submit`.

El host se deriva de `SITE_URL`, las URLs se leen del sitemap canónico y el envío se limita a 10.000 URLs. Sin una clave real, ambos comandos terminan sin fabricar ni enviar credenciales. El workflow no bloquea la publicación si IndexNow falla.

## Después de publicar

Comprobar con una sesión sin autenticar la portada, `robots.txt`, `sitemap-index.xml`, `sitemap-0.xml`, `site-index.json`, `llms.txt` y la imagen social. Search Console, Bing e IndexNow no garantizan inclusión ni posición: solo facilitan descubrimiento y diagnóstico.
