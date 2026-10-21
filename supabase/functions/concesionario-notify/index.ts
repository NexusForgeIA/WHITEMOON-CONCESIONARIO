import "jsr:@supabase/functions-js/edge-runtime.d.ts";

// concesionario-notify — notifica por Telegram un nuevo lead de la demo del concesionario
// (WHITEMOON-CONCESIONARIO). El lead ya se inserta en leads_web desde
// el cliente (origen='demo-concesionario'); esta función SOLO envía la notificación
// vía Telegram Bot API, manteniendo el token EXCLUSIVAMENTE server-side.
//
// Modelo "demo + pivote": el lead NO es una reserva de cita, es un
// PROSPECTO DE AGENCIA (dueño de un negocio que probó la demo). El tipo de
// negocio llega dentro de `mensaje` tras el prefijo "Tipo de negocio: "
// (lo fija assets/js/agente.js; si cambia allí, cambiarlo aquí).
//
// Recibe (POST JSON): { nombre, telefono, motivo, dia, hora, urgencia, origen }
// (reserva desde el chat) o { nombre, telefono, mensaje, origen } (prospecto).
// El cliente la llama con navigator.sendBeacon, que envía el cuerpo como
// Blob text/plain: por eso el parseo NO depende del Content-Type, se lee el
// texto y se intenta JSON.parse.
//
// Secrets usados (nunca en cliente):
//   - TELEGRAM_BOT_TOKEN : token del bot de Telegram
//   - TELEGRAM_CHAT_ID   : chat destino del aviso
//
// Regla del proyecto: si el envío falla → console.warn, nunca interrumpe nada.

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  const json = (body: unknown, status = 200) =>
    new Response(JSON.stringify(body), {
      status,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });

  let payload: Record<string, unknown> = {};
  try {
    const raw = await req.text();
    payload = raw ? JSON.parse(raw) : {};
  } catch {
    payload = {};
  }

  const data = (payload.args ?? payload) as Record<string, unknown>;
  const nombre = String(data.nombre ?? "").trim();
  const telefono = String(data.telefono ?? "").trim();
  const mensaje = String(data.mensaje ?? "").trim();
  const motivo = String(data.motivo ?? "").trim();
  const dia = String(data.dia ?? "").trim();
  const hora = String(data.hora ?? "").trim();
  const negocio = (mensaje.match(/Tipo de negocio:\s*(.+)$/)?.[1] ?? "").trim();
  const origen = String(data.origen ?? "concesionario-demo").trim();

  // Guard de lead incompleto — estándar WhiteMoon.
  if (!nombre || !telefono) {
    return json({ ok: false, error: "lead incompleto" }, 400);
  }

  // Dos formatos: reserva desde el chat de la demo (motivo + día + hora) o,
  // por compatibilidad, el prospecto de agencia de la versión anterior.
  const message = motivo || dia || hora
    ? `🔔 PRUEBA / CITA · demo del concesionario (${origen})\n` +
      `Nombre: ${nombre}\n` +
      `Teléfono: ${telefono}\n` +
      `Motivo: ${motivo || "-"}\n` +
      `Día: ${dia || "-"} · Hora: ${hora || "-"}`
    : `🔔 PROSPECTO DE AGENCIA · vino de la demo del concesionario (${origen})\n` +
      `Nombre: ${nombre}\n` +
      `Teléfono: ${telefono}\n` +
      `Tipo de negocio: ${negocio || "-"}`;

  let notified = false;
  try {
    const tgToken = Deno.env.get("TELEGRAM_BOT_TOKEN");
    const tgChat = Deno.env.get("TELEGRAM_CHAT_ID");
    if (tgToken && tgChat) {
      const r = await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: tgChat, text: message }),
      });
      notified = r.ok;
      if (!r.ok) {
        console.warn("[concesionario-notify] Telegram falló:", r.status, await r.text());
      }
    } else {
      console.warn("[concesionario-notify] sin TELEGRAM_BOT_TOKEN/CHAT_ID, mensaje:", message);
    }
  } catch (e) {
    console.warn("[concesionario-notify] error enviando Telegram:", e);
  }

  return json({ ok: true, notified });
});
