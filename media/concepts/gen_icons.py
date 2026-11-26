"""Generate 12 icon concepts for Rotate Minimap (Forever) as 512x512 SVGs."""
import math
import os
import sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
C = 256  # centre


# ---------- geometry helpers (angle 0 = up/north, clockwise positive) ----------
def P(r, a, cx=C, cy=C):
    t = math.radians(a)
    return (cx + r * math.sin(t), cy - r * math.cos(t))


def f(pt):
    return f"{pt[0]:.1f},{pt[1]:.1f}"


def arc_arrow(r, a0, a1, w, fill, stroke="none", sw=0, head=1.5, cx=C, cy=C, opacity=1):
    s = 1 if a1 > a0 else -1
    ro, ri = r + w / 2, r - w / 2
    large = 1 if abs(a1 - a0) > 180 else 0
    so = 1 if s > 0 else 0
    hd = s * math.degrees(w * head / r)
    d = (
        f"M{f(P(ro, a0, cx, cy))} A{ro:.1f},{ro:.1f} 0 {large} {so} {f(P(ro, a1, cx, cy))} "
        f"L{f(P(r + w * 1.1, a1, cx, cy))} L{f(P(r, a1 + hd, cx, cy))} L{f(P(r - w * 1.1, a1, cx, cy))} "
        f"L{f(P(ri, a1, cx, cy))} A{ri:.1f},{ri:.1f} 0 {large} {1 - so} {f(P(ri, a0, cx, cy))} Z"
    )
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linejoin="round" opacity="{opacity}"/>')


def arc(r, a0, a1, color, w, cap="round", opacity=1):
    large = 1 if abs(a1 - a0) > 180 else 0
    so = 1 if a1 > a0 else 0
    return (f'<path d="M{f(P(r, a0))} A{r},{r} 0 {large} {so} {f(P(r, a1))}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="{cap}" opacity="{opacity}"/>')


def ticks(r1, r2, n, color, w, rot=0, major_every=0, major_r1=None, major_w=None):
    out = []
    for i in range(n):
        a = rot + i * 360 / n
        is_major = major_every and i % major_every == 0
        a_r1 = major_r1 if is_major and major_r1 is not None else r1
        a_w = major_w if is_major and major_w else w
        out.append(f'<line x1="{P(a_r1, a)[0]:.1f}" y1="{P(a_r1, a)[1]:.1f}" '
                   f'x2="{P(r2, a)[0]:.1f}" y2="{P(r2, a)[1]:.1f}" stroke="{color}" stroke-width="{a_w}"/>')
    return "".join(out)


def chevron(s, fill, stroke, sw, cx=C, cy=C, rot=0):
    pts = [(0, -s), (0.72 * s, 0.78 * s), (0, 0.38 * s), (-0.72 * s, 0.78 * s)]
    d = "M" + " L".join(f"{cx + x:.1f},{cy + y + 0.1 * s:.1f}" for x, y in pts) + " Z"
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linejoin="round" transform="rotate({rot} {cx} {cy})"/>')


def letter_n(cx, cy, h, color, w, rot=0):
    hw = h * 0.36
    d = f"M{cx - hw:.1f},{cy + h / 2:.1f} V{cy - h / 2:.1f} L{cx + hw:.1f},{cy + h / 2:.1f} V{cy - h / 2:.1f}"
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="miter" stroke-miterlimit="1.6" '
            f'stroke-linecap="butt" transform="rotate({rot} {cx:.1f} {cy:.1f})"/>')


def rose_point(R, rin, a, light, dark):
    tip, left, right = P(R, a), P(rin, a - 45), P(rin, a + 45)
    return (f'<path d="M{C},{C} L{f(tip)} L{f(left)} Z" fill="{light}"/>'
            f'<path d="M{C},{C} L{f(tip)} L{f(right)} Z" fill="{dark}"/>')


