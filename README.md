# WhiteMoon Motor — demo de concesionario de coches y motos

Demo de WhiteMoon Agencia IA para concesionarios. Landing de una página con agente IA ("Nico") de 3 botones que responde, pivota ("esto te lo he respondido yo… ¿te interesa uno así?") y recoge nombre + teléfono.

**Negocio ficticio.** Sin precios, reseñas, cifras, marcas de coches ni matrículas. Los vehículos son fotos de archivo de Unsplash (ver `CREDITS.md`), no stock real. Teléfono, email y mapa son los de WhiteMoon. La página va con `noindex`.

## Estructura
- `index.html` — landing (Hero, Marquee, Sobre nosotros, Servicios, Stock de ejemplo, FAQ, Contacto) + JSON-LD (`AutoDealer`/`MotorcycleDealer`, `BreadcrumbList`, `FAQPage` igual al DOM).
- `assets/js/lead.js` — INSERT en `leads_web` (clave publicable, RLS) + aviso por `navigator.sendBeacon`. `origen='demo-concesionario'`, `sector='automovil'`.
- `assets/js/agente.js` — agente por botones. Cabecera "Asistente IA" (AI Act art. 50).
- `supabase/functions/concesionario-notify` — aviso a Telegram. Desplegada con `verify_jwt=false`; el token vive en Supabase Secrets, nunca en el cliente.
- `assets/js/site.js`, `assets/css/styles.css`, `assets/fonts/` — molde de las demos de WhiteMoon (Kanit autoalojada).

## Paleta
Fondo `#f6f4ef`, tinta `#14161a`, acento naranja `#c2410c` (texto blanco sobre él: contraste > 4,5:1), secundario `#9a3412`.

## Probar en local
`python3 -m http.server` en la raíz. Sin npm ni build.

## Pendiente
Pasar a un cliente real: sustituir las fotos de archivo por fotos propias del stock, revisar textos y FAQ con sus condiciones reales, quitar `noindex` y pasar la checklist legal de entrega.
