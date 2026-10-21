# WhiteMoon Motor — demo de concesionario (coches y motos)

Demo de WhiteMoon Agencia IA. Negocio **ficticio**: sin precios, cifras, reseñas ni stock real.

- HTML/CSS/JS vanilla, GitHub Pages. Frontend heredado de la demo de clínicas dentales (capa holográfica CSS, `holo.js`), paleta azul marino + naranja.
- Asistente **Nico** (`assets/js/watio.js`): elige servicio → día → hora → nombre → teléfono. Guarda en Supabase `leads_web` (`origen='concesionario-demo'`, `sector='Concesionario'`) y avisa por Telegram vía Edge Function `concesionario-notify` (secretos en Supabase Secrets).
- Despliegue de la función: `supabase functions deploy concesionario-notify --no-verify-jwt --project-ref mlaqtniujnvfxcvcourm`.
- Fotos: ver `CREDITS.md`.
- Local: `python3 -m http.server`.