def bez(p0, p1, p2, p3, t):
    mt = 1 - t
    pt = tuple(mt**3 * a + 3 * mt * mt * t * b + 3 * mt * t * t * c + t**3 * d
               for a, b, c, d in zip(p0, p1, p2, p3))
    tan = tuple(3 * mt * mt * (b - a) + 6 * mt * t * (c - b) + 3 * t * t * (d - c)
                for a, b, c, d in zip(p0, p1, p2, p3))
    n = math.hypot(*tan)
    return pt, (tan[0] / n, tan[1] / n)


def terrain():
    """Top-down landscape filling the 512 box (original, generic)."""
    trees = [(150, 120), (175, 140), (140, 150), (300, 340), (325, 360), (290, 370), (350, 330),
             (120, 300), (100, 325), (140, 330), (380, 210), (400, 235)]
    tree_svg = "".join(f'<circle cx="{x}" cy="{y}" r="20" fill="#2E5A2B"/>'
                       f'<circle cx="{x - 5}" cy="{y - 6}" r="9" fill="#3F7334"/>' for x, y in trees)
    return f"""
<rect width="512" height="512" fill="#4C7A3C"/>
<path d="M0,300 C90,280 130,350 210,330 C290,310 300,240 380,250 C440,258 480,225 512,215 V512 H0Z" fill="#5E8C47"/>
<path d="M200,70 L240,140 H160Z M250,90 L290,160 H210Z" fill="#7C7466"/>
<path d="M200,70 L214,95 H186Z M250,90 L264,115 H236Z" fill="#ECE7DC"/>
<ellipse cx="340" cy="150" rx="70" ry="46" fill="#2C6684"/>
<ellipse cx="335" cy="145" rx="52" ry="30" fill="#4C9AC0"/>
<path d="M-10,190 C70,210 120,170 180,200 C240,230 230,290 300,310 C370,330 430,300 530,360" fill="none" stroke="#2C6684" stroke-width="30" stroke-linecap="round"/>
<path d="M-10,190 C70,210 120,170 180,200 C240,230 230,290 300,310 C370,330 430,300 530,360" fill="none" stroke="#4C9AC0" stroke-width="14" stroke-linecap="round"/>
<path d="M60,520 C120,430 190,430 240,390 C290,350 300,260 360,240 C410,224 440,170 470,90" fill="none" stroke="#D8C08A" stroke-width="10" stroke-linecap="round"/>
{tree_svg}
<rect x="226" y="372" width="26" height="22" fill="#B5522F"/><rect x="226" y="364" width="26" height="10" fill="#7A3720"/>
"""


def parchment_map():
    return """
<rect width="512" height="512" fill="#E9D8A6"/>
<path d="M-10,200 C80,230 130,170 200,210 C270,250 250,320 330,340 C400,358 450,320 530,370" fill="none" stroke="#5E93AE" stroke-width="16" stroke-linecap="round"/>
<path d="M80,520 C140,420 230,420 260,340 C290,260 360,240 420,120" fill="none" stroke="#7A5A2A" stroke-width="7" stroke-dasharray="16 12" stroke-linecap="round"/>
<path d="M150,130 l18,-30 l18,30 M190,140 l18,-30 l18,30 M300,400 l14,-22 l14,22 M330,410 l14,-22 l14,22" fill="none" stroke="#7A5A2A" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>
<g fill="#6E8A3E"><circle cx="330" cy="170" r="11"/><circle cx="352" cy="182" r="11"/><circle cx="336" cy="194" r="11"/><circle cx="140" cy="300" r="11"/><circle cx="162" cy="312" r="11"/></g>
<path d="M366,288 l20,20 m0,-20 l-20,20" stroke="#A8321F" stroke-width="8" stroke-linecap="round"/>
"""


def svg(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">'
            f'<defs>{defs}</defs>{body}</svg>\n')


ICONS = []


def icon(slug, name, note):
    def deco(fn):
        ICONS.append((slug, name, note, fn))
        return fn
    return deco


@icon("01-brass-minimap", "Brass minimap",
      "A round minimap in a brass ring. The map is turned and the N gem moved off the top. Arrows on the ring show the turn.")
