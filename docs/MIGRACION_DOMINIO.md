# Migración futura de dominio

No hay un dominio propio seleccionado ni configurado. Las alternativas que deben evaluarse son `estadoquecumple.co` y `estadoquecumple.com.co`. Hasta que una exista y esté conectada, el canonical sigue siendo `https://estadoquecumple.github.io/`.

## Lista exacta de migración

1. Registrar el dominio.
2. Decidir el dominio canónico.
3. Si se compran ambos, configurar uno para redirigir al otro.
4. Verificar el dominio en la organización GitHub.
5. Configurar el dominio personalizado en GitHub Pages.
6. Configurar DNS según los valores vigentes indicados por GitHub.
7. Cambiar `SITE_URL`.
8. Regenerar canonical, sitemap, robots, Open Graph y JSON-LD desde la fuente central.
9. Mantener exactamente las mismas rutas.
10. Verificar la propiedad nueva en Search Console.
11. Verificar o conservar verificada la propiedad antigua.
12. Comprobar redirecciones de cada URL antigua a su equivalente.
13. Usar Cambio de dirección de Search Console si la propiedad es elegible.
14. Enviar el sitemap nuevo.
15. Mantener las redirecciones al menos 180 días.
16. Conservar la propiedad antigua para monitoreo.
17. Actualizar Bing e IndexNow.
18. No rediseñar la estructura y cambiar el dominio simultáneamente.

## Correspondencia que debe conservarse

| URL antigua | URL nueva |
| --- | --- |
| `https://estadoquecumple.github.io/` | `https://DOMINIO-NUEVO/` |
| `https://estadoquecumple.github.io/cams/` | `https://DOMINIO-NUEVO/cams/` |
| `https://estadoquecumple.github.io/estado-que-cumple/` | `https://DOMINIO-NUEVO/estado-que-cumple/` |
| `https://estadoquecumple.github.io/documentos/estado-que-cumple-2026-2030/` | `https://DOMINIO-NUEVO/documentos/estado-que-cumple-2026-2030/` |
| `https://estadoquecumple.github.io/observatorio/laboratorio-territorial/` | `https://DOMINIO-NUEVO/observatorio/laboratorio-territorial/` |
| cualquier otra ruta `/RUTA/` | `https://DOMINIO-NUEVO/RUTA/` |

Comprobaciones iniciales:

```powershell
Invoke-WebRequest -Method Head https://estadoquecumple.github.io/
Invoke-WebRequest -Method Head https://DOMINIO-NUEVO/
```

Debe verificarse además cada par con una solicitud que permita observar la cadena completa de redirecciones y el código final. El cambio de `SITE_URL` se hace en el entorno de compilación; no se deben reemplazar hosts a mano en componentes.
