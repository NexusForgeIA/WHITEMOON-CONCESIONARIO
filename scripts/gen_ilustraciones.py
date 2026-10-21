#!/usr/bin/env python3
"""Genera las ilustraciones de la demo (SVG propios, sin marcas ni matrículas).

Coches y motos genéricos dibujados a mano en código: no representan ningún
modelo real. Salida en assets/img/. Uso:  python3 scripts/gen_ilustraciones.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
INK = "#14161a"

# ------------------------------------------------------------------ utilidades
def shade(hexc, k):
    h = hexc.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    f = lambda v: max(0, min(255, round(v * k)))
    return "#%02x%02x%02x" % (f(r), f(g), f(b))


def lite(hexc, k):
    h = hexc.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    f = lambda v: max(0, min(255, round(v + (255 - v) * k)))
    return "#%02x%02x%02x" % (f(r), f(g), f(b))


_gid = [0]


def grad(color):
    """Degradado vertical del color de carrocería; devuelve (defs, url)."""
    _gid[0] += 1
    i = "g%d" % _gid[0]
    d = ('<linearGradient id="%s" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
         % (i, lite(color, .18), shade(color, .78)))
    return d, "url(#%s)" % i


GLASS = "#cfd9e2"

# ------------------------------------------------------------------------ coche
# a: base trasera de la cabina · b: techo trasero · c: techo delantero · d: base delantera · h: altura del techo
CARS = {
    "urbano":   dict(a=72,  b=104, c=232, d=282, h=-106, hood=384),
    "berlina":  dict(a=84,  b=128, c=238, d=292, h=-102, hood=394),
    "suv":      dict(a=60,  b=70,  c=262, d=312, h=-124, hood=392),
    "coupe":    dict(a=100, b=156, c=226, d=294, h=-98,  hood=396),
    "familiar": dict(a=44,  b=50,  c=268, d=316, h=-118, hood=390),
}


def wheel(cx, cy, r, rim="#c9ced4"):
    spokes = "".join(
        '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>'
        % (cx, cy, cx + round((r * .66) * __import__("math").cos(i * 1.2566 + .3)),
           cy + round((r * .66) * __import__("math").sin(i * 1.2566 + .3)), shade(rim, .8))
        for i in range(5))
    return ('<circle cx="%d" cy="%d" r="%d" fill="#1b1d21"/>'
            '<circle cx="%d" cy="%d" r="%d" fill="%s"/>%s'
            '<circle cx="%d" cy="%d" r="%d" fill="%s"/>'
            '<circle cx="%d" cy="%d" r="3.4" fill="#5d636b"/>') % (
        cx, cy, r, cx, cy, round(r * .62), rim, spokes, cx, cy, round(r * .26), shade(rim, .7), cx, cy)


def car(kind, color):
    p = CARS[kind]
    gd, gu = grad(color)
    a, b, c, d, h, hood = p["a"], p["b"], p["c"], p["d"], p["h"], p["hood"]
    lower = ("M8,-24 L8,-52 Q8,-63 24,-66 L%d,-66 Q%d,-60 %d,-44 L%d,-24 Z" %
             (d + 6, hood - 12, hood, hood))
    cabin = "M%d,-66 L%d,%d Q%d,%d %d,%d L%d,%d L%d,-66 Z" % (a, b, h + 4, b + 6, h, b + 16, h, c, h, d)
    win = "M%d,-70 L%d,%d L%d,%d L%d,-70 Z" % (a + 14, b + 6, h + 9, c - 6, h + 9, d - 16)
    pillar = (b + c) // 2
    arch_l = '<circle cx="88" cy="-26" r="34" fill="%s"/>' % INK
    arch_r = '<circle cx="314" cy="-26" r="34" fill="%s"/>' % INK
    return {
        "defs": gd,
        "svg": (
            '<ellipse cx="200" cy="2" rx="200" ry="9" fill="#14161a" opacity=".16"/>'
            + arch_l + arch_r
            + '<path d="%s" fill="%s"/>' % (lower, gu)
            + '<path d="%s" fill="%s"/>' % (cabin, shade(color, .86))
            + '<path d="%s" fill="%s"/>' % (win, GLASS)
            + '<path d="%s" fill="%s" opacity=".5"/>' % (win, "#ffffff")
            + '<rect x="%d" y="%d" width="7" height="%d" fill="%s"/>' % (pillar - 3, h + 8, -70 - (h + 8), shade(color, .86))
            + '<path d="M%d,-66 L%d,-30" stroke="%s" stroke-width="2" opacity=".5"/>' % (pillar, pillar, shade(color, .6))
            + '<rect x="%d" y="-56" width="16" height="4" rx="2" fill="%s" opacity=".7"/>' % (pillar + 12, shade(color, .6))
            + '<path d="M10,-30 L%d,-30" stroke="%s" stroke-width="3" opacity=".35"/>' % (hood - 2, INK)
            + '<rect x="%d" y="-52" width="11" height="9" rx="3" fill="#fff3c4"/>' % (hood - 14)
            + '<rect x="9" y="-56" width="9" height="12" rx="3" fill="#e0452b"/>'
            + wheel(88, -26, 26) + wheel(314, -26, 26)
        ),
    }


# ------------------------------------------------------------------------- moto
def moto(kind, color):
    gd, gu = grad(color)
    r = {"naked": 30, "scooter": 24, "trail": 34}[kind]
    lift = {"naked": 0, "scooter": 0, "trail": 4}[kind]
    rx, fx = 62, (270 if kind != "scooter" else 250)
    cy = -r
    tire = lambda x: ('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#1b1d21" stroke-width="%d"/>'
                      '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#b5bac1" stroke-width="2.4"/>'
                      '<circle cx="%d" cy="%d" r="4" fill="#5d636b"/>'
                      % (x, cy, r - 4, 9, x, cy, r - 11, x, cy)) + "".join(
        '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#b5bac1" stroke-width="1.2"/>' % (
            x, cy, x + round((r - 12) * __import__("math").cos(i * .5236)), cy + round((r - 12) * __import__("math").sin(i * .5236)))
        for i in range(12))
    s = '<ellipse cx="170" cy="2" rx="170" ry="8" fill="#14161a" opacity=".16"/>'
    if kind == "scooter":
        s += (
            '<path d="M%d,%d L%d,-92 L%d,-100" stroke="#8e949c" stroke-width="7" fill="none" stroke-linecap="round"/>' % (fx, cy, fx - 22, fx - 28)
            + '<path d="M%d,-102 L%d,-106 L%d,-102" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round"/>' % (fx - 36, fx - 24, fx - 16, INK)
            + '<path d="M%d,-92 Q%d,-70 %d,-40 L%d,-34 L%d,-72 Z" fill="%s"/>' % (fx - 14, fx - 4, fx - 30, fx - 70, fx - 62, gu)
            + '<path d="M40,-34 L%d,-34 L%d,-28 L38,-28 Z" fill="%s"/>' % (fx - 60, fx - 60, shade(color, .7))
            + '<path d="M30,-62 Q38,-92 78,-90 L128,-90 L132,-60 Z" fill="%s"/>' % gu
            + '<path d="M70,-92 Q100,-102 150,-96 L148,-84 L72,-84 Z" fill="%s"/>' % INK
            + '<ellipse cx="%d" cy="-90" rx="9" ry="11" fill="#fff3c4"/>' % (fx - 30)
            + '<rect x="30" y="-70" width="8" height="12" rx="3" fill="#e0452b"/>'
            + '<path d="M%d,-44 L50,-38" stroke="#8e949c" stroke-width="8" stroke-linecap="round"/>' % (rx + 52)
        )
    else:
        top = -112 - lift
        s += (
            # horquilla y manillar
            '<path d="M%d,%d L%d,%d" stroke="#8e949c" stroke-width="7" stroke-linecap="round"/>' % (fx, cy, fx - 34, top + 6)
            + '<path d="M%d,%d L%d,%d" stroke="#5d636b" stroke-width="3" stroke-linecap="round"/>' % (fx + 6, cy, fx - 28, top + 6)
            + '<path d="M%d,%d L%d,%d L%d,%d" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round"/>' % (fx - 42, top + 2, fx - 52, top - 4, fx - 62, top + 4, INK)
            # cuadro, motor, escape
            + '<path d="M120,-50 L212,-92" stroke="#8e949c" stroke-width="6" stroke-linecap="round"/>'
            + '<path d="M%d,%d L%d,-56" stroke="#8e949c" stroke-width="6" stroke-linecap="round"/>' % (rx, cy, 128)
            + '<path d="M140,-78 L214,-78 L214,-40 Q200,-34 176,-36 L140,-40 Z" fill="#3a3d44"/>'
            + "".join('<line x1="%d" y1="-76" x2="%d" y2="-62" stroke="#5d636b" stroke-width="2"/>' % (x, x) for x in (152, 166, 180, 194))
            + '<path d="M170,-42 L%d,-46" stroke="#8e949c" stroke-width="9" stroke-linecap="round"/>' % (rx - 14)
            # depósito, asiento, colín
            + '<path d="M150,-102 Q170,-128 214,-118 L238,%d L220,-92 L150,-90 Z" fill="%s"/>' % (top + 8, gu)
            + '<path d="M72,-98 Q110,-108 152,-100 L152,-88 L72,-86 Z" fill="%s"/>' % INK
            + '<path d="M50,-98 Q60,-110 78,-100 L76,-86 Z" fill="%s"/>' % shade(color, .8)
            # faro y piloto
            + '<ellipse cx="%d" cy="%d" rx="10" ry="12" fill="#fff3c4"/>' % (fx - 24, top + 20)
            + '<rect x="46" y="-98" width="8" height="10" rx="3" fill="#e0452b"/>'
        )
        if kind == "trail":
            s += ('<path d="M%d,%d Q%d,%d %d,%d" stroke="%s" stroke-width="8" fill="none" stroke-linecap="round"/>'
                  % (fx - 18, cy - r + 6, fx + 4, cy - r - 6, fx + 30, cy - r + 8, shade(color, .85))
                  + '<path d="M%d,%d L%d,%d L%d,%d Z" fill="%s" opacity=".85"/>' % (fx - 44, top + 4, fx - 30, top - 22, fx - 22, top + 8, GLASS))
    s += tire(rx) + tire(fx)
    return {"defs": gd, "svg": s}


# ------------------------------------------------------------------------ escena
BG = [("#f3dccb", "#f08a4b"), ("#dde2e6", "#c2410c"), ("#ece4d2", "#f08a4b"), ("#d5dce2", "#3d6d9e"),
      ("#f5e6d8", "#c2410c"), ("#cfd6dc", "#f08a4b"), ("#f0d4c3", "#3d6d9e"), ("#e3e6e0", "#c2410c")]
COLORS = ["#e2571c", "#2b2e34", "#3d6d9e", "#eceae4", "#3f7d5a", "#e3b02b", "#aab1b9", "#b3261e"]


def place(veh, w, h, cx, base, width):
    """Coloca el vehículo (ancho natural ≈ 400) centrado en cx, con el suelo en 'base'."""
    k = width / 400.0
    return '<g transform="translate(%.1f %.1f) scale(%.3f)">%s</g>' % (cx - 200 * k, base, k, veh["svg"])


def scene(w, h, items, bg, floor=.78, sun=True, label=None):
    """items: lista de (vehículo, cx, ancho). Fondo plano + círculo naranja + suelo."""
    c1, c2 = bg
    base = h * floor
    defs = "".join(v["defs"] for v, _, _ in items)
    body = '<rect width="%d" height="%d" fill="%s"/>' % (w, h, c1)
    if sun:
        body += '<circle cx="%.0f" cy="%.0f" r="%.0f" fill="%s" opacity=".28"/>' % (w * .68, h * .42, h * .36, c2)
    body += '<rect y="%.0f" width="%d" height="%.0f" fill="#14161a" opacity=".07"/>' % (base, w, h - base)
    body += '<line x1="0" y1="%.0f" x2="%d" y2="%.0f" stroke="#14161a" stroke-opacity=".18" stroke-width="2"/>' % (base, w, base)
    for v, cx, width in items:
        body += place(v, w, h, cx, base + h * .035, width)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img">'
            '<defs>%s</defs>%s</svg>') % (w, h, w, h, defs, body)


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def main():
    os.makedirs(OUT, exist_ok=True)

    # Hero: SUV + moto naked
    write("hero.svg", scene(1040, 693, [(car("suv", "#e2571c"), 330, 560), (moto("naked", "#2b2e34"), 850, 380)], BG[0]))

    # Marquee: 12 escenas
    plan = [("car", "urbano"), ("moto", "naked"), ("car", "berlina"), ("moto", "scooter"), ("car", "suv"), ("moto", "trail"),
            ("car", "coupe"), ("car", "familiar"), ("moto", "naked"), ("car", "urbano"), ("moto", "scooter"), ("car", "suv")]
    for i, (t, k) in enumerate(plan):
        col = COLORS[(i * 3 + 1) % len(COLORS)]
        v = car(k, col) if t == "car" else moto(k, col)
        wdt = 660 if t == "car" else 560
        write("mq-%02d.svg" % (i + 1), scene(840, 540, [(v, 420 + (i % 3 - 1) * 20, wdt)], BG[i % len(BG)]))

    # Deco: rueda, cuentakilómetros, llave, casco (440×440)
    wheel_svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440" width="440" height="440" role="img">'
                 '<rect width="440" height="440" fill="#f3dccb"/><circle cx="220" cy="220" r="150" fill="#1b1d21"/>'
                 '<circle cx="220" cy="220" r="104" fill="#c9ced4"/>%s<circle cx="220" cy="220" r="26" fill="#5d636b"/></svg>') % "".join(
        '<line x1="220" y1="220" x2="%d" y2="%d" stroke="#8e949c" stroke-width="12" stroke-linecap="round"/>' % (
            220 + round(92 * __import__("math").cos(i * 1.0472)), 220 + round(92 * __import__("math").sin(i * 1.0472))) for i in range(6))
    write("deco-1.svg", wheel_svg)
    dial = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440" width="440" height="440" role="img">'
            '<rect width="440" height="440" fill="#dde2e6"/><circle cx="220" cy="220" r="160" fill="#14161a"/>'
            '<circle cx="220" cy="220" r="140" fill="none" stroke="#5d636b" stroke-width="3"/>%s'
            '<path d="M220,220 L300,150" stroke="#f08a4b" stroke-width="7" stroke-linecap="round"/><circle cx="220" cy="220" r="12" fill="#eceae4"/></svg>') % "".join(
        '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#eceae4" stroke-width="%d"/>' % (
            220 + round(122 * __import__("math").cos(a)), 220 + round(122 * __import__("math").sin(a)),
            220 + round(138 * __import__("math").cos(a)), 220 + round(138 * __import__("math").sin(a)), 4 if i % 3 == 0 else 2)
        for i, a in enumerate([2.4 + i * 0.2 for i in range(24)]))
    write("deco-2.svg", dial)
    key = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440" width="440" height="440" role="img">'
           '<rect width="440" height="440" fill="#ece4d2"/><g transform="rotate(-28 220 220)">'
           '<rect x="130" y="196" width="190" height="48" rx="24" fill="#14161a"/><circle cx="178" cy="220" r="14" fill="#ece4d2"/>'
           '<rect x="300" y="208" width="90" height="24" rx="6" fill="#aab1b9"/>'
           '<path d="M330,232 v14 M352,232 v22 M374,232 v12" stroke="#aab1b9" stroke-width="8"/></g></svg>')
    write("deco-3.svg", key)
    helmet = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440" width="440" height="440" role="img">'
              '<rect width="440" height="440" fill="#f5e6d8"/><path d="M90,270 Q90,120 230,120 Q350,120 350,250 L350,300 L190,300 Q160,300 150,270 Z" fill="#e2571c"/>'
              '<path d="M200,200 L350,200 L350,262 L216,262 Q196,240 200,200 Z" fill="#14161a"/>'
              '<path d="M214,214 L340,214 L340,250 L224,250 Q212,236 214,214 Z" fill="#cfd9e2" opacity=".9"/>'
              '<rect x="120" y="300" width="230" height="22" rx="11" fill="#14161a"/></svg>')
    write("deco-4.svg", helmet)

    # Casos: 01 utilitario urbano, 02 moto naked, 03 SUV familiar (a: 940×460, b: 940×676, c: 1200×980)
    casos = [("1", lambda: car("urbano", "#e2571c"), .66, BG[0]), ("2", lambda: moto("naked", "#2b2e34"), .58, BG[3]),
             ("3", lambda: car("suv", "#3d6d9e"), .68, BG[2])]
    for n, mk, wdt, bg in casos:
        for suf, (w, h, k, flo) in {"a": (940, 460, 1, .8), "b": (940, 676, 1, .78), "c": (1200, 980, 1, .74)}.items():
            write("case%s-%s.svg" % (n, suf), scene(w, h, [(mk(), w * .5, w * wdt * (1.0 if suf != "b" else 1.2))], bg, floor=flo, sun=(suf != "b")))
    print("ok")


if __name__ == "__main__":
    main()