def i01(p):
    defs = f"""
<linearGradient id="{p}ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE6A0"/><stop offset=".45" stop-color="#C8912F"/><stop offset="1" stop-color="#6E440F"/></linearGradient>
<radialGradient id="{p}vig"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>
<clipPath id="{p}disc"><circle cx="256" cy="256" r="194"/></clipPath>"""
    n = P(219, -32)
    body = f"""
<circle cx="256" cy="256" r="246" fill="#3A2508"/>
<circle cx="256" cy="256" r="240" fill="url(#{p}ring)"/>
<circle cx="256" cy="256" r="200" fill="#2A1A06"/>
<g clip-path="url(#{p}disc)"><g transform="rotate(-32 256 256)">{terrain()}</g><circle cx="256" cy="256" r="194" fill="url(#{p}vig)"/></g>
{arc_arrow(219, 20, 125, 20, "#FFF2C4", "#4A2C06", 5)}
{arc_arrow(219, 160, 265, 20, "#FFF2C4", "#4A2C06", 5)}
<circle cx="{n[0]:.1f}" cy="{n[1]:.1f}" r="30" fill="#B8321F" stroke="#FFE6A0" stroke-width="6"/>
{letter_n(n[0], n[1], 26, "#FFF6E0", 7, -32)}
{chevron(64, "#FFD447", "#2A1A06", 9)}"""
    return svg(body, defs)


@icon("02-compass-rose", "Compass rose",
      "A compass rose turned 30 degrees on a night-blue face, with two turn arrows. Reads as navigation first.")
def i02(p):
    body = f"""
<circle cx="256" cy="256" r="246" fill="#172231"/>
<circle cx="256" cy="256" r="234" fill="none" stroke="#C9A04A" stroke-width="12"/>
{ticks(206, 222, 72, "#C9A04A", 3, rot=30)}
{arc_arrow(190, 55, 100, 16, "#7FC4D9")}
{arc_arrow(190, 235, 280, 16, "#7FC4D9")}
<g>{rose_point(100, 26, 75, "#9DB1C4", "#5A6E84")}{rose_point(100, 26, 165, "#9DB1C4", "#5A6E84")}
{rose_point(100, 26, 255, "#9DB1C4", "#5A6E84")}{rose_point(100, 26, 345, "#9DB1C4", "#5A6E84")}
{rose_point(172, 38, 120, "#F3E3B5", "#B8873A")}{rose_point(172, 38, 210, "#F3E3B5", "#B8873A")}
{rose_point(172, 38, 300, "#F3E3B5", "#B8873A")}{rose_point(172, 38, 30, "#F0614A", "#9C2A1A")}</g>
<circle cx="256" cy="256" r="18" fill="#F3E3B5" stroke="#172231" stroke-width="5"/>"""
    return svg(body)


@icon("03-heading-up-dial", "Heading-up dial",
      "The player arrow stays fixed and points up. The dial and its N turn around it. This is what the setting does.")
def i03(p):
    defs = f"""<radialGradient id="{p}bg"><stop offset="0" stop-color="#2A3D55"/><stop offset="1" stop-color="#0E1622"/></radialGradient>"""
    n = P(138, 24)
    tri = [P(206, 0), P(238, -7), P(238, 7)]
    body = f"""
<circle cx="256" cy="256" r="246" fill="url(#{p}bg)"/>
<circle cx="256" cy="256" r="200" fill="none" stroke="#3B5068" stroke-width="3"/>
{ticks(180, 200, 72, "#9FB6CC", 3, rot=24, major_every=9, major_r1=160, major_w=7)}
{letter_n(n[0], n[1], 42, "#FF6B4A", 9, 24)}
<path d="M{f(tri[0])} L{f(tri[1])} L{f(tri[2])} Z" fill="#FFD447" stroke="#FFD447" stroke-width="6" stroke-linejoin="round"/>
{arc_arrow(222, 115, 205, 13, "#9FB6CC", opacity=.85)}
{chevron(92, "#FFD447", "#0E1622", 11)}"""
    return svg(body, defs)


@icon("04-refresh-map", "Refresh map",
      "A parchment map inside two heavy turn arrows. Simple shapes that still read at 32 px.")
def i04(p):
    defs = f"""<clipPath id="{p}disc"><circle cx="256" cy="256" r="166"/></clipPath>"""
    body = f"""
<circle cx="256" cy="256" r="172" fill="#7A5A2A"/>
<g clip-path="url(#{p}disc)"><g transform="rotate(18 256 256)">{parchment_map()}</g></g>
{arc_arrow(216, 18, 148, 40, "#E0A93A", "#5A3608", 7)}
{arc_arrow(216, 198, 328, 40, "#E0A93A", "#5A3608", 7)}
{chevron(44, "#B8321F", "#4A2C06", 7)}"""
    return svg(body, defs)


@icon("05-turning-tile", "Turning tile",
      "A square map tile turned under an upright arrow, framed in a dark round window with motion arcs.")
def i05(p):
    defs = f"""<clipPath id="{p}win"><circle cx="256" cy="256" r="226"/></clipPath>
<clipPath id="{p}tile"><rect x="96" y="96" width="320" height="320"/></clipPath>"""
    body = f"""
<circle cx="256" cy="256" r="244" fill="#C9A04A"/>
<circle cx="256" cy="256" r="230" fill="#1E2A22"/>
<g clip-path="url(#{p}win)"><g transform="rotate(26 256 256)">
<g clip-path="url(#{p}tile)">{terrain()}</g>
<rect x="96" y="96" width="320" height="320" fill="none" stroke="#F3E3B5" stroke-width="8"/></g></g>
{arc_arrow(210, 300, 350, 14, "#C9A04A")}
{arc_arrow(210, 120, 170, 14, "#C9A04A")}
{chevron(58, "#FFD447", "#1E2A22", 9)}"""
    return svg(body, defs)


@icon("06-flat-teal", "Flat teal",
      "Two colours, no detail: a disc, one turn arrow, the player arrow and an N. Best for the smallest sizes.")
def i06(p):
    n = P(182, -20)
    body = f"""
<circle cx="256" cy="256" r="244" fill="#1F7A8C"/>
{arc_arrow(182, 22, 292, 36, "#FFFFFF")}
{letter_n(n[0], n[1], 46, "#FFFFFF", 12, -20)}
{chevron(82, "#FFFFFF", "#FFFFFF", 4)}"""
    return svg(body)


@icon("07-astrolabe", "Astrolabe",
      "A brass instrument with a turned inner plate and a fixed red index at the top. Old-world and detailed.")
def i07(p):
    defs = f"""
<linearGradient id="{p}brass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F6D98A"/><stop offset=".5" stop-color="#B07C2A"/><stop offset="1" stop-color="#5E3C0C"/></linearGradient>
<radialGradient id="{p}enamel"><stop offset="0" stop-color="#30445A"/><stop offset="1" stop-color="#121C28"/></radialGradient>"""
    tri = [P(200, 0), P(240, -8), P(240, 8)]
    tip = P(176, -35)
    body = f"""
<circle cx="256" cy="256" r="244" fill="url(#{p}brass)" stroke="#3E2706" stroke-width="6"/>
{ticks(206, 234, 120, "#3E2706", 2.5, major_every=10, major_r1=198, major_w=5)}
<circle cx="256" cy="256" r="196" fill="url(#{p}enamel)" stroke="#3E2706" stroke-width="4"/>
<g transform="rotate(-35 256 256)">
<circle cx="256" cy="256" r="150" fill="none" stroke="#E8C068" stroke-width="7"/>
<circle cx="256" cy="226" r="92" fill="none" stroke="#E8C068" stroke-width="4"/>
<path d="M256,106 V406 M106,256 H406" stroke="#E8C068" stroke-width="4" opacity=".6"/>
<path d="M256,78 L272,256 L256,290 L240,256 Z" fill="#E8C068" stroke="#3E2706" stroke-width="3"/>
</g>
<circle cx="{tip[0]:.1f}" cy="{tip[1]:.1f}" r="14" fill="#C8432B" stroke="#3E2706" stroke-width="3"/>
<circle cx="256" cy="256" r="26" fill="url(#{p}brass)" stroke="#3E2706" stroke-width="4"/>
<path d="M{f(tri[0])} L{f(tri[1])} L{f(tri[2])} Z" fill="#C8432B" stroke="#3E2706" stroke-width="4" stroke-linejoin="round"/>"""
    return svg(body, defs)


@icon("08-square-badge", "Square badge",
      "A square, bevelled badge like an ability icon, with a round minimap inside. Fits square avatar slots.")
def i08(p):
    defs = f"""
<linearGradient id="{p}frame" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E9CB7A"/><stop offset=".5" stop-color="#8E6420"/><stop offset="1" stop-color="#4A300A"/></linearGradient>
<linearGradient id="{p}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#25507A"/><stop offset="1" stop-color="#0B1828"/></linearGradient>
<linearGradient id="{p}sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF" stop-opacity=".18"/><stop offset=".5" stop-color="#FFF" stop-opacity="0"/></linearGradient>
<clipPath id="{p}disc"><circle cx="256" cy="256" r="160"/></clipPath>"""
    body = f"""
<rect x="4" y="4" width="504" height="504" rx="34" fill="#120C04"/>
<rect x="18" y="18" width="476" height="476" rx="24" fill="url(#{p}frame)"/>
<rect x="44" y="44" width="424" height="424" rx="10" fill="url(#{p}sky)"/>
<g clip-path="url(#{p}disc)"><g transform="rotate(-22 256 256)">{terrain()}</g></g>
<circle cx="256" cy="256" r="164" fill="none" stroke="#D8B25A" stroke-width="12"/>
{arc_arrow(196, 28, 112, 18, "#F1D58A", "#1A1206", 4)}
{arc_arrow(196, 208, 292, 18, "#F1D58A", "#1A1206", 4)}
{chevron(46, "#FFD447", "#1A1206", 8)}
<rect x="44" y="44" width="424" height="424" rx="10" fill="url(#{p}sheen)"/>
<rect x="44" y="44" width="424" height="424" rx="10" fill="none" stroke="#000" stroke-opacity=".55" stroke-width="6"/>"""
    return svg(body, defs)


@icon("09-spinning-n", "Spinning N",
      "A large N on a red disc, turned, with speed arcs. Bold and graphic, with no map at all.")
def i09(p):
    defs = f"""<radialGradient id="{p}red" cx=".35" cy=".3"><stop offset="0" stop-color="#E8593F"/><stop offset="1" stop-color="#861F12"/></radialGradient>"""
    body = f"""
{arc(208, 300, 352, "#E0A93A", 14)}{arc(234, 286, 334, "#E0A93A", 9, opacity=.7)}
{arc(208, 120, 172, "#E0A93A", 14)}{arc(234, 106, 154, "#E0A93A", 9, opacity=.7)}
<circle cx="256" cy="256" r="176" fill="url(#{p}red)" stroke="#FFD98A" stroke-width="12"/>
{letter_n(256, 256, 168, "#FFF2D0", 40, 18)}"""
    return svg(body, defs)


@icon("10-forever-loop", "Forever loop",
      "An infinity loop with an arrowhead, for the Forever client and for a setting that stays on. A compass and player arrow sit in the loops.")
def i10(p):
    d = ("M256,256 C320,130 472,130 472,256 C472,382 320,382 256,256 "
         "C192,130 40,130 40,256 C40,382 192,382 256,256Z")
    (x, y), (tx, ty) = bez((256, 256), (320, 130), (472, 130), (472, 256), 0.62)
    nx, ny = -ty, tx
    L = 52
    tip = (x + tx * L, y + ty * L)
    b1 = (x + nx * L * 0.95, y + ny * L * 0.95)
    b2 = (x - nx * L * 0.95, y - ny * L * 0.95)
    needle_n = P(40, 30, 132, 256)
    needle_s = P(40, 210, 132, 256)
    body = f"""
<path d="{d}" fill="none" stroke="#4A2C06" stroke-width="62" stroke-linejoin="round"/>
<path d="{d}" fill="none" stroke="#E8B84A" stroke-width="44" stroke-linejoin="round"/>
<path d="{d}" fill="none" stroke="#FFE6A0" stroke-width="8" stroke-linejoin="round" opacity=".7"/>
<path d="M{f(tip)} L{f(b1)} L{f(b2)} Z" fill="#E8B84A" stroke="#4A2C06" stroke-width="8" stroke-linejoin="round"/>
<circle cx="132" cy="256" r="50" fill="#172231" stroke="#4A2C06" stroke-width="5"/>
<path d="M{f(needle_n)} L{f(P(11, 120, 132, 256))} L{f(needle_s)} Z" fill="#E8E2D2"/>
<path d="M{f(needle_n)} L{f(P(11, 300, 132, 256))} L{f(P(11, 120, 132, 256))} Z" fill="#E8503A"/>
<circle cx="380" cy="256" r="50" fill="#172231" stroke="#4A2C06" stroke-width="5"/>
{chevron(30, "#FFD447", "#172231", 4, cx=380, cy=256)}"""
    return svg(body)


@icon("11-landscape-spin", "Landscape spin",
      "A bright top-down landscape turned inside a pale ring, with blue speed arcs. The most colourful option.")
def i11(p):
    defs = f"""<clipPath id="{p}disc"><circle cx="256" cy="256" r="178"/></clipPath>"""
    body = f"""
{arc(208, 22, 72, "#7FC4D9", 14)}{arc(234, 36, 82, "#7FC4D9", 9, opacity=.7)}
{arc(208, 202, 252, "#7FC4D9", 14)}{arc(234, 216, 262, "#7FC4D9", 9, opacity=.7)}
<circle cx="256" cy="256" r="186" fill="#22180A"/>
<g clip-path="url(#{p}disc)"><g transform="rotate(38 256 256)">{terrain()}</g></g>
<circle cx="256" cy="256" r="178" fill="none" stroke="#F3E3B5" stroke-width="10"/>
{chevron(52, "#FFD447", "#22180A", 8)}"""
    return svg(body, defs)


@icon("12-monoline", "Monoline",
      "Gold line art with no fill: a broken ring with an arrowhead, the player arrow and an N. Clean, and easy to recolour.")
def i12(p):
    a_end = 296
    end = P(200, a_end)
    t = (math.cos(math.radians(a_end)), math.sin(math.radians(a_end)))
    nrm = (math.sin(math.radians(a_end)), -math.cos(math.radians(a_end)))
    L = 46
    tip = (end[0] + t[0] * 8, end[1] + t[1] * 8)
    h1 = (tip[0] - t[0] * L + nrm[0] * L * 0.8, tip[1] - t[1] * L + nrm[1] * L * 0.8)
    h2 = (tip[0] - t[0] * L - nrm[0] * L * 0.8, tip[1] - t[1] * L - nrm[1] * L * 0.8)
    n = P(200, -22)
    body = f"""
{arc(200, 22, a_end, "#E8B84A", 24)}
<path d="M{f(h1)} L{f(tip)} L{f(h2)}" fill="none" stroke="#E8B84A" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>
{letter_n(n[0], n[1], 50, "#E8B84A", 14, -22)}
{chevron(84, "none", "#E8B84A", 22)}"""
    return svg(body)


if __name__ == "__main__":
    import json
    meta = []
    for slug, name, note, fn in ICONS:
        prefix = "i" + slug[:2] + "_"
        with open(os.path.join(OUT, f"{slug}.svg"), "w") as fh:
            fh.write(fn(prefix))
        meta.append({"slug": slug, "name": name, "note": note})
    with open(os.path.join(OUT, "meta.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
    print(f"wrote {len(meta)} icons to {OUT}")
